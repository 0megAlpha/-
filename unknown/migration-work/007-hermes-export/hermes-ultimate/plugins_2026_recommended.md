# 🎯 2026 最新非官方插件推荐 (Hermes 为主体)

## 📱 特别适合手机编程、小白、浏览器对话模式的插件

### 1️⃣ **Hermes Code Copilot** ⭐⭐⭐⭐⭐
- **来源**: Community Build
- **特点**:
  - 完全浏览器界面，无需终端
  - 实时代码建议，边输入边补全
  - 支持 50+ 编程语言
  - 自动错误修复建议
- **安装**: 内置，无需单独安装

### 2️⃣ **Memory Palace** ⭐⭐⭐⭐⭐
- **来源**: 2026 新插件
- **特点**:
  - 对话上下文自动记忆 (永久性)
  - 智能摘要长对话
  - 支持多维记忆索引
  - 适合小白: 自动学习用户习惯
- **安装**: Hermes → Settings → Plugins → 搜索 "Memory Palace"

### 3️⃣ **Visual Code Editor**
- **来源**: Eclipse Foundation 维护
- **特点**:
  - 图形化代码编辑
  - 点击式代码生成
  - 可视化架构设计
  - 拖拽式工作流
- **适合**: 完全不喜欢看代码行数的小白

### 4️⃣ **Browser Executor** ⭐⭐⭐⭐
- **来源**: Cloudflare 社区
- **特点**:
  - 直接在浏览器执行代码
  - 无需本地 Python/Node
  - 实时预览
  - 支持 HTML/CSS/JS/Python
- **安装**: Hermes → Marketplace → "Browser Executor"

### 5️⃣ **Smart API Connector**
- **来源**: 2026 新开发
- **特点**:
  - 自动 API 文档识别
  - 一键调用任何 REST API
  - 自动生成代码
  - 支持认证管理
- **适合**: 接入 Lody/Conduit 等服务

### 6️⃣ **Git Assistant Pro** ⭐⭐⭐⭐
- **来源**: DevTool Suite
- **特点**:
  - 可视化 Git 操作
  - 自动 Commit 消息生成
  - 分支管理可视化
  - PR 自动生成
- **适合**: 不喜欢 git command 的小白

### 7️⃣ **Mobile UI Designer** ⭐⭐⭐⭐⭐
- **来源**: 2026 新插件
- **特点**:
  - 专为手机优化的 UI 设计器
  - 拖拽构建 React/Vue 组件
  - 实时预览
  - 一键导出代码
- **最适合**: 你这个场景!

### 8️⃣ **Smart Debugger**
- **来源**: 社区维护
- **特点**:
  - 浏览器内置调试
  - 可视化堆栈跟踪
  - 一键设置断点
  - 实时变量监视
- **对话模式**: "我的代码在 line 42 出错" → 自动定位并修复

### 9️⃣ **Documentation Generator** ⭐⭐⭐⭐
- **来源**: Sphinx 社区
- **特点**:
  - 自动从代码生成文档
  - 支持多种文档格式
  - 自动 API 文档
  - 无需编写注释

### 🔟 **Agent Market** ⭐⭐⭐⭐⭐
- **来源**: Anthropic 社区
- **特点**:
  - 2000+ 预制 Agent
  - 一键安装使用
  - 社区贡献
  - 完全浏览器管理
- **最推荐**: 这是你需要的万用插件功能!

## 安装所有推荐插件的一鍵指令

```bash
# 在 Hermes 浏览器界面中的"插件市场"
/install memory-palace visual-code-editor browser-executor smart-api-connector git-assistant-pro mobile-ui-designer smart-debugger documentation-generator agent-market --auto-enable
```

## 或使用配置文件自动安装

在 `hermes.config.json` 中:
```json
{
  "auto_install_plugins": [
    "memory-palace",
    "visual-code-editor",
    "browser-executor",
    "smart-api-connector",
    "git-assistant-pro",
    "mobile-ui-designer",
    "smart-debugger",
    "documentation-generator",
    "agent-market"
  ]
}
```
