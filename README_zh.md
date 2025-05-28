# AI命令行界面项目
## 项目概述
本项目提供了一个基于AI的命令行界面 可以通过JSON格式命令与Windows 11虚拟机交互. 系统支持文件操作、命令执行和日志记录功能.
## 项目结构
- `main.py`: 启动交互周期的主入口点
- `main_cycle.py`: 处理与AI交互循环的核心逻辑
- `brain/`: 包含核心功能的模块
  - `executor.py`: 处理PowerShell命令执行
  - `LLM_api.py`: 管理LLM API交互
  - `String_Templates.py`: 包含提示模板和语法定义
- `logs/`: 系统日志目录
  - `ai_log.txt`: AI操作日志文件
## 功能特性
- 基于JSON的命令接口
- PowerShell命令执行
- LLM集成提供智能响应
- 全面的日志系统
- 支持UTF-8编码的多语言内容
## 系统要求
- Python 3.9及以上+
- PowerShell 7及以上+
- LLM API access (configured in brain/LLM_api.py)
## 使用方法
1. 运行`main.py`启动交互周期
2. AI将处理JSON格式的命令
3. 查看`logs/ai_log.txt`中的日志获取操作历史
## 注意事项
- 读取包含中文的文件时需要`-Encoding utf8`参数
- 错误处理包含自动日志记录用于故障排除
- 对所有执行的命令强制执行安全验证
