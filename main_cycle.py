from datetime import datetime
from sys import stdout
from zoneinfo import ZoneInfo
import json
import time

from brain import PowerShellSession
from brain import system_prompt, grammar, user_msg,error_msg
from brain import create_client, get_response_from_llm
from brain import extract_json_between_markers

"""
while Ture:
    得到LLM响应->执行命令->输出传回LLM
"""

class main_cycle:
    def __init__(self,user='wqws',model_name="deepseek-coder"):
        self.test_model = model_name
        self.user=user

        self.powershell = PowerShellSession()
        self.client, self.test_model = create_client(self.test_model) #创建客户端

        self.msg_history = None
        self.llm_result = None
        self.stdout = ''
        self.stderr = ''
        self.round_num = 0

    def cycle(self,max_rounds=None,temperature=0.75,msg='无',
              LLM_print=True, stderr_print=True, stdout_print=True
              ):
        while True:
            self.round_num+=1
            print(self.round_num,'----------------------------------------------------------------------\n\n')

            system_msg = system_prompt.format(
                user= self.user,
                Time=str(datetime.now(ZoneInfo("Asia/Shanghai"))),
                num=self.round_num,
                msg=msg
            ) + grammar
            cmd_output = user_msg.format(
                stdout= self.stdout,
                stderr= self.stderr
            )
            self.stdout = 'None'
            self.stderr = 'None'

            try:
                self.llm_result, self.msg_history = get_response_from_llm(
                    msg=cmd_output,
                    client=self.client,
                    model=self.test_model,
                    system_message=system_msg,
                    msg_history=self.msg_history,
                    print_debug=False,  # 开启调试输出
                    temperature=temperature
                )
                if LLM_print:
                    print('llm_output:\n',self.llm_result)
            except Exception as e:
                print(f"\n运行时错误: {str(e)}")
                if "AuthenticationError" in str(e):
                    print("请检查API密钥是否正确设置")
                elif "RateLimitError" in str(e):
                    print("API调用限额已用尽，请稍后重试")

            result_json= extract_json_between_markers(self.llm_result)

            if result_json is not None:
                if result_json["command"] == 'exit':
                    self.powershell.close()

                self.stdout,self.stderr = self.powershell.execute_command(result_json["command"])
            else:
                self.stderr=error_msg

            if stdout_print:
                print('输出:\n',self.stdout)
            if stderr_print:
                print('错误:\n',self.stderr)

            time.sleep(3)
            if max_rounds is not None and self.round_num==max_rounds:
                break;

        self.powershell.close()

if __name__ =="__main__":
    msg='''
如果刚开始进入命令行，你会出现在该项目的主文件夹中，其中logs/ai_log.txt是你的日志，你可以记录一些东西，以及想对开发者说的东西。
其中有个README.md是未完成的项目介绍,project_copy文件夹是项目的副本，我希望你查看项目的一些信息，然后完成markdown。
另外，直接读取文件时会导致中文字符串乱码，可能需要使用 -Encoding utf8后缀。
在你进行操作期间，开发者无法向你传递任何指令，当你遭遇不可解决的报错，请创建一个文件并记录。'''

    xxx=main_cycle()
    xxx.cycle(max_rounds=30,msg=msg)
