from datetime import datetime
from sys import stdout
from zoneinfo import ZoneInfo
import json
import time

from brain import PowerShellSession
from brain import system_prompt, grammar, user_msg,error_msg
from brain import create_client, get_response_from_llm,extract_json_between_markers,extract_json_between_markers1

class main_cycle:
    def __init__(self,user='wqws',model_name="deepseek-coder"):
        self.test_model = model_name
        self.user=user

        self.powershell = PowerShellSession()
        self.client, self.test_model = create_client(self.test_model) #创建客户端

        self.msg_history = None
        self.llm_result = None
        self.stdout = 'None'
        self.stderr = 'None'
        self.round_num = 0

    def cycle(self,max_rounds=None,temperature=0.75):
        while True:
            system_msg = system_prompt.format(
                user= self.user,
                num=self.round_num,
                Time= str(datetime.now(ZoneInfo("Asia/Shanghai")))
            ) + grammar
            cmd_output = user_msg.format(
                stdout= self.stdout,
                stderr= self.stderr
            )

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
                print('-------------------------------------------------------\n\n',self.round_num,'\n')
                print('llm_output:\n',self.llm_result)

            except Exception as e:
                print(f"\n运行时错误: {str(e)}")
                if "AuthenticationError" in str(e):
                    print("请检查API密钥是否正确设置")
                elif "RateLimitError" in str(e):
                    print("API调用限额已用尽，请稍后重试")

            result_json= extract_json_between_markers(self.llm_result)

            self.stdout = 'None'
            self.stderr = 'None'

            if result_json["command"]=='exit':
                self.powershell.close()

            if result_json is not None:
                cmd_result = self.powershell.execute_command(result_json["command"])

                self.stdout=cmd_result['stdout']
                self.stderr=cmd_result['stderr']

            else:
                self.stderr=error_msg

            print('输出:\n',self.stdout)
            print('错误:\n',self.stderr)

            time.sleep(3)

            self.round_num+=1
            if max_rounds is not None and self.round_num==max_rounds:
                break;

        self.powershell.close()

if __name__ =="__main__":
    xxx=main_cycle()
    xxx.cycle(max_rounds=30)
