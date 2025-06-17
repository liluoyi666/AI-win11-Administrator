from datetime import datetime
from zoneinfo import ZoneInfo
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QObject
from zoneinfo import ZoneInfo


from brain import executor_chat_prompt,supervisor_chat_prompt
from brain import create_client, get_response_from_llm
from Control_Center import setting,status


def get_time():
    return str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19]


class chat_cycle(QThread):

    work_exit = pyqtSignal(int)                 # 退出标记
    Round_num = pyqtSignal(int)                 # 轮次
    executor_output = pyqtSignal(str)           # 执行者输出
    supervisor_output = pyqtSignal(str)         # 监察者输出
    Setting = pyqtSignal(setting)               # 基础设置

    def __init__(self):
        super().__init__()

        self.setting = None
        self.status = None

        self.to_executor = ''       # 执行者视图下的信息
        self.to_supervisor = ''     # 监察者视图下的信息
        self.user_msg = None

        self.executor_result = ''
        self.supervisor_result = ''

# ----------------------------------------------------------------------------------------------------------------------
    def run(self):
        # 进入主循环
        round_num = 1

        while True:
            self.Round_num.emit(round_num)

            # 等待用户的操作
            while True:
                if self.user_msg is None or self.user_msg == "":
                    time.sleep(0.1)
                else:
                    self.to_executor += f"用户({get_time()}):\n{self.user_msg}"
                    self.to_supervisor += f"用户({get_time()}):\n{self.user_msg}"
                    self.user_msg = None
                    break
                if self.status.exit != 1:
                    break

            if self.status.exit != 1:
                break

            # 获取执行者的响应并发送信号
            self.executor_result = self.get_result_executor(self.to_executor,round_num)
            self.executor_output.emit(self.executor_result)
            self.to_supervisor += f"执行者({get_time()}):\n{self.executor_result}"
            self.to_executor = ''

            # 获取监察者的响应并发送信号
            if self.status.single_or_dual == 2:
                self.supervisor_result= self.get_result_supervisor(self.to_supervisor,round_num)
                self.to_executor += f"监察者({get_time()}):\n{self.supervisor_result}"
                self.to_supervisor = ''
            else:
                self.supervisor_result= ""
            self.supervisor_output.emit(self.supervisor_result)

            if self.status.exit != 1:
                break

            round_num += 1
            print(round_num, '----------------------------------------------------------------------\n\n')

        # 清空信息
        self.to_executor = ''
        self.to_supervisor = ''
        self.user_msg = None

        self.Setting.emit(self.setting)
        self.work_exit.emit(0)

# ----------------------------------------------------------------------------------------------------------------------
    # 获取执行者响应
    def get_result_executor(self, msg, round_num):
        system_msg = executor_chat_prompt(
            user = self.setting.user,
            system = self.setting.system,
            language = self.setting.language,
            time = str(datetime.now(ZoneInfo("Asia/Shanghai"))),
            num = round_num
        )
        # 尝试得到ai的响应
        try:
            executor_result, self.setting.executor_memory = get_response_from_llm(
                msg = msg,
                client = self.setting.executor_client,
                model = self.setting.test_model,
                system_message = system_msg,
                msg_history = self.setting.executor_memory,
                print_debug = False,  # 开启调试输出
                temperature = self.setting.temperature
            )
            if self.setting.LLM_print:
                print('执行者输出:\n', executor_result)
        except Exception as e:
            print(f"\n运行时错误: {str(e)}")
            if "AuthenticationError" in str(e):
                print("请检查API密钥是否正确设置")
            elif "RateLimitError" in str(e):
                print("API调用限额已用尽，请稍后重试")

        return executor_result

# ----------------------------------------------------------------------------------------------------------------------
    # 获取监察者响应
    def get_result_supervisor(self, msg, round_num):
        system_msg = supervisor_chat_prompt(
            user=self.setting.user,
            system=self.setting.system,
            language=self.setting.language,
            time=str(datetime.now(ZoneInfo("Asia/Shanghai"))),
            num=round_num
        )

        try:
            supervisor_result, self.setting.supervisor_memory = get_response_from_llm(
                msg = msg,
                client=self.setting.supervisor_client,
                model=self.setting.test_model,
                system_message=system_msg,
                msg_history=self.setting.supervisor_memory,
                print_debug=False,  # 开启调试输出
                temperature=self.setting.temperature
            )
            if self.setting.LLM_print:
                print('监察者输出:\n', supervisor_result)
        except Exception as e:
            print(f"\n运行时错误: {str(e)}")
            if "AuthenticationError" in str(e):
                print("请检查API密钥是否正确设置")
            elif "RateLimitError" in str(e):
                print("API调用限额已用尽，请稍后重试")

        return supervisor_result

# ----------------------------------------------------------------------------------------------------------------------
    # 控制函数
    @pyqtSlot()
    def Exit(self):  # 退出
        self.status.exit = 0

    @pyqtSlot()
    def num_AI(self):  # 切换AI个数
        if self.status.single_or_dual == 1:
            self.status.single_or_dual = 2
        else:
            self.status.single_or_dual = 1

    @pyqtSlot()
    def send_user_msg(self,msg):
        self.user_msg=msg

    @pyqtSlot()
    def send_status(self,setting:setting,status:status):
        self.setting = setting
        self.status = status


if __name__ == '__main__':
    print()