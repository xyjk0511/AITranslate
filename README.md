# AITranslate / AI 翻译助手

A lightweight translation application with a **FastAPI backend** and **Flutter frontend**, designed for practical Chinese-English translation workflows and keyword extraction.

一个由 **FastAPI 后端** 和 **Flutter 前端** 组成的轻量级翻译应用，面向中英翻译与关键词提取等实际使用场景。

---

## Overview / 项目概述

**Goal / 目标**
- Provide a simple end-to-end AI translation app with both backend API and mobile/web-style client support.
- 提供一个完整的 AI 翻译小系统，既有后端接口，也有前端客户端。

This repository is useful as a small full-stack AI application example:
- backend API service
- frontend client interaction
- environment-based LLM configuration
- practical deployment-friendly structure

这个仓库适合作为一个小型全栈 AI 应用示例，体现：
- 后端 API 服务
- 前端交互
- 基于环境变量的模型接入
- 更接近实际部署的项目结构

---

## Architecture / 架构

```text
frontend (Flutter)
    ↓
FastAPI backend
    ↓
LLM provider (DashScope / compatible API)
```

### Main capabilities / 主要能力
- translate input text from Chinese to English
- return structured results to the client
- extract keywords alongside translation
- expose a clean health check and API endpoint

---

## Repository Structure / 仓库结构

```text
backend/           # FastAPI backend service
frontend/          # Flutter client
docs/              # project notes and usage docs
README.md          # project overview
```

---

## Backend / 后端

The backend is built with **FastAPI** and exposes a translation endpoint plus a health check.

后端使用 **FastAPI** 实现，提供翻译接口和健康检查接口。

### Typical setup / 基本启动方式
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Health check / 健康检查
```bash
curl http://127.0.0.1:8000/health
```

---

## Frontend / 前端

The frontend is built with **Flutter**, making the project suitable for mobile, desktop, or web-style experimentation.

前端使用 **Flutter**，适合做移动端、桌面端或 Web 端风格的实验。

### Typical setup / 基本启动方式
```bash
cd frontend
flutter pub get
flutter run
```

---

## Why this project matters / 为什么这个项目值得保留

This is not the strongest ML project in the portfolio, but it is still a useful example of:
- integrating an LLM-backed backend with a real client
- handling environment-based API configuration
- building a small but complete AI product flow

它虽然不是你最强的 ML 项目，但仍然体现了：
- 用真实前后端连接 LLM 服务
- 通过环境变量管理模型接入
- 构建一个完整的小型 AI 产品流程

---

## Reproducibility / 复现说明

### Prerequisites
- Python 3.10+
- Flutter SDK
- an API key configured through environment variables

### Environment variables
Set your provider key in the backend environment file, for example:
```bash
DASHSCOPE_API_KEY=your_api_key_here
```

---

## Future improvements / 后续可改进方向

- improve README examples and screenshots
- add request/response schema examples
- unify backend/frontend local development commands
- add small demo GIFs or UI screenshots

如果继续整理，这个项目最值得补的是：
- README 示例与截图
- 请求 / 响应示例
- 更统一的前后端启动方式
- 界面演示图或录屏
