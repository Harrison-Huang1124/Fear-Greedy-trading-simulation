# API修复说明 - 真实数据支持

## ✅ 已修复的问题

### 1. 当前价格获取
- ✅ 现在会**首先获取实时价格**（通过 `/api/stock/<symbol>`）
- ✅ 确保显示的当前价格是真实的
- ✅ 如果API失败，会明确提示使用模拟数据

### 2. 时间序列数据
- ✅ 优先使用真实的时间序列数据
- ✅ API返回时会标记是否为真实数据
- ✅ 前端会正确处理新的响应格式

### 3. 数据一致性
- ✅ 当前价格和时间序列数据现在保持一致
- ✅ 如果获取到真实价格，会作为基础价格使用
- ✅ 图表数据会基于真实价格

## 🔍 如何验证使用真实数据

### 方法1：查看浏览器控制台

打开浏览器开发者工具（F12），查看Console标签页：

**真实数据**：
```
[真实数据] TSLA 当前价格: $245.67
[真实数据] 获取到 100 个时间序列数据点
[数据源] 使用真实数据 (real)
```

**模拟数据**：
```
[数据源] 使用模拟数据 (simulated) - API可能不可用
```

### 方法2：检查价格显示

- ✅ **真实数据**：价格旁边有绿色闪烁点，显示"实时数据"
- ⚠️ **模拟数据**：没有绿色点，价格可能是固定的基础价格

### 方法3：测试API端点

在浏览器访问：
```
http://localhost:5000/api/stock/TSLA
```

应该返回：
```json
{
  "symbol": "TSLA",
  "price": 245.67,
  "change": 2.34,
  "change_percent": 0.96,
  "is_real_data": true,
  ...
}
```

## ⚠️ 可能的问题

### 问题1：Alpha Vantage API限制

**症状**：总是使用模拟数据

**原因**：
- 免费版API有调用限制（每天500次）
- 可能已达到限制

**解决**：
1. 等待24小时后重试
2. 或使用自己的API密钥（在`app.py`中修改`ALPHA_VANTAGE_API_KEY`）

### 问题2：市场关闭时间

**症状**：获取不到最新数据

**原因**：
- 股票市场在非交易时间不更新
- 数据可能有15-20分钟延迟（免费版）

**解决**：
- 这是正常的，免费API有延迟
- 在交易时间内使用会获得最新数据

### 问题3：网络问题

**症状**：Network Error

**解决**：
1. 确保Flask后端正在运行
2. 检查网络连接
3. 查看Flask终端的错误信息

## 📊 数据流程

```
用户输入股票代码 (如 TSLA)
    ↓
1. 获取实时价格 (/api/stock/TSLA)
   - 从Alpha Vantage获取
   - 如果失败，使用模拟数据
    ↓
2. 获取时间序列 (/api/stock/TSLA/timeseries)
   - 从Alpha Vantage获取5分钟K线
   - 如果失败，基于真实价格生成模拟数据
    ↓
3. 计算FGI指标
   - 基于价格数据计算
   - 显示在图表上
    ↓
4. 显示结果
   - 当前价格（真实或模拟）
   - 价格图表
   - FGI图表
```

## 🛠️ 调试技巧

### 查看Flask日志

在Flask终端窗口查看：
- `API limit reached` - API达到限制
- `using mock data` - 使用模拟数据
- `Error fetching` - 获取数据出错

### 查看浏览器Network标签

1. 按F12打开开发者工具
2. 切换到Network标签
3. 刷新页面
4. 查看API请求：
   - `/api/stock/TSLA` - 实时价格
   - `/api/stock/TSLA/timeseries` - 时间序列
5. 点击请求查看响应数据

### 测试API直接调用

在浏览器或使用curl：
```bash
# 测试实时价格
curl http://localhost:5000/api/stock/TSLA

# 测试时间序列
curl http://localhost:5000/api/stock/TSLA/timeseries
```

## 💡 改进建议

如果经常遇到API限制，可以考虑：

1. **使用自己的API密钥**：
   - 注册Alpha Vantage账号
   - 获取免费API密钥
   - 修改`app.py`中的`ALPHA_VANTAGE_API_KEY`

2. **添加数据缓存**：
   - 已实现1分钟缓存
   - 可以减少API调用

3. **使用其他数据源**：
   - Yahoo Finance API
   - IEX Cloud
   - Polygon.io

## ✅ 验证清单

- [ ] Flask后端正在运行
- [ ] 可以访问 `http://localhost:5000/api/stock/TSLA`
- [ ] 浏览器控制台显示"[真实数据]"
- [ ] 当前价格显示正确
- [ ] 价格图表显示真实数据
- [ ] 没有Network Error

如果所有项目都打勾，说明正在使用真实数据！🎉

