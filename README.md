# AI 翻译助手

FastAPI 后端 + Flutter 前端的中文到英文翻译小助手，调用阿里云 DashScope（OpenAI 兼容接口）。

## 目录
- backend：FastAPI 服务
- frontend：Flutter 客户端
- docs/AI_USAGE.md：AI 使用记录模板

## 前置条件
- Python 3.10+
- Flutter SDK（已配置 Android 模拟器或桌面/Web 开发环境）
- DashScope API Key（环境变量 `DASHSCOPE_API_KEY` 或 `backend/.env`）

## 后端运行
1. 进入后端目录并安装依赖：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
2. 配置环境变量（任选其一）：
   - 在系统环境变量里设置 `DASHSCOPE_API_KEY`。
   - 或复制 `.env` 模板：
     ```bash
     cp .env.example .env
     # 编辑 .env 写入 DASHSCOPE_API_KEY=你的密钥
     ```
3. 启动服务（默认端口 8000）：
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
4. 健康检查：`curl http://127.0.0.1:8000/health`
5. 翻译接口示例：
   ```bash
   curl -X POST http://127.0.0.1:8000/translate \
     -H "Content-Type: application/json" \
     -d '{"text": "今天天气很好"}'
   ```

## 前端运行（Flutter）
1. 安装依赖：
   ```bash
   cd frontend
   flutter pub get
   ```
2. 确认后端地址：`frontend/lib/main.dart` 的 `backendBaseUrl` 常量注释说明：
   - Android 模拟器：`http://10.0.2.2:8000`
   - 桌面 / 浏览器调试：`http://127.0.0.1:8000`
   - 真机：改为宿主机的局域网 IP，例如 `http://192.168.x.x:8000`
3. 运行：
   - Android 模拟器：`flutter run -d emulator-id`
   - Flutter Web：`flutter run -d chrome`
   - 桌面（如 Windows）：`flutter run -d windows`

界面：输入框输入中文 → 点击“翻译” → 展示英文 translation 和 3 个 keywords；请求时有 loading，失败会有 SnackBar/红字提示。

## 其他说明
- 后端已开启 CORS（允许本地跨域调试）。
- LLM 输出解析具备容错：尝试 `json.loads`，提取最外层 JSON，再用模型纠错重试；keywords 最终保证长度 3。
- 健壮性：text 为空返回 400，并带明确信息。

