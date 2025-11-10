from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import math

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# Alpha Vantage API配置
ALPHA_VANTAGE_API_KEY = "WHE60OHXDIR1CQT1"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# 用户数据存储（实际应用中应使用数据库）
users = {}
portfolios = {}
transactions = {}

# 数据缓存
financials_cache = {}
price_cache = {}
cache_timeout = 300  # 5分钟缓存

class TradingSimulator:
    def __init__(self):
        self.initial_balance = 100000.0
        
    def get_stock_price(self, symbol):
        """获取实时股票价格（带缓存和模拟数据）"""
        import time
        import random
        
        # 检查缓存
        current_time = time.time()
        if symbol in price_cache:
            cached_data, cache_time = price_cache[symbol]
            if current_time - cache_time < 60:  # 价格数据1分钟缓存
                return cached_data
        
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': ALPHA_VANTAGE_API_KEY
            }
            response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
            data = response.json()
            
            # 检查API限制
            if 'Note' in data or 'Information' in data:
                print(f"API limit reached for {symbol}, using mock data")
                return self._get_mock_price(symbol)
                
            if 'Global Quote' in data:
                quote = data['Global Quote']
                result = {
                    'symbol': symbol,
                    'price': float(quote['05. price']),
                    'change': float(quote['09. change']),
                    'change_percent': float(quote['10. change percent'].replace('%', '')),
                    'volume': int(quote['06. volume']),
                    'high': float(quote['03. high']),
                    'low': float(quote['04. low']),
                    'open': float(quote['02. open']),
                    'previous_close': float(quote['08. previous close'])
                }
                
                # 缓存数据
                price_cache[symbol] = (result, current_time)
                return result
            else:
                print(f"No data found for {symbol}, using mock data")
                return self._get_mock_price(symbol)
        except Exception as e:
            print(f"Error fetching stock price for {symbol}: {e}, using mock data")
            return self._get_mock_price(symbol)
    
    def _get_mock_price(self, symbol):
        """获取模拟价格数据"""
        import random
        import time
        
        # 基础价格（根据股票代码设置不同基础价格）
        base_prices = {
            'AAPL': 250, 'MSFT': 400, 'GOOGL': 150, 'AMZN': 150, 'TSLA': 200,
            'META': 300, 'NVDA': 500, 'META': 300, 'NVDA': 500
        }
        
        base_price = base_prices.get(symbol, 100)
        
        # 添加随机波动
        change_percent = random.uniform(-5, 5)
        price = base_price * (1 + change_percent / 100)
        change = price - base_price
        
        result = {
            'symbol': symbol,
            'price': round(price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'volume': random.randint(1000000, 10000000),
            'high': round(price * 1.02, 2),
            'low': round(price * 0.98, 2),
            'open': round(base_price, 2),
            'previous_close': round(base_price, 2)
        }
        
        # 缓存模拟数据
        price_cache[symbol] = (result, time.time())
        return result
    
    def get_stock_financials(self, symbol):
        """获取股票财务数据（带缓存）"""
        import time
        
        # 检查缓存
        current_time = time.time()
        if symbol in financials_cache:
            cached_data, cache_time = financials_cache[symbol]
            if current_time - cache_time < cache_timeout:
                return cached_data
        
        try:
            # 获取财务比率数据
            params = {
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': ALPHA_VANTAGE_API_KEY
            }
            response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
            data = response.json()
            
            # 检查API限制
            if 'Note' in data or 'Information' in data:
                print(f"API limit reached for financials {symbol}, using mock data")
                return self._get_mock_financials(symbol)
            
            if 'Symbol' in data:
                result = {
                    'symbol': symbol,
                    'eps': self._safe_float(data.get('EPS')),
                    'pe_ratio': self._safe_float(data.get('PERatio')),
                    'peg_ratio': self._safe_float(data.get('PEGRatio')),
                    'roe': self._safe_float(data.get('ReturnOnEquityTTM')),
                    'roa': self._safe_float(data.get('ReturnOnAssetsTTM')),
                    'roi': self._safe_float(data.get('ReturnOnInvestmentCapitalTTM')),
                    'market_cap': data.get('MarketCapitalization'),
                    'dividend_yield': self._safe_float(data.get('DividendYield')),
                    'beta': self._safe_float(data.get('Beta')),
                    'sector': data.get('Sector'),
                    'industry': data.get('Industry'),
                    'description': data.get('Description')
                }
                
                # 缓存数据
                financials_cache[symbol] = (result, current_time)
                return result
            else:
                print(f"No financial data found for {symbol}, using mock data")
                return self._get_mock_financials(symbol)
        except Exception as e:
            print(f"Error fetching financials for {symbol}: {e}, using mock data")
            return self._get_mock_financials(symbol)
    
    def _get_mock_financials(self, symbol):
        """获取模拟财务数据"""
        import random
        import time
        
        # 根据股票代码生成不同的财务数据
        financial_data = {
            'AAPL': {'eps': 6.58, 'pe': 38.34, 'roe': 0.15, 'roa': 0.25, 'beta': 1.2, 'sector': 'Technology', 'industry': 'Consumer Electronics'},
            'MSFT': {'eps': 11.2, 'pe': 35.7, 'roe': 0.18, 'roa': 0.22, 'beta': 0.9, 'sector': 'Technology', 'industry': 'Software'},
            'GOOGL': {'eps': 5.8, 'pe': 25.9, 'roe': 0.12, 'roa': 0.19, 'beta': 1.1, 'sector': 'Technology', 'industry': 'Internet'},
            'AMZN': {'eps': 2.9, 'pe': 45.2, 'roe': 0.08, 'roa': 0.12, 'beta': 1.3, 'sector': 'Consumer Discretionary', 'industry': 'E-commerce'},
            'TSLA': {'eps': 3.2, 'pe': 65.8, 'roe': 0.22, 'roa': 0.15, 'beta': 2.1, 'sector': 'Consumer Discretionary', 'industry': 'Electric Vehicles'},
            'NVDA': {'eps': 4.4, 'pe': 85.2, 'roe': 0.35, 'roa': 0.28, 'beta': 1.8, 'sector': 'Technology', 'industry': 'Semiconductors'}
        }
        
        # 获取基础数据或使用默认值
        base_data = financial_data.get(symbol, {
            'eps': 3.5, 'pe': 25.0, 'roe': 0.12, 'roa': 0.18, 'beta': 1.0, 
            'sector': 'Technology', 'industry': 'General'
        })
        
        # 添加随机波动
        result = {
            'symbol': symbol,
            'eps': round(base_data['eps'] * random.uniform(0.9, 1.1), 2),
            'pe_ratio': round(base_data['pe'] * random.uniform(0.95, 1.05), 2),
            'peg_ratio': round(random.uniform(0.8, 2.5), 2),
            'roe': round(base_data['roe'] * random.uniform(0.9, 1.1), 3),
            'roa': round(base_data['roa'] * random.uniform(0.9, 1.1), 3),
            'roi': round(base_data['roe'] * random.uniform(0.8, 1.2), 3),
            'market_cap': f"${random.randint(100, 3000)}B",
            'dividend_yield': round(random.uniform(0.01, 0.05), 3),
            'beta': round(base_data['beta'] * random.uniform(0.95, 1.05), 2),
            'sector': base_data['sector'],
            'industry': base_data['industry'],
            'description': f"{symbol} is a leading company in the {base_data['industry']} industry, operating in the {base_data['sector']} sector."
        }
        
        # 缓存模拟数据
        financials_cache[symbol] = (result, time.time())
        return result
    
    def _safe_float(self, value):
        """安全转换为浮点数"""
        if value is None or value == 'None' or value == '-':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def get_stock_time_series(self, symbol):
        """获取股票时间序列数据（用于分时图）"""
        try:
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': symbol,
                'interval': '5min',
                'apikey': ALPHA_VANTAGE_API_KEY
            }
            response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
            data = response.json()
            
            # 检查API限制
            if 'Note' in data or 'Information' in data:
                print(f"API limit reached for time series {symbol}, using mock data")
                return self._get_mock_time_series(symbol)
            
            if 'Time Series (5min)' in data:
                time_series = data['Time Series (5min)']
                # 获取最近24小时的数据
                sorted_times = sorted(time_series.keys(), reverse=True)[:288]  # 24小时 * 12个5分钟间隔
                
                chart_data = []
                for timestamp in sorted_times:
                    values = time_series[timestamp]
                    chart_data.append({
                        'time': timestamp,
                        'open': float(values['1. open']),
                        'high': float(values['2. high']),
                        'low': float(values['3. low']),
                        'close': float(values['4. close']),
                        'volume': int(values['5. volume'])
                    })
                
                return sorted(chart_data, key=lambda x: x['time'])
            else:
                print(f"No time series data found for {symbol}, using mock data")
                return self._get_mock_time_series(symbol)
        except Exception as e:
            print(f"Error fetching time series for {symbol}: {e}, using mock data")
            return self._get_mock_time_series(symbol)
    
    def _get_mock_time_series(self, symbol):
        """获取模拟时间序列数据"""
        import random
        from datetime import datetime, timedelta
        
        # 获取基础价格
        base_prices = {
            'AAPL': 250, 'MSFT': 400, 'GOOGL': 150, 'AMZN': 150, 'TSLA': 200,
            'META': 300, 'NVDA': 500
        }
        base_price = base_prices.get(symbol, 100)
        
        # 生成最近24小时的数据（每5分钟一个点）
        chart_data = []
        current_time = datetime.now()
        
        for i in range(100):  # 生成100个数据点
            timestamp = current_time - timedelta(minutes=5*i)
            
            # 价格随机波动
            price_change = random.uniform(-0.02, 0.02)  # ±2%波动
            price = base_price * (1 + price_change)
            
            # 生成OHLC数据
            open_price = price
            close_price = price * random.uniform(0.98, 1.02)
            high_price = max(open_price, close_price) * random.uniform(1.0, 1.01)
            low_price = min(open_price, close_price) * random.uniform(0.99, 1.0)
            
            chart_data.append({
                'time': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': random.randint(100000, 2000000)
            })
        
        return sorted(chart_data, key=lambda x: x['time'])
    
    def get_sp500_stocks(self):
        """获取标普500股票列表"""
        # 完整的标普500股票列表（前100只主要股票）
        return [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK.B',
            'UNH', 'JNJ', 'JPM', 'V', 'PG', 'HD', 'MA', 'DIS', 'PYPL', 'ADBE',
            'NFLX', 'CRM', 'INTC', 'CMCSA', 'PFE', 'ABT', 'TMO', 'COST', 'PEP',
            'WMT', 'MRK', 'ACN', 'CSCO', 'ABBV', 'VZ', 'TXN', 'NKE', 'QCOM',
            'CVX', 'DHR', 'LLY', 'T', 'AVGO', 'UNP', 'AMGN', 'PM', 'HON',
            'IBM', 'LOW', 'SPGI', 'INTU', 'CAT', 'AXP', 'GS', 'BA', 'RTX',
            'MMM', 'GE', 'BKNG', 'AMD', 'ISRG', 'GILD', 'BLK', 'SYK', 'ZTS',
            'ADP', 'TGT', 'LMT', 'SO', 'MO', 'CL', 'KO', 'WBA', 'CVS', 'MDT',
            'AMT', 'ELV', 'CI', 'PLD', 'DUK', 'EQIX', 'ICE', 'AON', 'SHW',
            'ITW', 'FIS', 'EMR', 'PSA', 'BDX', 'A', 'KLAC', 'APH', 'EW',
            'ETN', 'ROST', 'NSC', 'AEP', 'CTAS', 'MCO', 'CME', 'IDXX', 'EXC',
            'MRNA', 'SRE', 'PAYX', 'YUM', 'CHTR', 'ALL', 'NOC', 'AFL', 'CTSH',
            'ROK', 'EA', 'VRSK', 'ODFL', 'MCHP', 'FAST', 'LHX', 'WEC', 'FTNT',
            'CDNS', 'CPRT', 'XEL', 'IEX', 'HSY', 'TTWO', 'WAB', 'MTD', 'BIIB',
            'DXCM', 'ZBRA', 'ANSS', 'CHD', 'CINF', 'BRO', 'EXR', 'FANG', 'GRMN',
            'HOLX', 'IFF', 'JKHY', 'KEYS', 'LRCX', 'MKTX', 'NDSN', 'NTAP', 'PKI',
            'QRVO', 'RMD', 'SNPS', 'SWKS', 'TEL', 'TER', 'TMO', 'TRMB', 'TYL',
            'VRTX', 'WAT', 'WST', 'ZEN', 'ZTS'
        ]
    
    def create_user(self, username):
        """创建新用户"""
        if username not in users:
            users[username] = {
                'balance': self.initial_balance,
                'created_at': datetime.now().isoformat()
            }
            portfolios[username] = {}
            transactions[username] = []
            return True
        return False
    
    def buy_stock(self, username, symbol, quantity):
        """买入股票"""
        if username not in users:
            return {'success': False, 'message': '用户不存在'}
        
        # 获取当前股价
        stock_data = self.get_stock_price(symbol)
        if not stock_data:
            return {'success': False, 'message': '无法获取股票价格'}
        
        price = stock_data['price']
        total_cost = price * quantity
        
        if users[username]['balance'] < total_cost:
            return {'success': False, 'message': '余额不足'}
        
        # 执行交易
        users[username]['balance'] -= total_cost
        
        if symbol in portfolios[username]:
            portfolios[username][symbol]['quantity'] += quantity
            portfolios[username][symbol]['avg_price'] = (
                (portfolios[username][symbol]['avg_price'] * (portfolios[username][symbol]['quantity'] - quantity) + total_cost) / 
                portfolios[username][symbol]['quantity']
            )
        else:
            portfolios[username][symbol] = {
                'quantity': quantity,
                'avg_price': price
            }
        
        # 记录交易
        transaction = {
            'id': len(transactions[username]) + 1,
            'type': 'BUY',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_cost,
            'timestamp': datetime.now().isoformat()
        }
        transactions[username].append(transaction)
        
        return {'success': True, 'message': f'成功买入 {quantity} 股 {symbol}', 'transaction': transaction}
    
    def sell_stock(self, username, symbol, quantity):
        """卖出股票"""
        if username not in users:
            return {'success': False, 'message': '用户不存在'}
        
        if symbol not in portfolios[username] or portfolios[username][symbol]['quantity'] < quantity:
            return {'success': False, 'message': '股票数量不足'}
        
        # 获取当前股价
        stock_data = self.get_stock_price(symbol)
        if not stock_data:
            return {'success': False, 'message': '无法获取股票价格'}
        
        price = stock_data['price']
        total_value = price * quantity
        
        # 执行交易
        users[username]['balance'] += total_value
        portfolios[username][symbol]['quantity'] -= quantity
        
        if portfolios[username][symbol]['quantity'] == 0:
            del portfolios[username][symbol]
        
        # 记录交易
        transaction = {
            'id': len(transactions[username]) + 1,
            'type': 'SELL',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_value,
            'timestamp': datetime.now().isoformat()
        }
        transactions[username].append(transaction)
        
        return {'success': True, 'message': f'成功卖出 {quantity} 股 {symbol}', 'transaction': transaction}
    
    def get_portfolio(self, username):
        """获取投资组合"""
        if username not in users:
            return None
        
        portfolio_value = 0
        portfolio_details = []
        
        for symbol, holding in portfolios[username].items():
            stock_data = self.get_stock_price(symbol)
            if stock_data:
                current_price = stock_data['price']
                current_value = current_price * holding['quantity']
                portfolio_value += current_value
                
                gain_loss = current_value - (holding['avg_price'] * holding['quantity'])
                gain_loss_percent = (gain_loss / (holding['avg_price'] * holding['quantity'])) * 100
                
                portfolio_details.append({
                    'symbol': symbol,
                    'quantity': holding['quantity'],
                    'avg_price': holding['avg_price'],
                    'current_price': current_price,
                    'current_value': current_value,
                    'gain_loss': gain_loss,
                    'gain_loss_percent': gain_loss_percent
                })
        
        total_value = users[username]['balance'] + portfolio_value
        total_return = total_value - self.initial_balance
        total_return_percent = (total_return / self.initial_balance) * 100
        
        return {
            'balance': users[username]['balance'],
            'portfolio_value': portfolio_value,
            'total_value': total_value,
            'total_return': total_return,
            'total_return_percent': total_return_percent,
            'holdings': portfolio_details
        }

# 初始化交易模拟器
simulator = TradingSimulator()

# FGI Calculation Constants
K_P = 2.5  # Price momentum constant
K_O = 2.0  # Order momentum constant
K_V = 1.5  # Volatility constant

class FGICalculator:
    """Fear & Greed Index Calculator"""
    
    @staticmethod
    def calculate_ema(data, period):
        """Calculate Exponential Moving Average"""
        if len(data) == 0:
            return []
        
        multiplier = 2 / (period + 1)
        ema = []
        
        # Start with SMA for first value
        sum_val = sum(data[:min(period, len(data))])
        ema.append(sum_val / min(period, len(data)))
        
        # Calculate EMA for remaining values
        for i in range(1, len(data)):
            value = data[i]
            prev_ema = ema[i - 1]
            new_ema = (value - prev_ema) * multiplier + prev_ema
            ema.append(new_ema)
        
        return ema
    
    @staticmethod
    def calculate_log_returns(prices):
        """Calculate log returns"""
        returns = []
        for i in range(1, len(prices)):
            if prices[i - 1] > 0:
                returns.append(math.log(prices[i] / prices[i - 1]))
            else:
                returns.append(0)
        return returns
    
    @staticmethod
    def calculate_rolling_std(data, window=20):
        """Calculate rolling standard deviation"""
        if len(data) == 0:
            return []
        
        stds = []
        for i in range(len(data)):
            start = max(0, i - window + 1)
            window_data = data[start:i + 1]
            
            if len(window_data) < 2:
                stds.append(0)
                continue
            
            mean = sum(window_data) / len(window_data)
            variance = sum((x - mean) ** 2 for x in window_data) / len(window_data)
            std = math.sqrt(variance)
            
            # Annualize (assuming 252 trading days)
            annualized_std = std * math.sqrt(252)
            stds.append(annualized_std)
        
        return stds
    
    @staticmethod
    def simulate_order_imbalance(prices):
        """Simulate order imbalance from price changes"""
        imbalance = [0]
        for i in range(1, len(prices)):
            price_change = (prices[i] - prices[i - 1]) / prices[i - 1] if prices[i - 1] > 0 else 0
            noise = (np.random.random() - 0.5) * 0.1
            imbalance.append(price_change * 100 + noise)
        return imbalance
    
    @staticmethod
    def calculate_price_momentum(prices, short_period=12, long_period=26):
        """Calculate Price Momentum (PM_t)"""
        if len(prices) < long_period:
            return []
        
        ema_short = FGICalculator.calculate_ema(prices, short_period)
        ema_long = FGICalculator.calculate_ema(prices, long_period)
        
        pm = []
        min_len = min(len(ema_short), len(ema_long))
        for i in range(min_len):
            if ema_long[i] > 0:
                pm.append((ema_short[i] - ema_long[i]) / ema_long[i])
            else:
                pm.append(0)
        
        return pm
    
    @staticmethod
    def calculate_order_momentum(prices, short_period=12, long_period=26):
        """Calculate Order Momentum (OM_t)"""
        if len(prices) < long_period:
            return []
        
        order_imbalance = FGICalculator.simulate_order_imbalance(prices)
        ema_short = FGICalculator.calculate_ema(order_imbalance, short_period)
        ema_long = FGICalculator.calculate_ema(order_imbalance, long_period)
        
        om = []
        min_len = min(len(ema_short), len(ema_long))
        for i in range(min_len):
            om.append(ema_short[i] - ema_long[i])
        
        return om
    
    @staticmethod
    def calculate_volatility(prices, window=20):
        """Calculate Volatility (Vol_t)"""
        log_returns = FGICalculator.calculate_log_returns(prices)
        volatility = FGICalculator.calculate_rolling_std(log_returns, window)
        
        # Pad with first value to match prices length
        if len(volatility) > 0:
            volatility.insert(0, volatility[0] if len(volatility) > 0 else 0)
        
        # Calculate mean volatility
        valid_vols = [v for v in volatility if v > 0]
        mean_vol = sum(valid_vols) / len(valid_vols) if len(valid_vols) > 0 else 0.2
        
        return {
            'volatility': volatility,
            'mean_vol': mean_vol
        }
    
    @staticmethod
    def calculate_fear_index(pm, om, vol, mean_vol):
        """Calculate Fear Index (FI_t)"""
        sigmoid_pm = 1 / (1 + math.exp(K_P * pm))
        sigmoid_om = 1 / (1 + math.exp(K_O * om))
        sigmoid_vol = 1 / (1 + math.exp(-K_V * (vol - mean_vol)))
        return 100 * sigmoid_pm * sigmoid_om * sigmoid_vol
    
    @staticmethod
    def calculate_greed_index(pm, om, vol, mean_vol):
        """Calculate Greed Index (GI_t)"""
        sigmoid_pm = 1 / (1 + math.exp(-K_P * pm))
        sigmoid_om = 1 / (1 + math.exp(-K_O * om))
        sigmoid_vol = 1 / (1 + math.exp(K_V * (vol - mean_vol)))
        return 100 * sigmoid_pm * sigmoid_om * sigmoid_vol
    
    @staticmethod
    def calculate_fgi(prices, short_period=12, long_period=26, vol_window=20):
        """Calculate complete FGI metrics"""
        if len(prices) < long_period:
            return None
        
        pm = FGICalculator.calculate_price_momentum(prices, short_period, long_period)
        om = FGICalculator.calculate_order_momentum(prices, short_period, long_period)
        vol_data = FGICalculator.calculate_volatility(prices, vol_window)
        volatility = vol_data['volatility']
        mean_vol = vol_data['mean_vol']
        
        # Align arrays
        min_length = min(len(pm), len(om), len(volatility))
        
        fi = []
        gi = []
        
        for i in range(min_length):
            pm_val = pm[i] if i < len(pm) else 0
            om_val = om[i] if i < len(om) else 0
            vol_val = volatility[i] if i < len(volatility) else mean_vol
            
            fi.append(FGICalculator.calculate_fear_index(pm_val, om_val, vol_val, mean_vol))
            gi.append(FGICalculator.calculate_greed_index(pm_val, om_val, vol_val, mean_vol))
        
        return {
            'pm': pm[:min_length],
            'om': om[:min_length],
            'volatility': volatility[:min_length],
            'mean_vol': mean_vol,
            'fi': fi,
            'gi': gi
        }

# Initialize FGI Calculator
fgi_calculator = FGICalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    """获取股票列表"""
    stocks = simulator.get_sp500_stocks()
    return jsonify(stocks)

@app.route('/api/stocks/search/<query>')
def search_stocks(query):
    """搜索股票"""
    all_stocks = simulator.get_sp500_stocks()
    query = query.upper()
    matching_stocks = [stock for stock in all_stocks if query in stock]
    return jsonify(matching_stocks[:10])  # 返回前10个匹配结果

@app.route('/api/stock/<symbol>')
def get_stock_price(symbol):
    """获取股票价格"""
    try:
        price_data = simulator.get_stock_price(symbol)
        if price_data:
            # Check if this is real data or mock data
            # Real data will have recent timestamp in cache
            is_real = False
            if symbol in price_cache:
                cached_data, cache_time = price_cache[symbol]
                # If cached within last 5 minutes and has realistic price, likely real
                import time
                if time.time() - cache_time < 300:
                    # Check if price is realistic (not just base price with random)
                    if 'change' in price_data and abs(price_data.get('change', 0)) < 1000:
                        is_real = True
            
            price_data['is_real_data'] = is_real
            return jsonify(price_data)
        else:
            return jsonify({'error': '无法获取股票价格'}), 400
    except Exception as e:
        print(f"Error in get_stock_price: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<symbol>/financials')
def get_stock_financials(symbol):
    """获取股票财务数据"""
    financials = simulator.get_stock_financials(symbol)
    if financials:
        return jsonify(financials)
    else:
        return jsonify({'error': '无法获取财务数据'}), 400

@app.route('/api/stock/<symbol>/timeseries')
def get_stock_timeseries(symbol):
    """获取股票时间序列数据"""
    try:
        timeseries = simulator.get_stock_time_series(symbol)
        if timeseries and len(timeseries) > 0:
            # Add metadata to indicate if data is real or simulated
            # Check if first item has realistic timestamp (not just generated)
            first_item = timeseries[0]
            is_real = 'time' in first_item and len(first_item.get('time', '')) > 10
            
            return jsonify({
                'data': timeseries,
                'is_real_data': is_real,
                'count': len(timeseries),
                'symbol': symbol
            })
        else:
            return jsonify({'error': '无法获取时间序列数据', 'data': []}), 400
    except Exception as e:
        print(f"Error in get_stock_timeseries: {e}")
        return jsonify({'error': str(e), 'data': []}), 500

@app.route('/api/user/create', methods=['POST'])
def create_user():
    """创建用户"""
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': '用户名不能为空'}), 400
    
    success = simulator.create_user(username)
    if success:
        session['username'] = username
        return jsonify({'success': True, 'message': '用户创建成功'})
    else:
        return jsonify({'success': False, 'message': '用户名已存在'}), 400

@app.route('/api/user/login', methods=['POST'])
def login_user():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    
    if username in users:
        session['username'] = username
        return jsonify({'success': True, 'message': '登录成功'})
    else:
        return jsonify({'success': False, 'message': '用户不存在'}), 400

@app.route('/api/trade/buy', methods=['POST'])
def buy_stock():
    """买入股票"""
    if 'username' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    
    data = request.get_json()
    symbol = data.get('symbol')
    quantity = int(data.get('quantity', 0))
    
    if not symbol or quantity <= 0:
        return jsonify({'success': False, 'message': '参数错误'}), 400
    
    result = simulator.buy_stock(session['username'], symbol, quantity)
    return jsonify(result)

@app.route('/api/trade/sell', methods=['POST'])
def sell_stock():
    """卖出股票"""
    if 'username' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    
    data = request.get_json()
    symbol = data.get('symbol')
    quantity = int(data.get('quantity', 0))
    
    if not symbol or quantity <= 0:
        return jsonify({'success': False, 'message': '参数错误'}), 400
    
    result = simulator.sell_stock(session['username'], symbol, quantity)
    return jsonify(result)

@app.route('/api/portfolio')
def get_portfolio():
    """获取投资组合"""
    if 'username' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    
    portfolio = simulator.get_portfolio(session['username'])
    return jsonify(portfolio)

@app.route('/api/transactions')
def get_transactions():
    """获取交易历史"""
    if 'username' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    
    user_transactions = transactions.get(session['username'], [])
    return jsonify(user_transactions)

@app.route('/api/stock/<symbol>/fgi')
def get_stock_fgi(symbol):
    """获取股票的Fear & Greed Index数据"""
    try:
        # Get time series data
        timeseries = simulator.get_stock_time_series(symbol)
        if not timeseries or len(timeseries) == 0:
            return jsonify({'error': '无法获取时间序列数据'}), 400
        
        # Extract prices
        prices = [float(item['close']) for item in timeseries if 'close' in item]
        
        if len(prices) < 26:
            return jsonify({'error': '数据点不足，需要至少26个数据点'}), 400
        
        # Calculate FGI
        fgi_data = fgi_calculator.calculate_fgi(prices)
        
        if not fgi_data:
            return jsonify({'error': 'FGI计算失败'}), 400
        
        return jsonify(fgi_data)
    except Exception as e:
        print(f"Error calculating FGI for {symbol}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/fgi-dashboard')
def fgi_dashboard():
    """FGI Dashboard页面（用于开发环境，生产环境应使用React build）"""
    return render_template('fgi_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)