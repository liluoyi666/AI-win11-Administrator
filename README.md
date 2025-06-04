
# AI-win11-Administrator (English)
点击 [AI-win11-管理员 (中文)](#ai-win11-管理员-中文) 跳转到中文版.

## Project Overview
This project enables Large Language Models (LLMs) to operate Windows 11 systems. The AI outputs specifically formatted JSON, which is parsed to extract instructions for execution, allowing the AI to perform various tasks. This enables the automation of Windows 11 operations, where repetitive tasks can be completed autonomously by AI, enhancing work efficiency.
***This will maximize AI capabilities***
</br>

The Dual-AI architecture utilizes two AIs for mutual supervision and collaborative work. One AI generates instructions while the other verifies whether instructions should be executed and provides feedback. This architecture better handles complex tasks and scenarios while significantly improving security. It also greatly enhances user interaction experience.
***AI safety and interactivity will be substantially improved***

## Directory

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Core Features](#core-features)
- [AI Command Format and Execution Principles](#ai-command-format-and-command-execution-principles)
- [Single-AI vs Dual-AI Architecture](#single-ai-vs-dual-ai-architecture)
- [Project Vision](#project-vision)
- [Current Status](#current-status)
- [Local Deployment](#local-deployment)
- [Contribution](#contribution)
- [License](#license)

## Project Structure
- `main.py`: Entry point of the project, responsible for launching the main loop.
- `main_cycle_single.py`: Core execution loop for single-AI mode.
- `main_cycle_double.py`: Core execution loop for dual-AI mode.
- `brain/`: Core AI processing modules including PowerShell sessions, string templates, LLM API services, JSON parsers, and logging services.
- `logs/`: System operation logs recording various actions and information during runtime.
- `more_type/`: Provides additional operation types for the AI to perform more complex tasks.

## Core Features
- **Structured JSON for PowerShell Execution**: Enables LLMs to execute PowerShell commands through specifically formatted JSON for system operations.
- **Secure Virtual Machine Environment**: Deploys the program in a virtual machine to enhance system security and prevent host system damage from erroneous operations.
- **Multi-Data Type Interfaces**: Supports interfaces for various data types, providing richer data processing capabilities for LLMs.
- **Seamless Switching Between Single-AI and Dual-AI Modes**: Allows mode selection based on security requirements and economic constraints to accommodate different user needs.

## AI Command Format and Command Execution Principles
### Command Format
AI output must contain JSON in the following format. The system detects AI output, extracts commands, and executes them on the computer:
```json
{
    "type": "operation_type",
    "related_command",   
    "add_log": "log_entry_written_during_operation"
}
```
The `type` key must always be present. Other keys depend on the specific operation type. The absence of `add_log` doesn't affect operation execution, and its presence doesn't interfere with any operation type. Log entries automatically include timestamps and line breaks. Log files are automatically maintained by the system.
### Command Execution Principle
The system's core execution loop (`main_cycle.py`) receives LLM responses and parses the contained JSON. Based on the `type` key, it invokes corresponding operation methods. For example:
- If `type` is `powershell`, it executes PowerShell commands using the `PowerShellSession.execute_command()` method
- If `type` is `read_log`, it reads logs using the `log.read()` method

## Single-AI vs Dual-AI Architecture
### Single-AI Architecture
A single AI handles both instruction interpretation and operation execution. It directly processes user input, converts requirements into operational commands based on built-in rules and manuals, and executes them through the PowerShell interface.

### Dual-AI Architecture
Uses two specialized AIs:
1. **Executor AI**: Generates commands to achieve user objectives
2. **Supervisor AI**: Decides whether to execute the Executor's commands and provides solutions/feedback

- Logs are maintained separately
- Executor outputs are fully visible to Supervisor
- Supervisor outputs are partially visible to Executor
- Future updates will balance permissions between both AIs

This architecture improves system stability, security, and enhances user interaction experience.

## Project Vision
### Original Plan
- **Initial Stage**: Enable LLM PowerShell operations with stable program execution
- **Early Stage**: Migrate to VM environment; expand operation syntax and security settings
- **Mid Stage**: Add more data type interfaces; enable autonomous completion of simple projects
- **Final Stage**: Achieve non-VM deployment; enable safe completion of 50% of human computer tasks
</br>

### Extended Plan
- **Initial Stage**: Achieve stable dual-AI command execution
- **Early Stage**: Implement seamless switching between work and conversation modes
- **Mid Stage**: Develop GUI applications; add more data interfaces; design AI avatars
- **Final Stage**: Create integrated solution combining automation, conversational AI, and system security management

## Current Status
- **Single-AI architecture operational**
- **Added file I/O methods (100-line text batch writing)**
- **Improved JSON parser (significantly reduced error rate)**
- **Dual-AI architecture operational**

## Local Deployment
### Environment Setup
Ensure your system meets these requirements:
- **OS**: Windows 11
- **Python**: Python 3.x
- **Dependencies**: Install from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### API Key Configuration
Configure API keys according to your LLM provider. For DeepSeek models:
```bash
export DEEPSEEK_API_KEY=your_api_key
```

### Launch Project
Run from project root:
```bash
python main.py
```

### Main Loop Execution
Configure parameters in `main.py`:
```python
msg = '''
When entering CLI, you're in the project's main directory.
Your task: ...
'''

xxx = main_cycle_single(log_path=r"logs/log_ai_executor.txt")
xxx.cycle(max_rounds=30, msg=msg)
```

## Contribution
### Code Comprehension Guide:
1. `brain/LLM_api.py`
2. `brain/String_Templates.py`
3. `brain/powershell.py`
4. `main_cycle_single/double.py`

### Contribution Steps:
1. Fork the repository
2. Create new branch: `git checkout -b feature/your-feature-name`
3. Commit changes: `git commit -m 'Add some feature'`
4. Push branch: `git push origin feature/your-feature-name`
5. Submit Pull Request

## License
This project is licensed under [License Name]. See `LICENSE` for details.

### ---------------------------------------------------------------------------------------------------------------

# AI-win11-管理员 (中文)
Click [AI-win11-Administrator (English)](#ai-win11-administrator-english) to switch to English。

## 项目概述
本项目旨在让大语言模型（LLM）能够操作Windows 11系统。让AI输出特地格式的json，解析json中的指令，对指令进行执行，允许AI执行各种任务。这为自动化操作Windows 11系统提供了可能，使得一些重复性的任务可以由AI自动完成，提高工作效率。
***这将把AI的能力发挥到极致***
</br>

双 AI 架构原理是利用两个 AI 进行互相监督协同工作，一个 AI 负责生成指令，另一个负责确认指令是否应该执行并提出意见。这种架构能更好地应对复杂的任务和情况，且大大提升安全性。且双AI架构能极大提升用户在交互时的体验。
***AI安全性与趣味性将有巨大提升***

## 目录

- [项目概述](#项目概述)
- [项目结构](#项目结构)
- [核心特性](#核心特性)
- [AI命令格式与命令执行的原理](#ai命令格式与命令执行的原理)
- [单AI架构与双AI架构](#单ai架构与双ai架构)
- [项目愿景](#项目愿景)
- [当前情况](#当前状况)
- [本地部署方法](#本地部署方法)
- [贡献](#贡献)
- [许可证](#许可证)

## 项目结构
- `main.py`：项目的入口文件，负责启动主循环。
- `main_cycle_single.py`：单AI核心执行循环。
- `main_cycle_double.py`：双AI核心执行循环。
- `brain`/：核心 AI 处理模块，包含 PowerShell 会话、字符串模板、LLM API 服务、JSON 解析器和日志服务等。
- `logs`/：系统操作日志，记录系统运行过程中的各种操作和信息。
- `more_type`/：为 ai 提供更多的操作类型，从而执行更复杂的任务。

## 核心特性
- **结构化JSON执行PowerShell命令**：通过特定格式的JSON，LLM可以方便地执行PowerShell命令，实现对系统的操作。
- **安全的虚拟机环境**：将程序部署在虚拟机中，增加了系统的安全性，避免因错误操作对主机系统造成影响。
- **多数据类型接口**：支持多种数据类型的接口，为LLM提供更丰富的数据处理能力。
- **单AI模式与双AI模式自由切换**：根据安全需求与经济条件选择模式，以适应不同用户需求。

## AI命令格式与命令执行的原理
### 命令格式
AI的输出需包含以下格式的json，系统会检测AI的输出，并将提取出命令，在计算机中执行：
```json
{
    "type": "操作类型",
    "相关命令",   
    "add_log": "执行操作时顺便写入日志"
}
```
任何情况下都必须存在type键，其他键具体由type决定。add_log不存在不影响操作执行，add_log存在也不会影响任何类型的操作。记入日志时会自动添加时间以及换行，无需手动添加。日志文件由系统自动维护。
### 命令执行原理
系统通过main_cycle.py的核心执行循环，接收 LLM 的响应并解析其中的 JSON。根据 JSON 中的type键，调用相应的操作方法。例如，如果type为powershell，则调用PowerShellSession类的execute_command方法执行相应的 PowerShell 命令；如果type为read_log，则调用log类的read方法读取日志。

## 单AI架构与双AI架构
### 单AI架构
单 AI 架构是指整个系统中只有一个 AI解析指令和执行操作。
它直接接收用户的留言，根据内置的规则和操作手册，将用户的需求转化为具体的操作命令，并通过 PowerShell 接口执行这些命令。

### 双AI架构
设定两个AI：执行者AI与监察者AI，执行者负责编写命令以完成用户的目标，监察者当前负责决定是否应该执行执行者的命令，并为执行者提供思路与解决方案。
双方的日志分别独立，执行者的所有输出对监察者完全公开，监察者的输出只有部分向执行者分开。
后续为了平衡执行者和监察者的操作权限，还会进行进一步的平衡性调整，进一步修改其可执行命令。
双AI架构有利于提示系统稳定性与安全性，在后续开发与用户的交流对话模式下，双AI也可以提升用户在交流中趣味性。

## 项目愿景
### 原始计划
- **起步阶段**：让LLM能够操作PowerShell，确保程序稳定运行。
- **初期阶段**：将程序转移到虚拟机，增加更多操作语法和安全设置。
- **中期阶段**：增加更多数据类型接口，尝试让LLM自主完成某些简单项目。
- **最终阶段**：实现非虚拟机部署，让LLM安全稳定地完成人类50%的计算机任务。
</br>

### 分支计划
- **起步阶段**：实现双AI命令执行系统稳定运行。
- **初期阶段**：实现工作状态与对话状态的自由切换，既可与用户对话，也可以操作计算机。
- **中期阶段**：开发可视化窗口以及软件，增加更多数据类型接口，设计AI虚拟形象。
- **最终阶段**：完成为一集成：自动化工作，休闲聊天，电脑安全管控等功能的多功能AI桌面助手。

## 当前状况
- **单AI架构初步运行成功**
- **增加了文件读写方法，实现100行文本一次写入**
- **修改了json解析器，大大降低报错率**
- **双AI架构初步运行成功**

## 本地部署方法
### 环境准备
确保你的系统满足以下要求：
- **操作系统**：Windows 11
- **Python版本**：Python 3.x
- **依赖库**：根据`requirements.txt`文件安装所需的依赖库。可以使用以下命令进行安装：
```bash
pip install -r requirements.txt
```

### 配置API密钥
根据你使用的LLM模型，配置相应的API密钥。例如，如果你使用的是DeepSeek模型，需要设置`DEEPSEEK_API_KEY`环境变量：
```bash
export DEEPSEEK_API_KEY=your_api_key
```

### 启动项目
在项目根目录下，运行以下命令启动项目：
```bash
python main.py
```

### 运行主循环
在`main.py`文件中，你可以设置一些参数，如`max_rounds`和`msg`，来控制主循环的运行。例如：

```python
msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
你需要做：...
'''

xxx = main_cycle_single(log_path=r"logs/log_ai_executor.txt")
xxx.cycle(max_rounds=30, msg=msg)
```

## 贡献
### 如果你想完全理解代码，可按照该顺序查看代码：
1. `brain/LLM_api.py`
2. `brain/String_Templates.py`
3. `brain/powershell.py`
4. `main_cycle_single/double.py`

### 如果你想为这个项目做出贡献，请遵循以下步骤：
1. Fork这个仓库。
2. 创建一个新的分支：`git checkout -b feature/your-feature-name`。
3. 提交你的更改：`git commit -m 'Add some feature'`。
4. 推送至分支：`git push origin feature/your-feature-name`。
5. 提交Pull Request。

## 许可证
本项目采用[许可证名称]许可证。请查看`LICENSE`文件以获取更多信息。
```

This Markdown document provides both English and Chinese versions, with links at the beginning of each version to allow users to switch between languages easily.
