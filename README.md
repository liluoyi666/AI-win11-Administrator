
# AI-win11-Administrator (English)
点击 [AI-win11-管理员 (中文)](#ai-win11-管理员-中文) 跳转到中文版.

## Project Overview
This project aims to enable large language models (LLMs) to operate Windows 11 systems. By having AI output specially formatted JSON, the system parses instructions from the JSON and executes them, allowing AI to perform various tasks. This enables automation of Windows 11 operations, allowing repetitive tasks to be completed automatically by AI to improve work efficiency.
***This unleashes the full potential of AI***
</br>

The dual-AI architecture utilizes two AIs for mutual supervision and collaborative work. One AI generates instructions while the other confirms whether they should be executed and provides feedback. This architecture better handles complex tasks and situations while significantly enhancing security. Additionally, the dual-AI architecture greatly improves the user experience during interactions.
***AI security and entertainment value will be significantly enhanced***


## Directory

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Core Features](#core-features)
- [AI Command Format and Execution Principle](#ai-command-format-and-execution-principle)
- [Single-AI vs Dual-AI Architecture](#single-ai-vs-dual-ai-architecture)
- [GUI Software Design and Features](#gui-software-design-and-features)
- [Project Vision](#project-vision)
- [Current Status](#current-status)
- [Local Deployment Guide](#local-deployment-guide)
- [Contribution](#contribution)
- [License](#license)
- [Developer's Message](#developers-message)


## Project Structure
```
AI-win11-Administrator:
    main.py             # Launches GUI

    more_Types/         # Additional operation types

    logs/:              # Logs
        log_ai_executor.txt     # Executor AI logs
        log_ai_supervisor.txt   # Supervisor AI logs
    
    brain/:             # Core functionality implementation
        prompts/:               # AI prompts
            String.py                   # Common strings
            String_chat.py              # Chat prompt templates
            String_work.py              # Work prompt templates
        json_parser.py          # JSON parser
        LLM_api.py              # API interface
        log_editor.py           # Logging service
        powershell.py           # Command line
    
    Control_Center/:    # Central control system
        GUI.py                  # GUI interface
        new_GUI.py              # New GUI
        status.py               # System status class
        thread_chat.py          # Chat thread
        thread_work.py          # Work thread
    
    Role_Settings/      # AI character customization (in development)

```

## Core Features
- **Structured JSON Execution of PowerShell Commands**: Through specially formatted JSON, LLMs can conveniently execute PowerShell commands to operate the system.
- **Secure Virtual Machine Environment**: Deployed in a VM to enhance system security and prevent accidental damage to the host system.
- **Multi-Data Type Interfaces**: Supports interfaces for various data types, providing richer data processing capabilities for LLMs.
- **Switchable Single/Dual AI Modes**: Choose between modes based on security needs and resource constraints to accommodate different user requirements.
</br>

## AI Command Format and Execution Principle
### Workflow
```
while True:
    AI generates JSON based on system feedback from previous round
    System parses instructions from JSON and executes them
    System feedback from execution is preserved for next AI round
```

### Command Format
AI output must contain JSON in the following format. The system detects AI output, extracts commands, and executes them:
```json
{
    "type": "operation_type",
    "command_details",   
    "add_log": "Optional log message during execution"
}
```
The "type" key is always required. Other keys depend on the operation type. The "add_log" key doesn't affect operation execution but adds log entries. Timestamps and line breaks are added automatically during logging. Log files are maintained automatically by the system.

### Execution Principle
The core execution cycle in main_cycle.py receives LLM responses and parses the JSON. Based on the "type" key, it calls corresponding methods. For example:
- If type is "powershell", execute PowerShell commands via PowerShellSession class
- If type is "read_log", read logs via log class read method
</br>

## Single-AI vs Dual-AI Architecture
### Single-AI Architecture
A single AI handles both instruction parsing and execution. It directly receives user input, converts requirements into operational commands based on built-in rules, and executes them through the PowerShell interface.

### Dual-AI Architecture

Features two specialized AIs:
1. **Executor AI**: Generates commands to achieve user objectives
2. **Supervisor AI**: Decides whether commands should be executed and provides solutions/feedback

Logs are maintained separately. Executor outputs are fully visible to Supervisor, while only partial Supervisor outputs are shared with Executor. Future development will balance permissions between them. The dual-AI architecture enhances system stability and security while improving user interaction experience.
</br>

## GUI Software Design and Features
### Chat vs Work States
- **Initial State**: Chat mode for conversing with AI
- **Work Mode**: User can queue messages but not chat directly
- **Flexible Switching**: Seamlessly switch between modes while preserving AI memory and PowerShell session states

### Message Queue Mechanism
During work mode, users can queue up to three messages with timestamps. Messages can be added:
- Before entering work mode (pre-planned instructions)
- During work mode (real-time adjustments)
Messages are automatically timestamped to ensure AI understands information timeliness.

### GUI Layout
- **Left Panel**: Log display showing:
  - AI-generated commands during work mode
  - Chat messages during conversation mode
  - System notifications (all timestamped)
- **Right Panel**: Control panel with:
  - Mode switching
  - AI configuration
  - Message queuing
  - System status information
</br>

## Project Vision
### Original Plan
- **Initial Stage**: Enable LLM PowerShell operation with stable execution
- **Early Stage**: Migrate to VM environment, add more operation syntax and security
- **Mid Stage**: Expand data interfaces, enable autonomous completion of simple projects
- **Final Stage**: Non-VM deployment enabling AI to safely handle 50% of human computer tasks

### Extended Plan
- **Initial Stage**: Implement stable dual-AI command execution
- **Early Stage**: Achieve seamless chat/work mode switching
- **Mid Stage**: Develop visual interface, expand data interfaces, design AI avatars
- **Final Stage**: Create integrated solution combining automation, conversational AI, and system security
</br>

## Current Status
- **Single-AI architecture operational**
- **Added file I/O methods with 100-line write capacity**
- **Enhanced JSON parser reducing error rates**
- **Dual-AI architecture functional**
- **Multi-command batch execution implemented**
- **GUI with chat functionality completed**
</br>

## Local Deployment Guide
### Environment Setup
System requirements:
- **OS**: Windows 11
- **Python**: 3.x
- **Dependencies**: Install via:
```bash
pip install -r requirements.txt
```

### API Key Configuration
Configure API keys according to your LLM provider. For DeepSeek:
```bash
set DEEPSEEK_API_KEY=your_api_key  # Windows
# or
export DEEPSEEK_API_KEY=your_api_key  # Linux/macOS
```

### Launching the Project
Run from project root:
```bash
python main.py
```

### Main Cycle Configuration
In `main.py`, configure parameters like `max_rounds` and initial message:
```python
msg = '''
When first entering command line, you're in the project's main directory.
Your task: ...
'''

xxx = main_cycle_single(log_path=r"logs/log_ai_executor.txt")
xxx.cycle(max_rounds=30, msg=msg)
```


## Contribution
### Code Understanding Sequence:
1. `brain/LLM_api.py`
2. `brain/String.py`
3. `brain/powershell.py`
4. `Control_Center/thread_work.py`

### Contribution Guidelines:
1. Fork the repository
2. Create new branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push branch: `git push origin feature/your-feature`
5. Submit Pull Request
</br>

## License
This project is licensed under [LICENSE NAME]. See `LICENSE` for details.
</br>

## Developer's Message:
The developer acknowledges that VM deployment solves over 80% of security concerns. However, requiring all users to install VM software presents significant adoption barriers. More importantly, if AI cannot directly operate the user's computer, the software's utility diminishes substantially. We must therefore consider security without relying on VM deployment - otherwise this project loses much of its purpose.
</br>

Banning "rm" commands is like the proverbial ostrich hiding its head. AI could package destructive commands in scripts, and sometimes "rm" is legitimately used for cleanup. Hard-coded restrictions can't prevent misuse - only something with equivalent intelligence can effectively supervise AI. Hence we developed the dual-AI "Executor-Supervisor" architecture. This should prove interesting, though we can't yet guarantee its effectiveness.
</br>

AI role-playing is fascinating - and no, I'm not just playing around. We might increase the Executor's creative freedom while restricting the Supervisor's, creating distinct AI personalities. This would enhance both security and user experience. Imagine chatting with AIs exhibiting different personalities - that's valuable beyond just technical considerations.

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
- [GUI软件设计与功能介绍](#gui软件设计与功能介绍)
- [项目愿景](#项目愿景)
- [当前情况](#当前状况)
- [本地部署方法](#本地部署方法)
- [贡献](#贡献)
- [许可证](#许可证)
- [开发者留言](#开发者留言)

## 项目结构
```
AI-win11-Administrator:
    main.py             # 启动GUI

    more_Types/         # 更多操作类型

    logs/:              # 日志
        log_ai_executor.txt     # 执行者AI日志
        log_ai_supervisor.txt   # 监察者AI日志
    
    brain/:             # 核心功能实现
        prompts/:               # AI提示词
            String.py                   # 通用字符串
            String_chat.py              # 聊天提示词模板
            String_work.py              # 工作提示词模板
        json_parser.py          # json解析器
        LLM_api.py              # api
        log_editor.py           # 日志服务
        powershell.py           # 命令行
    
    Control_Center/:    # 中央控制系统
        GUI.py                  # GUI
        new_GUI.py              # 新GUI
        status.py               # 系统状态类
        thread_chat.py          # 聊天线程
        thread_work.py          # 工作线程
    
    Role_Settings/      # AI个性化角色设定(开发中)

```

## 核心特性
- **结构化JSON执行PowerShell命令**：通过特定格式的JSON，LLM可以方便地执行PowerShell命令，实现对系统的操作。
- **安全的虚拟机环境**：将程序部署在虚拟机中，增加了系统的安全性，避免因错误操作对主机系统造成影响。
- **多数据类型接口**：支持多种数据类型的接口，为LLM提供更丰富的数据处理能力。
- **单AI模式与双AI模式自由切换**：根据安全需求与经济条件选择模式，以适应不同用户需求。
</br>

## AI命令格式与命令执行的原理
### 运行流程
```
while True:
    AI通过上一轮系统返回的消息，生成json
    系统解析json中的指令，并执行
    保留执行时系统返回的信息，下一轮返回给AI
```

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
</br>

## 单AI架构与双AI架构
### 单AI架构
单 AI 架构是指整个系统中只有一个 AI解析指令和执行操作。
它直接接收用户的留言，根据内置的规则和操作手册，将用户的需求转化为具体的操作命令，并通过 PowerShell 接口执行这些命令。

### 双AI架构

设定两个AI：执行者AI与监察者AI，执行者负责编写命令以完成用户的目标，监察者当前负责决定是否应该执行执行者的命令，并为执行者提供思路与解决方案。
双方的日志分别独立，执行者的所有输出对监察者完全公开，监察者的输出只有部分向执行者分开。
后续为了平衡执行者和监察者的操作权限，还会进行进一步的平衡性调整，进一步修改其可执行命令。
双AI架构有利于提示系统稳定性与安全性，在后续开发与用户的交流对话模式下，双AI也可以提升用户在交流中趣味性。
</br>

## GUI软件设计与功能介绍
### 聊天与工作状态
初始进入GUI为聊天状态，可与AI进行聊天，可提前保存工作留言，以及进入工作状态。进入工作状态后，你无法与AI直接进行交流，但可继续追加工作留言，与AI保持交流。
在工作期间，你可以随时切换为聊天状态与AI交流，即便反复进行状态切换，AI的记忆和powershell的状态都会长期保存，从而确保AI操作的连续性，灵活性，可控性。

### 工作留言机制
在工作期间AI无法与你直接交流，但可以通过留言获取用户的任务以及提示。留言队列可以保存最新的三条用户留言，并在工作状态时呈现给AI。
在聊天状态时用户可以提前进行留言追加，在工作状态开启后AI将会得到用户的留言。在工作状态时，用户也可以进行该操作，实现在工作中途给AI传递信息。
用户的留言会实时追加到留言列表中，且自带时间信息，确保AI了解信息的时效。

### GUI布局设计
左侧为日志信息流显示区，在工作时显示AI生成的指令以及AI操作后返回的信息，在聊天时显示AI的聊天信息，当然也包括用户发送的信息以及本系统的提示信息，且这些信息都附带了时间信息。
右侧为控制面板，可切换当前状态，切换AI个数，追加工作留言。并显示工作状态信息。
</br>

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
</br>

## 当前状况
- **单AI架构初步运行成功**
- **增加了文件读写方法，实现100行文本一次写入**
- **修改了json解析器，大大降低报错率**
- **双AI架构初步运行成功**
- **能够一次检测多个json，并按顺序运行，大大提高操作效率**
- **开发完成GUI以及聊天功能**
</br>

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
2. `brain/String.py`
3. `brain/powershell.py`
4. `Control_Center/thread_work.py`

### 如果你想为这个项目做出贡献，请遵循以下步骤：
1. Fork这个仓库。
2. 创建一个新的分支：`git checkout -b feature/your-feature-name`。
3. 提交你的更改：`git commit -m 'Add some feature'`。
4. 推送至分支：`git push origin feature/your-feature-name`。
5. 提交Pull Request。
</br>

## 许可证
本项目采用[许可证名称]许可证。请查看`LICENSE`文件以获取更多信息。
</br>

## 开发者留言：
开发者很清楚，虚拟机部署能够解决80%以上的安全问题。但是，逼迫所有用户都安装虚拟机软件是很困难的事情。而且，如果AI无法直接操作用户的计算机，这个软件的实用性功能会大大降低。开发者的意思是，我们可能需要要在抛弃虚拟机部署的前提下，考虑这个软件的安全性，否则这个软件的开发的意义并不大。
</br>

禁止AI运行rm指令就像是掩耳盗铃，AI可以把破坏指令包装成脚本再运行，而且有时候rm也可能只用于清理垃圾文件。通过硬编码难以阻止AI做坏事，能阻止AI的只有与其拥有同等智商的东西，因此，开发者们推出了双AI"执行者-监察者"架构。这应该是件很有意思的事情，尽管我们并不确定这是否有用。
</br>

让AI进行角色扮演是件很有趣的事情，好吧，我并没有只想着玩。也许可以增加执行者AI的生成自由度，降低监察者AI的生成自由度，实现实际上AI性格上的差别，在聊天时如果能感受到AI不同的性格也是很不错的体验，当然，这有利于安全。
```
This Markdown document provides both English and Chinese versions, with links at the beginning of each version to allow users to switch between languages easily.
