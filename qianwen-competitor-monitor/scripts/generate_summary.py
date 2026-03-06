#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime

def get_latest_summary(platform_dir):
    """获取指定平台最新的 summary.json"""
    platform_path = Path(platform_dir)
    
    if not platform_path.exists():
        return None
    
    # 获取所有时间戳文件夹
    timestamp_dirs = [d for d in platform_path.iterdir() if d.is_dir()]
    
    if not timestamp_dirs:
        return None
    
    # 按时间排序，获取最新的
    latest_dir = sorted(timestamp_dirs, key=lambda x: x.name, reverse=True)[0]
    summary_file = latest_dir / 'summary.json'
    
    if summary_file.exists():
        with open(summary_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            if isinstance(data, dict) and 'apps' in data:
                apps_data = data['apps']
            elif isinstance(data, list):
                apps_data = data
            else:
                return None
            
            return {
                'platform': platform_path.name,
                'timestamp': latest_dir.name,
                'data': apps_data
            }
    
    return None

def generate_summary_report():
    """生成汇总报告"""
    print('='*70)
    print('AI竞品监控 - 数据汇总')
    print('='*70)
    
    # 读取两个平台的最新数据
    platforms = ['huawei', 'yingyongbao']
    all_data = {}
    
    for platform in platforms:
        platform_dir = Path(f'./logs/{platform}')
        summary = get_latest_summary(platform_dir)
        
        if summary:
            all_data[platform] = summary
            print(f'\n✅ {platform:15s} - 最新数据: {summary["timestamp"]}')
        else:
            print(f'\n⚠️  {platform:15s} - 未找到数据')
    
    if not all_data:
        print('\n❌ 没有找到任何平台的数据')
        return
    
    # 构建汇总结构
    summary_report = {
        'generated_at': datetime.now().isoformat(),
        'platforms': {}
    }
    
    # 按应用名称组织数据
    app_names = set()
    for platform_data in all_data.values():
        for app in platform_data['data']:
            app_names.add(app['app_name'])
    
    # 为每个应用收集各平台数据
    for app_name in sorted(app_names):
        summary_report['platforms'][app_name] = {}
        
        for platform, platform_data in all_data.items():
            # 查找该应用在当前平台的数据
            app_data = next((app for app in platform_data['data'] if app['app_name'] == app_name), None)
            
            if app_data:
                summary_report['platforms'][app_name][platform] = {
                    'download_count': app_data.get('download_count', 'unknown'),
                    'rating': app_data.get('rating', 'unknown'),
                    'review_count': app_data.get('review_count', 'unknown'),
                    'url': app_data.get('url', ''),
                    'timestamp': platform_data['timestamp']
                }
            else:
                summary_report['platforms'][app_name][platform] = {
                    'download_count': 'not_found',
                    'rating': 'not_found',
                    'review_count': 'not_found',
                    'url': '',
                    'timestamp': platform_data['timestamp']
                }
    
    # 保存汇总报告（JSON格式）
    output_file = Path('./logs/summary_report.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_report, f, ensure_ascii=False, indent=2)
    
    print(f'\n{"="*70}')
    print('汇总报告')
    print('='*70)
    
    # 按平台分组显示（两个独立表格）
    platforms_config = [
        ('huawei', '华为应用市场'),
        ('yingyongbao', '应用宝')
    ]
    
    for platform_key, platform_name in platforms_config:
        print(f'\n## {platform_name}')
        print(f'{"应用":15s} | {"下载量":15s} | {"评分":8s} | {"评论数":10s} | {"采集时间":20s}')
        print('-'*85)
        
        for app_name in sorted(app_names):
            app_data = summary_report['platforms'][app_name]
            
            if platform_key in app_data:
                data = app_data[platform_key]
                download = str(data.get('download_count', 'unknown'))
                rating = str(data.get('rating', 'unknown'))
                review = str(data.get('review_count', 'unknown'))
                timestamp = data.get('timestamp', 'unknown')
            else:
                download = 'not_found'
                rating = 'not_found'
                review = 'not_found'
                timestamp = 'not_found'
            
            print(f'{app_name:15s} | {download:15s} | {rating:8s} | {review:10s} | {timestamp:20s}')
    
    print(f'\n{"="*70}')
    print(f'✅ 汇总报告已保存: {output_file}')
    print(f'   生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

if __name__ == '__main__':
    generate_summary_report()

