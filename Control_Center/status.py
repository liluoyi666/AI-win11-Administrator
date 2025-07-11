from datetime import datetime
from sys import stdout
from zoneinfo import ZoneInfo
import json
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QObject

from brain import PowerShellSession
from brain import create_client, get_response_from_llm
from brain import json_parser,json_parser_push
from brain import log

from more_Types import Name_TextEditor,TextEditor_user_manual,TextEditor

"""
中央状态定义
"""

# 系统基础设置，保存：AI客户端，AI记忆，命令行状态，日志开启。不参与GUI直接信息交换
class setting(QObject):
    def __init__(self,user='wqws',language='Zh',model_name="deepseek-chat",system="win11",temperature=0.75,
                 executor_log_path="C:\\AI-win11-Administrator\\logs\\log_ai_executor.txt",
                 supervisor_log_path="C:\\AI-win11-Administrator\\logs\\log_ai_supervisor.txt",
                 LLM_print=True, stdout_print=True, stderr_print=True):
        super().__init__()

        self.test_model = model_name        # 模型名称
        self.user=user                      # 用户
        self.system=system                  # 用户计算机系统
        self.language=language              # 用户语言
        self.temperature=temperature        # 生成自由度

        self.LLM_print=LLM_print            # 是否打印AI输出
        self.stderr_print=stderr_print      # 是否打印系统输出
        self.stdout_print=stdout_print      # 是否打印系统错误

        self.powershell = PowerShellSession()                                       # 创建powershell长期存在窗口

        self.executor_client, self.test_model = create_client(self.test_model)      # 创建执行者客户端
        self.executor_log=log(executor_log_path)                                    # 打开执行者日志
        self.executor_memory = None                                                 # 执行者记忆

        self.supervisor_client, self.test_model = create_client(self.test_model)    # 创建监察者客户端
        self.supervisor_log=log(supervisor_log_path)                                # 打开监察者日志
        self.supervisor_memory = None                                               # 监察者记忆

        print('系统设置初始化完成')

    def close(self):
        self.executor_log.flush_buffer()
        self.supervisor_log.flush_buffer()

        self.powershell.close()


# 可修改的系统状态，参与GUI的信息交换
class status:
    def __init__(self):

        self.single_or_dual = 1     # 工作与聊天公用

        self.exit = 0               #0为工作，1为聊天