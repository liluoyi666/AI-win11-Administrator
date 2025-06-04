from datetime import datetime
from sys import stdout
from zoneinfo import ZoneInfo
import json
import time

from brain import PowerShellSession
from brain import executor_system_prompt,executor_grammar,executor_user_msg,error_msg
from brain import supervisor_system_prompt,supervisor_user_msg,supervisor_grammar
from brain import create_client, get_response_from_llm
from brain import extract_json_between_markers,json_parser
from brain import log

from more_Types import Name_TextEditor,TextEditor_user_manual,TextEditor

"""
while Ture:
    得到LLM响应->执行命令->输出传回LLM
"""

class main_cycle_double:
    def __init__(self,user='wqws',model_name="deepseek-chat",system="win11",
                 executor_log_path=r"logs\log_ai_executor.txt",supervisor_log_path=r"logs\log_ai_supervisor.txt"):
        self.test_model = model_name
        self.user=user
        self.system=system

        self.powershell = PowerShellSession()   # 创建powershell

        self.executor_client, self.test_model = create_client(self.test_model)      # 创建执行者客户端
        self.executor_log=log(executor_log_path)                                    # 打开执行者日志
        self.executor_memory = None                                                 # 执行者记忆
        self.executor_result = None                                                 # 执行者上一轮返回

        self.supervisor_client, self.test_model = create_client(self.test_model)    # 创建监察者客户端
        self.supervisor_log=log(supervisor_log_path)                                # 打开监察者日志
        self.supervisor_memory = None                                               # 监察者记忆
        self.supervisor_result = None                                               # 监察者上一轮返回
        self.confirm=""                                                             # 监察者是否确认
        self.to_executor=""                                                         # 监察者对执行者

        self.stdout = ''
        self.stderr = ''
        self.round_num = 1

        print('系统初始化完成----------------------------------------------------------------------')


    def cycle(self,language,max_rounds=None,temperature=0.75,msg='无',
              LLM_print=True, stderr_print=True, stdout_print=True):

        # 将所有type对应的操作方法存储在字典
        method = {}
        method["powershell"] = self.powershell.execute_command
        method["read_log"] = self.executor_log.read
        method["exit"] = self.close
        method[Name_TextEditor] = TextEditor.execute

        Grammar= executor_grammar + TextEditor_user_manual

        # 进入主循环
        while True:

            # 生成字符串，用于发送给执行者ai
            executor_system_msg = executor_system_prompt(
                user= self.user,
                system=self.system,
                language=language,
                time=str(datetime.now(ZoneInfo("Asia/Shanghai"))),
                num=self.round_num,
                msg=msg,
                executor_grammar=executor_grammar
            )
            executor_last_round_output = executor_user_msg(
                stdout= self.stdout,
                stderr= self.stderr,
                supervisor_msg=self.confirm+"\n"+self.to_executor
            )

            # 尝试得到执行者ai的响应
            try:
                self.executor_result, self.executor_memory = get_response_from_llm(
                    msg=executor_last_round_output,
                    client=self.executor_client,
                    model=self.test_model,
                    system_message=executor_system_msg,
                    msg_history=self.executor_memory,
                    print_debug=False,  # 开启调试输出
                    temperature=temperature
                )
                if LLM_print:
                    print('执行者输出:\n',self.executor_result)
            except Exception as e:
                print(f"\n运行时错误: {str(e)}")
                if "AuthenticationError" in str(e):
                    print("请检查API密钥是否正确设置")
                elif "RateLimitError" in str(e):
                    print("API调用限额已用尽，请稍后重试")


            # 生成字符串，用于发送给监察者ai
            supervisor_system_msg = supervisor_system_prompt(
                user= self.user,
                system=self.system,
                language=language,
                time=str(datetime.now(ZoneInfo("Asia/Shanghai"))),
                num=self.round_num,
                msg=msg,
                supervisor_grammar=supervisor_grammar,
                executor_grammar=Grammar
            )
            supervisor_last_round_output = supervisor_user_msg(
                stdout= self.stdout,
                stderr= self.stderr,
                executor_msg=self.executor_result
            )

            self.stdout = 'None'
            self.stderr = 'None'

            while True:
                try:
                    self.supervisor_result, self.supervisor_memory = get_response_from_llm(
                        msg=supervisor_last_round_output,
                        client=self.supervisor_client,
                        model=self.test_model,
                        system_message=supervisor_system_msg,
                        msg_history=self.supervisor_memory,
                        print_debug=False,  # 开启调试输出
                        temperature=temperature
                    )
                    if LLM_print:
                        print('监察者输出:\n',self.supervisor_result)
                except Exception as e:
                    print(f"\n运行时错误: {str(e)}")
                    if "AuthenticationError" in str(e):
                        print("请检查API密钥是否正确设置")
                    elif "RateLimitError" in str(e):
                        print("API调用限额已用尽，请稍后重试")

                supervisor_last_round_output=error_msg

                supervisor_result_json=json_parser(self.supervisor_result)
                if supervisor_result_json is not None and "confirm" in supervisor_result_json:
                    if supervisor_result_json["confirm"]=="True" or supervisor_result_json["confirm"]=="False":
                        self.confirm=supervisor_result_json["confirm"]
                    else:
                        print("监察者json关键键错误")
                        continue

                    if "add_log" in supervisor_result_json:
                        now_time = str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19]
                        self.supervisor_log.write(time=now_time, msg=supervisor_result_json["add_log"].strip())
                    if "to_executor" in supervisor_result_json:
                        self.to_executor=supervisor_result_json["to_executor"]
                    break
                else:
                    print("监察者json解析失败")
                    continue

            if self.confirm=="False":
                print("监察者进行了驳回")
                continue

            now_time = str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19]
            executor_result_json= json_parser(self.executor_result)

            # 如果json解析成功
            if executor_result_json is not None and "type" in executor_result_json:
                Type=executor_result_json["type"]

                if "add_log" in executor_result_json:
                    self.executor_log.write(time=now_time, msg=executor_result_json["add_log"].strip())

                # 根据Type选择相应的方法，执行指令
                self.stdout,self.stderr = method[Type](executor_result_json)

            # 如果json无法解析
            else:
                self.stderr=error_msg

            if stdout_print:
                print('输出:\n',self.stdout)
            if stderr_print:
                print('错误:\n',self.stderr)

            time.sleep(10)
            if max_rounds is not None and self.round_num==max_rounds:
                return

            if self.stdout=="<__exit__>":
                return

            self.round_num+=1
            print(self.round_num,'----------------------------------------------------------------------\n\n')

    # 关闭方法
    def close(self,msg):
        if msg["confirm"]=="true":
            self.executor_log.flush_buffer()
            self.supervisor_log.flush_buffer()
            self.powershell.close()
            return "<__exit__>",""
        else:
            return "","未确认关闭"

if __name__ =="__main__":
    msg='''
我想测试监察者的驳回能力是否生效。
请执行者随意进行一个操作，监察者进行驳回
如果驳回成功，请在日志中记录
'''

    xxx=main_cycle_double()
    xxx.cycle(language="zh",max_rounds=30,msg=msg)
