#!/usr/bin/env python3
"""
测试新增的分时图和财务数据功能
"""

import requests
import json
import time

# 测试配置
BASE_URL = "http://localhost:5000"
TEST_SYMBOL = "AAPL"

def test_new_features():
    """测试新功能"""
    print("开始测试新增功能...")
    print("=" * 50)
    
    # 测试1: 财务数据API
    print("1. 测试财务数据API...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock/{TEST_SYMBOL}/financials")
        data = response.json()
        
        if 'error' in data:
            print(f"   财务数据获取失败: {data['error']}")
        else:
            print(f"   EPS: {data.get('eps', 'N/A')}")
            print(f"   P/E比率: {data.get('pe_ratio', 'N/A')}")
            print(f"   ROE: {data.get('roe', 'N/A')}")
            print(f"   ROA: {data.get('roa', 'N/A')}")
            print(f"   行业: {data.get('industry', 'N/A')}")
            print("   财务数据获取成功")
    except Exception as e:
        print(f"   财务数据测试失败: {e}")
        return False
    
    # 测试2: 时间序列数据API
    print("\n2. 测试时间序列数据API...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock/{TEST_SYMBOL}/timeseries")
        data = response.json()
        
        if 'error' in data:
            print(f"   时间序列数据获取失败: {data['error']}")
        else:
            print(f"   获取到 {len(data)} 个数据点")
            if len(data) > 0:
                print(f"   最新价格: ${data[-1]['close']}")
                print(f"   时间范围: {data[0]['time']} 到 {data[-1]['time']}")
            print("   时间序列数据获取成功")
    except Exception as e:
        print(f"   时间序列数据测试失败: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("新功能测试完成！")
    print("请在浏览器中测试分时图和财务数据功能")
    return True

if __name__ == "__main__":
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    # 运行测试
    success = test_new_features()
    
    if success:
        print("\n新功能测试成功！")
    else:
        print("\n新功能测试失败，请检查错误信息")

