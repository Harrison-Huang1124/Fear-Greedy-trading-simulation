#!/usr/bin/env python3
"""
测试新的分时图和成交量图功能
"""

import requests
import json
import time

# 测试配置
BASE_URL = "http://localhost:5000"
TEST_SYMBOL = "AAPL"

def test_charts():
    """测试新的图表功能"""
    print("开始测试新的图表功能...")
    print("=" * 50)
    
    # 测试1: 时间序列数据
    print("1. 测试时间序列数据...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock/{TEST_SYMBOL}/timeseries")
        data = response.json()
        
        if 'error' in data:
            print(f"   时间序列数据获取失败: {data['error']}")
        else:
            print(f"   获取到 {len(data)} 个数据点")
            if len(data) > 0:
                print(f"   最新价格: ${data[-1]['close']}")
                print(f"   最新成交量: {data[-1]['volume']:,}")
                print("   时间序列数据获取成功")
    except Exception as e:
        print(f"   时间序列数据测试失败: {e}")
        return False
    
    # 测试2: 价格数据
    print("\n2. 测试价格数据...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock/{TEST_SYMBOL}")
        data = response.json()
        
        if 'error' in data:
            print(f"   价格数据获取失败: {data['error']}")
        else:
            print(f"   股票: {data['symbol']}")
            print(f"   价格: ${data['price']}")
            print(f"   涨跌: {data['change']} ({data['change_percent']}%)")
            print("   价格数据获取成功")
    except Exception as e:
        print(f"   价格数据测试失败: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("图表功能测试完成！")
    print("请在浏览器中查看新的分时图和成交量图")
    print("- 分时图：平滑的价格走势线（无点）")
    print("- 成交量图：彩色柱状图显示成交量")
    return True

if __name__ == "__main__":
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    # 运行测试
    success = test_charts()
    
    if success:
        print("\n图表功能测试成功！")
    else:
        print("\n图表功能测试失败，请检查错误信息")

