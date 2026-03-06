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
    '千问': 'https://sj.qq.com/appdetail/com.aliyun.tongyi',
    '元宝': 'https://sj.qq.com/appdetail/com.tencent.hunyuan.app.chat',
    '豆包': 'https://sj.qq.com/appdetail/com.larus.nova',
    'DeepSeek': 'https://sj.qq.com/appdetail/com.deepseek.chat',
    'Kimi': 'https://sj.qq.com/appdetail/com.moonshot.kimichat'
}

def get_yingyongbao_app_info(url, app_name, output_dir):
    """获取应用宝App信息"""
    
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
        time.sleep(2)
        
        # 获取页面文本
        page_text = driver.find_element(By.TAG_NAME, 'body').text
        
        # 提取应用名称（如果未提供）
        if not app_name:
            name_selectors = ['h1.det-name', '.det-name', 'h1', '.name']
            for selector in name_selectors:
                try:
                    app_name_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    if app_name_elem:
                        app_name = app_name_elem.text.strip()
                        if app_name:
                            break
                except:
                    continue
            if not app_name:
                app_name = 'unknown'
        
        # 提取下载量
        download_count = 'unknown'
        
        # 正则匹配下载量（支持小数点和加号）
        patterns = [
            # 支持小数：2085.2万下载
            r'([0-9.]+)\s*([亿千万百十]+)\s*次?\s*下载',
            r'([0-9.]+)\s*([亿千万百十]+)\s*次?\s*安装',
            r'([0-9,.]+[万亿千百十]+)\s*次?下载',
            # 支持加号：1000万+下载
            r'([0-9.]+[万亿千百十]+)\+?\s*下载'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    download_count = ''.join(matches[0])
                else:
                    download_count = matches[0]
                break
        
        # 提取评分
        rating = 'unknown'
        
        # 应用宝页面的评分通常为 "4.1" 这种单独数字
        rating_patterns = [
            r'^(\d+\.\d+)$',  # 单独一行只有评分数字
            r'[★⭐]\s*(\d+\.\d+)',
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
        
        # 提取评论数（支持 999+ 格式）
        review_count = 'unknown'
        review_patterns = [
            # 支持加号：评论 999+
            r'评论\s*([0-9]+\+)',
            r'([0-9.]+[万千百十]?)\s*条评论',
            r'([0-9,.]+)\s*条评价',
            r'评论[：:]*\s*([0-9,.]+[万千]?)',
            r'([0-9,.]+[万千]?)\s*人评论'
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
    print('应用宝 - AI竞品监控')
    print('='*70)
    
    # 创建本次运行的文件夹
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    output_dir = Path(f'./logs/yingyongbao/{timestamp}')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f'\n📁 输出目录: {output_dir}')
    
    all_results = []
    
    for app_name, app_url in APPS.items():
        print(f'\n[{app_name}]')
        result = get_yingyongbao_app_info(app_url, app_name, output_dir)
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
