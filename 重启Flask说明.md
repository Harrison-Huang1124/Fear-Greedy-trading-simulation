# 如何重启Flask后端

## 🔄 方法1：如果Flask正在运行

### 步骤1：找到并关闭Flask进程

1. **查看Flask窗口**：
   - 找到运行 `python app.py` 的命令提示符窗口
   - 按 `Ctrl + C` 停止Flask服务器

2. **或者使用任务管理器**：
   - 按 `Ctrl + Shift + Esc` 打开任务管理器
   - 找到 `python.exe` 进程
   - 右键点击 → 结束任务

### 步骤2：重新启动Flask

打开新的命令提示符窗口：

```bash
cd D:\ISEF
python app.py
```

应该看到：
```
* Running on http://0.0.0.0:5000
```

## 🔄 方法2：使用批处理脚本（推荐）

### 创建重启脚本

我已经为你创建了 `restart_flask.bat`，双击运行即可！

## 🔄 方法3：快速重启（如果Flask窗口还在）

1. 在运行Flask的命令提示符窗口中
2. 按 `Ctrl + C` 停止
3. 按上箭头键（↑）找到之前的命令
4. 按回车键重新运行

## ✅ 验证Flask是否重启成功

### 方法1：查看Flask窗口输出

应该看到：
```
* Running on http://0.0.0.0:5000
* Debug mode: on
```

### 方法2：测试API

在浏览器访问：
```
http://localhost:5000/api/stocks
```

应该返回股票列表的JSON数据。

### 方法3：检查端口

运行：
```bash
netstat -ano | findstr :5000
```

应该看到端口5000在监听。

## ⚠️ 常见问题

### 问题1：端口被占用

**错误**：`Address already in use`

**解决**：
1. 找到占用端口的进程并关闭
2. 或修改端口（在`app.py`最后一行改为`port=5001`）

### 问题2：找不到python命令

**错误**：`'python' is not recognized`

**解决**：
1. 使用 `python3` 代替 `python`
2. 或使用完整路径：`C:\Python3x\python.exe app.py`

### 问题3：模块未找到

**错误**：`ModuleNotFoundError: No module named 'flask'`

**解决**：
```bash
pip install -r requirements.txt
```

## 💡 提示

- **保持Flask窗口打开**：Flask需要持续运行
- **不要关闭窗口**：关闭窗口会停止Flask
- **使用两个窗口**：一个运行Flask，一个运行React

