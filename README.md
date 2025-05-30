﻿
# AI-win11-Administrator (English)
点击 [AI-win11-管理员 (中文)](#ai-win11-管理员-中文) 跳转到中文版.

## Project Overview
This project aims to enable large language models (LLMs) to operate the Windows 11 system. Through a controllable PowerShell interface, the system allows the AI to perform various tasks while maintaining stability. This makes it possible to automate operations on the Windows 11 system, enabling the AI to automatically complete some repetitive tasks and improving work efficiency.
***This will maximize the capabilities of AI***

## Core Features
- **Structured JSON Execution of PowerShell Commands**: LLMs can easily execute PowerShell commands through a specific JSON format to operate the system.
- **Secure Virtual Machine Environment**: Deploying the program in a virtual machine enhances system security and avoids potential impacts on the host system due to incorrect operations.
- **Multi - Data Type Interfaces**: Supports interfaces for multiple data types, providing LLMs with more comprehensive data processing capabilities.
- **Self - Iteration Ability**: LLMs have the ability to self - iterate, continuously improving performance and functionality over time.

## Project Vision
### Plan
- **Initial Stage**: Enable the LLM to operate PowerShell and ensure the program runs stably.
- **Early Stage**: Transfer the program to a virtual machine and add more operation syntax and security settings.
- **Middle Stage**: Add more data type interfaces and attempt to let the LLM independently complete some simple projects.
- **Late Stage**: Enable the LLM to complete all tasks that humans can perform and achieve self - iteration.

### Core Settings
Let the LLM generate JSON in a fixed format for operations to ensure the standardization and manageability of operations.

## Project Structure
- `main.py`: The entry file of the project, responsible for starting the main loop.
- `main_cycle.py`: The core execution loop, which processes the LLM's responses and executes corresponding commands.
- `brain/`: The core AI processing module, including PowerShell sessions, string templates, LLM API services, JSON parsers, and log services.
- `logs/`: System operation logs, recording various operations and information during system operation.
- `more_type/`: Provides more operation types for the AI to execute more complex tasks.

## Future Plans
- **Expand the Command Set**: Add more operation types to enable the LLM to perform more complex tasks.
- **Enhance Self - Learning Ability**: Improve the LLM's self - learning ability to better adapt to different tasks and environments.
- **Add More Complex Task Automation**: Implement more complex task automation to further improve work efficiency.

## Usage
The system accepts commands in JSON format and executes them in environments such as PowerShell. Here are some JSON examples for common operations:

### Using the PowerShell Command Line
```json
{
    "type": "powershell",
    "command": "The command you want to execute",
    "add_log": "Write to the log while executing the instruction"
}
```

### Viewing Logs
```json
{
    "type": "read_log",
    "start": x,
    "end": y,
    "add_log": "Write to the log while executing the instruction"
}
```

### Stopping Interaction
```json
{
    "type": "exit",
    "confirm": "true",
    "add_log": "Write to the log while executing the instruction"
}
```

## Local Deployment Method
### Environment Preparation
Ensure your system meets the following requirements:
- **Operating System**: Windows 11
- **Python Version**: Python 3.x
- **Dependency Libraries**: Install the required dependency libraries according to the `requirements.txt` file. You can use the following command to install them:
```bash
pip install -r requirements.txt
```

### Configuring API Keys
Configure the corresponding API key according to the LLM model you are using. For example, if you are using the DeepSeek model, you need to set the `DEEPSEEK_API_KEY` environment variable:
```bash
export DEEPSEEK_API_KEY=your_api_key
```

### Starting the Project
In the project root directory, run the following command to start the project:
```bash
python main.py
```

### Running the Main Loop
In the `main.py` file, you can set some parameters, such as `max_rounds` and `msg`, to control the operation of the main loop. For example:
```python
msg = '''
If you first enter the command line, you will be in the main folder of this project.
What you need to do:...
'''

xxx = main_cycle(log_path=r"logs\log_ai.txt")
xxx.cycle(max_rounds=30, msg=msg)
```

## Contribution
### If you want to fully understand the code, you can view the code in the following order:
1. brain/LLM_api.py
2. brain/String_Templates.py
3. brain/powershell.py
4. main_cycle.py

### If you want to contribute to this project, please follow these steps:
1. Fork this repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a Pull Request.

## License
This project uses the [License Name] license. Please check the `LICENSE` file for more information.

***-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------***

# AI-win11-管理员 (中文)
Click [AI-win11-Administrator (English)](#ai-win11-administrator-english) to switch to Chinese。

## 项目概述
本项目旨在让大语言模型（LLM）能够操作Windows 11系统。通过一个可控的PowerShell接口，系统在保持稳定性的同时，允许AI执行各种任务。这为自动化操作Windows 11系统提供了可能，使得一些重复性的任务可以由AI自动完成，提高工作效率。
***这将把AI的能力发挥到极致***

## 核心特性
- **结构化JSON执行PowerShell命令**：通过特定格式的JSON，LLM可以方便地执行PowerShell命令，实现对系统的操作。
- **安全的虚拟机环境**：将程序部署在虚拟机中，增加了系统的安全性，避免因错误操作对主机系统造成影响。
- **多数据类型接口**：支持多种数据类型的接口，为LLM提供更丰富的数据处理能力。
- **自我迭代能力**：LLM具备自我迭代的能力，随着时间的推移可以不断提升性能和功能。

## 项目愿景
### 计划
- **起步阶段**：让LLM能够操作PowerShell，确保程序稳定运行。
- **初期阶段**：将程序转移到虚拟机，增加更多操作语法和安全设置。
- **中期阶段**：增加更多数据类型接口，尝试让LLM自主完成某些简单项目。
- **后期阶段**：让LLM完成人类所能完成的所有任务，并实现自我迭代。

### 核心设置
让LLM生成固定格式的JSON进行操作，以确保操作的规范性和可管理性。

## 项目结构
- `main.py`：项目的入口文件，负责启动主循环。
- `main_cycle.py`：核心执行循环，处理LLM的响应并执行相应的命令。
- `brain/`：核心AI处理模块，包含PowerShell会话、字符串模板、LLM API服务、JSON解析器和日志服务等。
- `logs/`：系统操作日志，记录系统运行过程中的各种操作和信息。
- `more_type/`：为ai提供更多的操作类型，从而执行更复杂的任务。

## 未来计划
- **扩展命令集**：增加更多的操作类型，让LLM能够执行更复杂的任务。
- **提升自学习能力**：提高LLM的自学习能力，使其能够更好地适应不同的任务和环境。
- **添加更复杂的任务自动化**：实现更复杂的任务自动化，进一步提高工作效率。

## 使用方法
系统接受JSON格式的命令，并在PowerShell等环境中执行。以下是一些常见操作的JSON示例：

### 使用PowerShell命令行
```json
{
    "type": "powershell",
    "command": "你要执行的命令",
    "add_log": "执行指令时顺便写入日志"
}
```

### 查看日志
```json
{
    "type": "read_log",
    "start": x,
    "end": y,
    "add_log": "执行指令时顺便写入日志"
}
```

### 停止交互
```json
{
    "type": "exit",
    "confirm": "true",
    "add_log": "执行指令时顺便写入日志"
}
```

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

xxx = main_cycle(log_path=r"logs\log_ai.txt")
xxx.cycle(max_rounds=30, msg=msg)
```

## 贡献
### 如果你想完全理解代码，可按照该顺序查看代码：
1. brain/LLM_api.py
2. brain/String_Templates.py
3. brain/powershell.py
4. main_cycle.py

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