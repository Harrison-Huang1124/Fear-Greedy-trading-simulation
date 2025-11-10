# Network Error 快速修复指南

## 🔴 问题：显示 Network Error

这通常意味着 **Flask 后端没有运行**！

## ✅ 立即解决方案

### 方法1：使用一键启动脚本（推荐）

双击运行 `start_all.bat`，它会自动：
1. 检查依赖
2. 启动Flask后端
3. 启动React前端

### 方法2：手动启动（分步操作）

#### 步骤1：启动Flask后端（必须！）

1. 打开**命令提示符**（CMD）
2. 进入项目目录：
   ```bash
   cd D:\ISEF
   ```
3. 启动Flask：
   ```bash
   python app.py
   ```
4. 应该看到：
   ```
   * Running on http://0.0.0.0:5000
   ```
5. **保持这个窗口打开！**

#### 步骤2：启动React前端

1. 打开**另一个**命令提示符窗口
2. 进入项目目录：
   ```bash
   cd D:\ISEF
   ```
3. 启动React：
   ```bash
   npm start
   ```
4. 等待编译完成

#### 步骤3：验证

1. 测试Flask API：
   - 在浏览器访问：`http://localhost:5000/api/stocks`
   - 应该看到JSON格式的股票列表

2. 访问React应用：
   - 浏览器会自动打开，或手动访问：`http://localhost:3000`

## 🔍 诊断步骤

### 检查1：Flask是否运行？

在浏览器访问：`http://localhost:5000/api/stocks`

- ✅ **能访问**：Flask正常运行
- ❌ **无法访问**：Flask未运行，需要启动

### 检查2：端口是否被占用？

```bash
netstat -ano | findstr :5000
```

如果有输出，说明端口被占用。

### 检查3：查看浏览器控制台

1. 按 `F12` 打开开发者工具
2. 查看 **Console** 标签页的错误信息
3. 查看 **Network** 标签页，检查哪些请求失败了

## 🛠️ 常见问题修复

### 问题1：Flask启动失败

**错误**：`ModuleNotFoundError: No module named 'flask'`

**解决**：
```bash
pip install -r requirements.txt
```

### 问题2：端口5000被占用

**解决**：修改 `app.py` 最后一行：
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 改为5001
```

然后修改 `src/api/fetchData.js`：
```javascript
const API_BASE_URL = 'http://localhost:5001';  // 改为5001
```

### 问题3：CORS错误

**检查**：确保 `app.py` 中有：
```python
from flask_cors import CORS
CORS(app)
```

### 问题4：API请求超时

**解决**：
1. 检查防火墙设置
2. 检查杀毒软件是否阻止
3. 尝试重启计算机

## 💡 代码已更新

我已经更新了代码，现在即使Flask未运行，应用也会：
- 显示友好的错误提示
- 使用模拟数据作为fallback（如果API失败）
- 在High-Frequency模式下完全使用客户端模拟数据

## 📋 完整检查清单

- [ ] Flask后端正在运行（`python app.py`）
- [ ] 可以在浏览器访问 `http://localhost:5000/api/stocks`
- [ ] React前端正在运行（`npm start`）
- [ ] 浏览器可以访问 `http://localhost:3000`
- [ ] 没有防火墙阻止端口5000和3000

## 🚀 快速测试

运行这个命令测试Flask：

```bash
python -c "import requests; print(requests.get('http://localhost:5000/api/stocks').json())"
```

如果成功，会显示股票列表。

## 🆘 仍然无法解决？

1. **查看Flask窗口的错误信息**
2. **查看React窗口的错误信息**
3. **查看浏览器控制台（F12）的错误信息**
4. **确保两个服务都在运行**

记住：**必须同时运行Flask和React两个服务！**

