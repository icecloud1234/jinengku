#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import re
import datetime
from pathlib import Path

# 竞品App配置
APPS = {
    '千问': 'https://appgallery.huawei.com/app/C109126425',
    '元宝': 'https://appgallery.huawei.com/app/C110782717',
    '豆包': 'https://appgallery.huawei.com/app/C109089785',
    'DeepSeek': 'https://appgallery.huawei.com/app/C112973233',
    'Kimi': 'https://appgallery.huawei.com/app/C110026431'
}

def convert_to_chinese_format(value):
    """
    将英文数字格式转换为中文格式（亿）
    例如：199M -> 1.99亿，3,274M -> 32.74亿
    """
    if not isinstance(value, str):
        return value
    
    # 匹配英文格式：3,274M, 1.5B, 5K (支持逗号)
    match = re.match(r'([\d,]+(?:\.\d+)?)\s*([KMB])', value, re.IGNORECASE)
    if not match:
        return value  # 不是英文格式，直接返回
    
    num_str, unit = match.groups()
    # 移除逗号后转换为数字
    num = float(num_str.replace(',', ''))
    
    # 转换单位（统一转为亿）
    # K = 千 = 1,000 = 0.0001亿
    # M = 百万 = 1,000,000 = 0.01亿
    # B = 十亿 (Billion) = 1,000,000,000 = 1亿
    if unit.upper() == 'K':
        result = num * 0.0001  # 转为亿
        return f'{result:.4f}亿'.rstrip('0').rstrip('.')
    elif unit.upper() == 'M':
        result = num * 0.01  # M是百万，转为亿
        return f'{result:.2f}亿'.rstrip('0').rstrip('.')
    elif unit.upper() == 'B':
        result = num * 1  # B是十亿 (Billion)，1B = 1亿
        return f'{result:.2f}亿'.rstrip('0').rstrip('.')
    
    return value


def get_huawei_app_info(url, app_name, output_dir):
    """获取华为应用市场App信息"""
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    print(f'\n访问: {url}')
    
    try:
        # 使用系统 chromedriver（需要显式指定 Service）
        service = Service('/usr/local/bin/chromedriver')  # 系统默认路径
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
        driver.get(url)
        
        # 等待页面加载
        time.sleep(3)
        
        # 获取页面文本
        page_text = driver.find_element(By.TAG_NAME, 'body').text
        
        # 提取应用名称（如果未提供）
        if not app_name:
            try:
                app_name_elem = driver.find_element(By.TAG_NAME, 'h1')
                app_name = app_name_elem.text.strip()
            except:
                app_name = 'unknown'
        
        # 提取下载量/安装量
        download_count = 'unknown'
        
        # 正则匹配下载量/安装量（支持中英文格式和逗号分隔符）
        patterns = [
            # 英文格式：3,274M installs, 1.5B installs (支持逗号)
            r'([\d,]+(?:\.\d+)?[KMB])\s+installs?',
            r'([\d,]+(?:\.\d+)?[KMB])\s+downloads?',
            # 中文格式
            r'([0-9.]+)\s*([亿千万百十]+)\s*次\s*安装',
            r'([0-9.]+)\s*([亿千万百十]+)\s*次\s*下载',
            r'([0-9,.]+[万亿千百十]+)\s*次?安装',
            r'([0-9,.]+[万亿千百十]+)\s*次?下载'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    download_count = ''.join(matches[0])
                else:
                    download_count = matches[0]
                # 转换为中文格式
                download_count = convert_to_chinese_format(download_count)
                break
        
        # 提取评分
        rating = 'unknown'
        
        # 华为页面的评分通常出现在前几个单独的行中，格式为 "3.3"
        rating_patterns = [
            r'^(\d+\.\d+)$',  # 单独一行只有评分数字
            r'(\d+\.\d+)\s*[★⭐]',
            r'评分[：:]*\s*(\d+\.\d+)',
            r'(\d+\.\d+)\s*分',
            r'(\d+\.\d+)\s*/\s*5'
        ]
        
        for pattern in rating_patterns:
            # 对于第一个模式，按行匹配
            if pattern == r'^(\d+\.\d+)$':
                for line in page_text.split('\n')[:20]:  # 只检查前20行
                    match = re.match(pattern, line.strip())
                    if match:
                        potential_rating = float(match.group(1))
                        # 评分应该在0-5之间
                        if 0 <= potential_rating <= 5:
                            rating = match.group(1)
                            break
            else:
                matches = re.findall(pattern, page_text)
                if matches:
                    rating = matches[0]
                    break
            
            if rating != 'unknown':
                break
        
        # 提取评论数
        review_count = 'unknown'
        review_patterns = [
            # 英文格式：Ratings: 1400, Reviews: 5.2K
            r'Ratings?:\s*(\d+(?:\.\d+)?[KMB]?)',
            r'Reviews?:\s*(\d+(?:\.\d+)?[KMB]?)',
            # 中文格式
            r'([0-9.]+[万千百十]?)\s*人评分',
            r'([0-9,.]+)\s*条评论',
            r'评论[：:]*\s*([0-9,.]+[万千]?)',
            r'([0-9,.]+[万千]?)\s*人'
        ]
        
        for pattern in review_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                review_count = matches[0]
                break
        
        # 截图保存到本次运行的文件夹
        screenshot_path = str(output_dir / f'{app_name}-screenshot.png')
        driver.save_screenshot(screenshot_path)
        
        driver.quit()
        
        result = {
            'app_name': app_name,
            'download_count': download_count,
            'rating': rating,
            'review_count': review_count,
            'url': url,
            'screenshot': screenshot_path,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        print(f'  下载量: {download_count} | 评分: {rating} | 评论数: {review_count}')
        
        return result
        
    except Exception as e:
        print(f'  爬取失败: {e}')
        return {
            'app_name': app_name,
            'download_count': 'unknown',
            'rating': 'unknown',
            'review_count': 'unknown',
            'url': url,
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }

if __name__ == '__main__':
    print('='*70)
    print('华为应用市场 - AI竞品监控')
    print('='*70)
    
    # 创建本次运行的文件夹
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    output_dir = Path(f'./logs/huawei/{timestamp}')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f'\n📁 输出目录: {output_dir}')
    
    all_results = []
    
    for app_name, app_url in APPS.items():
        print(f'\n[{app_name}]')
        result = get_huawei_app_info(app_url, app_name, output_dir)
        all_results.append(result)
    
    # 保存汇总JSON到本次运行的文件夹
    json_path = output_dir / 'summary.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print('\n' + '='*70)
    print('汇总结果')
    print('='*70)
    for result in all_results:
        print(f"{result['app_name']:12s} | 下载: {result['download_count']:10s} | 评分: {result['rating']:8s} | 评论: {result['review_count']}")
    
    print(f'\n✅ 结果已保存到: {output_dir}')
    print(f'   - summary.json (汇总数据)')
    print(f'   - *-screenshot.png (各App截图)')

