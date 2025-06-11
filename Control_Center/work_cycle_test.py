from datetime import datetime
from sys import stdout
from zoneinfo import ZoneInfo
import json
import time

from brain import executor_system_prompt,executor_user_msg
from brain import supervisor_system_prompt,supervisor_user_msg

from brain import executor_grammar,supervisor_grammar,error_msg,single_ai

from brain import PowerShellSession
from brain import create_client, get_response_from_llm
from brain import json_parser,json_parser_push
from brain import log

from more_Types import Name_TextEditor,TextEditor_user_manual,TextEditor

from Control_Center import setting,status

"""
while Ture:
    得到执行者响应
    监察者确认
    执行命令
    输出传回LLM
"""

class work_cycle:
    def __init__(self,setting:setting,status:status):

        self.setting = setting

        self.status = status

        self.stdout = ''
        self.stderr = ''
        self.exit = 0

        self.executor_result=''
        self.supervisor_result=''

        # 将所有type对应的操作方法存储在字典
        self.method = {}
        self.method["powershell"] = self.setting.powershell.execute_command
        self.method["read_log"] = self.setting.executor_log.read
        self.method["exit"] = self.Exit
        self.method[Name_TextEditor] = TextEditor.execute

        # AI用操作手册
        self.Grammar= executor_grammar + TextEditor_user_manual


# ----------------------------------------------------------------------------------------------------------------------
    def cycle(self):

        # 进入主循环
        round_num = 1
        confirm = ''
        to_executor = ''

        while True:
            # 在每次循环开始时，接收用户是否exit,增加msg,切换AI个数
            if self.exit != 0:
                break

            # 获取执行者的响应
            self.executor_result = self.get_result_executor(self.status.get_msgs(),
                                                            round_num,
                                                            confirm,
                                                            to_executor)
            self.status.executor_result=self.executor_result
            # 在此处向GUI传输执行者的输出
            # 在每次循环中间时，接收用户是否exit,增加msg,切换AI个数
            # 如果使用双AI模式
            if self.status.single_or_dual==2:
                self.supervisor_result,confirm,to_executor = self.get_result_supervisor(self.status.get_msgs(),
                                                                                        round_num,
                                                                                        self.executor_result)
            else:
                self.supervisor_result,confirm, to_executor=["","True",single_ai]
            self.status.supervisor_result=self.supervisor_result
            # 在此处向GUI传输监察者的输出

            if confirm=="False":
                print("监察者进行了驳回")
                continue

            # 执行命令
            self.execute(self.executor_result)
            self.status.stdout=self.stdout
            self.status.stderr=self.stderr
            # 在此处向GUI传输系统输出信息

            time.sleep(1)
            if self.exit != 0:
                break

            round_num+=1
            print(round_num,'----------------------------------------------------------------------\n\n')

        # 结束循环后，将AI记忆，powershell状态，以及别的信息全部返回
        return self.setting,self.status

# ----------------------------------------------------------------------------------------------------------------------
    # 获取执行者响应
    def get_result_executor(self,msg,round_num, confirm, to_executor):
        system_msg = executor_system_prompt(
            user=self.setting.user,
            system=self.setting.system,
            language=self.setting.language,
            time=str(datetime.now(ZoneInfo("Asia/Shanghai"))),
            num=round_num,
            msg=msg,
            executor_grammar=self.Grammar
        )
        cmd_output = executor_user_msg(
            stdout=self.stdout,
            stderr=self.stderr,
            supervisor_msg = confirm + "\n" + to_executor
        )
        # 尝试得到ai的响应
        try:
            executor_result, self.setting.executor_memory = get_response_from_llm(
                msg=cmd_output,
                client=self.setting.executor_client,
                model=self.setting.test_model,
                system_message=system_msg,
                msg_history=self.setting.executor_memory,
                print_debug=False,  # 开启调试输出
                temperature=self.setting.temperature
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
    def get_result_supervisor(self,msg,round_num,executor_result):
        system_msg = supervisor_system_prompt(
            user = self.setting.user,
            system = self.setting.system,
            language = self.setting.language,
            time = str(datetime.now(ZoneInfo("Asia/Shanghai"))),
            num = round_num,
            msg = msg,
            supervisor_grammar = supervisor_grammar,
            executor_grammar = self.Grammar
        )
        cmd_output = supervisor_user_msg(
            stdout = self.stdout,
            stderr = self.stderr,
            executor_msg = executor_result
        )

        confirm = "True"
        to_executor = ''
        while True:
            try:
                supervisor_result, self.setting.supervisor_memory = get_response_from_llm(
                    msg = cmd_output,
                    client = self.setting.supervisor_client,
                    model = self.setting.test_model,
                    system_message = system_msg,
                    msg_history = self.setting.supervisor_memory,
                    print_debug = False,  # 开启调试输出
                    temperature = self.setting.temperature
                )
                if self.setting.LLM_print:
                    print('监察者输出:\n', supervisor_result)
            except Exception as e:
                print(f"\n运行时错误: {str(e)}")
                if "AuthenticationError" in str(e):
                    print("请检查API密钥是否正确设置")
                elif "RateLimitError" in str(e):
                    print("API调用限额已用尽，请稍后重试")

            result_json = json_parser(supervisor_result)

            # 判断不为None,且存在"confirm",且"confirm"是"True"或"False"
            if result_json is not None and "confirm" in result_json and result_json["confirm"] in {"True", "False"}:
                confirm = result_json["confirm"]
                if "add_log" in result_json:
                    now_time = str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19]
                    self.setting.supervisor_log.write(time=now_time, msg=result_json["add_log"].strip())
                if "to_executor" in result_json:
                    to_executor = result_json["to_executor"]
                return supervisor_result,confirm, to_executor
            else:
                cmd_output = error_msg
                print("监察者json解析失败")
                continue

# ----------------------------------------------------------------------------------------------------------------------
    # 执行AI的指令
    def execute(self, executor_result):
        now_time = str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19]

        # 解析json为列表
        result_json = json_parser_push(executor_result)

        # 执行列表中的所有指令
        self.stdout = ''
        self.stderr = ''
        for id, cmd in enumerate(result_json):
            stdout = 'Empty'
            stderr = 'Empty'

            if cmd is not None and "type" in cmd:
                if "add_log" in cmd:
                    self.setting.executor_log.write(time=now_time, msg=cmd["add_log"].strip())

                # 根据Type选择相应的方法，并进行操作, 如果没有该Type, 使用报错函数
                Type = cmd["type"]
                stdout, stderr = self.method.get(Type, self.none)(cmd)

            else:
                stderr = error_msg

            self.stdout += f'第{id + 1}条json的输出:\n{stdout}\n'
            self.stderr += f'第{id + 1}条json的报错:\n{stderr}\n'

        if self.setting.stdout_print:
            print('输出:\n', self.stdout)
        if self.setting.stderr_print:
            print('错误:\n', self.stderr)

# ----------------------------------------------------------------------------------------------------------------------
    # 退出工作状态
    def Exit(self,msg):
        if msg["confirm"]=="true":
            self.exit=1
            return "停止工作",""
        else:
            return "","未确认关闭"

    # type不存在
    def none(self,msg):
        return "","使用了不存在的type，请重试"

if __name__ =="__main__":
    msg='''
请尝试在命令行中打印一些文字
'''
    my_status = status()
    my_status.user_msg=[msg]
    my_setting = setting(language="zh")
    my_setting,my_status = work_cycle(setting=my_setting,status=my_status).cycle()

