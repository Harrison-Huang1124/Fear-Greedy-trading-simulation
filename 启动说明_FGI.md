# NeuroTrade FGI Dashboard 启动说明

## ⚠️ 重要：需要同时运行两个服务

### 步骤1：启动Flask后端（必须）

1. 打开**第一个**命令提示符窗口
2. 进入项目目录：
   ```bash
   cd D:\ISEF
   ```
3. 启动Flask服务器：
   ```bash
   python app.py
   ```
4. 应该看到：
   ```
   * Running on http://0.0.0.0:5000
   ```

**⚠️ 不要关闭这个窗口！**

### 步骤2：启动React前端

1. 打开**第二个**命令提示符窗口（保持第一个窗口运行）
2. 进入项目目录：
   ```bash
   cd D:\ISEF
   ```
3. 启动React应用：
   ```bash
   npm start
   ```
   或双击 `start_react.bat`

4. 应该看到：
   ```
   Compiled successfully!
   Local:            http://localhost:3000
   ```

### 步骤3：访问应用

浏览器会自动打开，或手动访问：
- **前端**: http://localhost:3000
- **后端API**: http://localhost:5000

## 🔍 验证服务是否运行

### 检查Flask后端

在浏览器访问：`http://localhost:5000/api/stocks`

应该返回股票列表JSON数据。

### 检查React前端

在浏览器访问：`http://localhost:3000`

应该看到NeuroTrade FGI Dashboard界面。

## ❌ 常见错误：Network Error

### 错误原因

如果看到 "Network Error" 或 "Failed to fetch"，通常是因为：

1. **Flask后端没有运行**（最常见）
   - 解决：确保 `python app.py` 正在运行

2. **端口5000被占用**
   - 解决：关闭占用5000端口的程序，或修改Flask端口

3. **CORS问题**
   - 解决：确保 `app.py` 中有 `CORS(app)`

### 快速诊断

1. **测试后端API**：
   ```bash
   curl http://localhost:5000/api/stocks
   ```
   或在浏览器访问：`http://localhost:5000/api/stocks`

2. **检查端口占用**：
   ```bash
   netstat -ano | findstr :5000
   ```

3. **查看浏览器控制台**（F12）：
   - 查看Network标签页
   - 查看Console标签页的错误信息

## 🛠️ 故障排除

### 问题1：Flask启动失败

**错误**：`ModuleNotFoundError: No module named 'flask'`

**解决**：
```bash
pip install -r requirements.txt
```

### 问题2：React启动失败

**错误**：`Cannot find module 'react'`

**解决**：
```bash
npm install
```

### 问题3：端口被占用

**错误**：`Address already in use`

**解决**：
- Flask：修改 `app.py` 最后一行改为 `app.run(debug=True, host='0.0.0.0', port=5001)`
- React：设置环境变量 `set PORT=3001 && npm start`

### 问题4：API连接失败

**错误**：`Network Error` 或 `CORS error`

**解决**：
1. 确保Flask正在运行
2. 检查 `app.py` 中有 `CORS(app)`
3. 检查防火墙设置
4. 尝试在浏览器直接访问 `http://localhost:5000/api/stocks`

## 📋 完整启动检查清单

- [ ] Python已安装
- [ ] Node.js已安装
- [ ] Flask依赖已安装（`pip install -r requirements.txt`）
- [ ] React依赖已安装（`npm install`）
- [ ] Flask后端正在运行（端口5000）
- [ ] React前端正在运行（端口3000）
- [ ] 浏览器可以访问 `http://localhost:5000/api/stocks`
- [ ] 浏览器可以访问 `http://localhost:3000`

## 🚀 快速启动脚本

### Windows批处理文件

创建 `start_all.bat`：

```batch
@echo off
echo Starting NeuroTrade FGI Dashboard...
echo.

echo Starting Flask backend...
start "Flask Backend" cmd /k "cd /d D:\ISEF && python app.py"

timeout /t 3 /nobreak >nul

echo Starting React frontend...
start "React Frontend" cmd /k "cd /d D:\ISEF && npm start"

echo.
echo Both services are starting...
echo Flask: http://localhost:5000
echo React: http://localhost:3000
echo.
pause
```

然后双击 `start_all.bat` 即可同时启动两个服务。

## 💡 提示

- **保持两个窗口都打开**：Flask和React都需要持续运行
- **先启动Flask**：React需要连接到Flask API
- **检查控制台输出**：错误信息会显示在终端中
- **使用浏览器开发者工具**：F12查看网络请求和错误

## 🆘 仍然无法解决？

1. 检查所有错误信息（终端和浏览器控制台）
2. 确保防火墙没有阻止端口5000和3000
3. 尝试重启计算机
4. 检查是否有杀毒软件阻止Node.js或Python

