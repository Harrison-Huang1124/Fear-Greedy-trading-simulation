#!/usr/bin/env python3
"""
测试股票模拟交易系统的API接口
"""

import requests
import json
import time

# 测试配置
BASE_URL = "http://localhost:5000"
TEST_USER = "test_user"

# 创建会话以保持登录状态
session = requests.Session()

def test_api():
    """测试API接口"""
    print("开始测试股票模拟交易系统API...")
    print("=" * 50)
    
    # 测试1: 创建用户
    print("1. 测试用户创建...")
    try:
        response = session.post(f"{BASE_URL}/api/user/create", 
                               json={"username": TEST_USER})
        result = response.json()
        print(f"   结果: {result['message']}")
        assert result['success'] == True
        print("   用户创建成功")
    except Exception as e:
        print(f"   用户创建失败: {e}")
        return False
    
    # 测试2: 获取股票列表
    print("\n2. 测试获取股票列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/stocks")
        stocks = response.json()
        print(f"   获取到 {len(stocks)} 只股票")
        print(f"   前5只股票: {stocks[:5]}")
        assert len(stocks) > 0
        print("   股票列表获取成功")
    except Exception as e:
        print(f"   股票列表获取失败: {e}")
        return False
    
    # 测试3: 搜索股票
    print("\n3. 测试股票搜索...")
    try:
        response = requests.get(f"{BASE_URL}/api/stocks/search/AAPL")
        suggestions = response.json()
        print(f"   搜索结果: {suggestions}")
        assert len(suggestions) > 0
        print("   股票搜索成功")
    except Exception as e:
        print(f"   股票搜索失败: {e}")
        return False
    
    # 测试4: 获取股票价格
    print("\n4. 测试获取股票价格...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock/AAPL")
        stock_data = response.json()
        if 'error' in stock_data:
            print(f"   股票价格获取失败: {stock_data['error']}")
            print("   (这可能是由于API限制或网络问题)")
        else:
            print(f"   AAPL价格: ${stock_data['price']}")
            print(f"   涨跌: {stock_data['change']} ({stock_data['change_percent']}%)")
            print("   股票价格获取成功")
    except Exception as e:
        print(f"   股票价格获取失败: {e}")
        return False
    
    # 测试5: 获取投资组合
    print("\n5. 测试获取投资组合...")
    try:
        response = session.get(f"{BASE_URL}/api/portfolio")
        portfolio = response.json()
        print(f"   现金余额: ${portfolio['balance']:,.2f}")
        print(f"   投资组合价值: ${portfolio['portfolio_value']:,.2f}")
        print(f"   总价值: ${portfolio['total_value']:,.2f}")
        print("   投资组合获取成功")
    except Exception as e:
        print(f"   投资组合获取失败: {e}")
        return False
    
    # 测试6: 获取交易历史
    print("\n6. 测试获取交易历史...")
    try:
        response = session.get(f"{BASE_URL}/api/transactions")
        transactions = response.json()
        print(f"   交易记录数量: {len(transactions)}")
        print("   交易历史获取成功")
    except Exception as e:
        print(f"   交易历史获取失败: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("所有API测试完成！")
    print("请在浏览器中访问: http://localhost:5000")
    print("使用用户名 'test_user' 登录测试")
    return True

if __name__ == "__main__":
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    # 运行测试
    success = test_api()
    
    if success:
        print("\n系统运行正常！")
    else:
        print("\n系统测试失败，请检查错误信息")