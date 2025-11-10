#!/usr/bin/env python3
"""
测试修复后的功能
"""

import requests
import json
import time

# 测试配置
BASE_URL = "http://localhost:5000"
TEST_SYMBOL = "AAPL"

def test_fixes():
    """测试修复后的功能"""
    print("开始测试修复后的功能...")
    print("=" * 50)
    
    # 测试1: 实时价格显示
    print("1. 测试实时价格显示...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock/{TEST_SYMBOL}")
        data = response.json()
        
        if 'error' in data:
            print(f"   价格获取失败: {data['error']}")
        else:
            print(f"   股票: {data['symbol']}")
            print(f"   价格: ${data['price']}")
            print(f"   涨跌: {data['change']} ({data['change_percent']}%)")
            print("   实时价格显示正常")
    except Exception as e:
        print(f"   价格测试失败: {e}")
        return False
    
    # 测试2: 财务数据缓存
    print("\n2. 测试财务数据缓存...")
    try:
        # 第一次请求
        start_time = time.time()
        response1 = requests.get(f"{BASE_URL}/api/stock/{TEST_SYMBOL}/financials")
        first_time = time.time() - start_time
        
        # 第二次请求（应该使用缓存）
        start_time = time.time()
        response2 = requests.get(f"{BASE_URL}/api/stock/{TEST_SYMBOL}/financials")
        second_time = time.time() - start_time
        
        print(f"   第一次请求时间: {first_time:.2f}秒")
        print(f"   第二次请求时间: {second_time:.2f}秒")
        
        if second_time < first_time:
            print("   缓存机制工作正常")
        else:
            print("   缓存可能未生效")
    except Exception as e:
        print(f"   财务数据测试失败: {e}")
        return False
    
    # 测试3: 成交量数据
    print("\n3. 测试成交量数据...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock/{TEST_SYMBOL}/timeseries")
        data = response.json()
        
        if 'error' in data:
            print(f"   成交量数据获取失败: {data['error']}")
        else:
            print(f"   获取到 {len(data)} 个数据点")
            if len(data) > 0:
                print(f"   最新成交量: {data[-1]['volume']:,}")
                print(f"   最新价格: ${data[-1]['close']}")
            print("   成交量数据获取成功")
    except Exception as e:
        print(f"   成交量数据测试失败: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("所有修复测试完成！")
    print("请在浏览器中查看美化后的界面")
    return True

if __name__ == "__main__":
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    # 运行测试
    success = test_fixes()
    
    if success:
        print("\n修复测试成功！")
    else:
        print("\n修复测试失败，请检查错误信息")

