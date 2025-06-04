from datetime import datetime
from sys import stdout
from zoneinfo import ZoneInfo
import json
import time

from brain import PowerShellSession
from brain import system_prompt, grammar, user_msg,error_msg
from brain import create_client, get_response_from_llm
from brain import extract_json_between_markers,json_parser
from brain import log

from more_Types import Name_TextEditor,TextEditor_user_manual,TextEditor

"""
while Ture:
    得到LLM响应->执行命令->输出传回LLM
"""

class main_cycle:
    def __init__(self,user='wqws',model_name="deepseek-chat"
                                             "",log_path=r"logs\log_ai_executor.txt"):
        self.test_model = model_name
        self.user=user

        self.powershell = PowerShellSession()                         # 创建powershell
        self.client, self.test_model = create_client(self.test_model) # 创建客户端
        self.log=log(log_path)                                        # 打开日志

        self.msg_history = None
        self.llm_result = None
        self.stdout = ''
        self.stderr = ''
        self.round_num = 1

    def cycle(self,language,max_rounds=None,temperature=0.75,msg='无',
              LLM_print=True, stderr_print=True, stdout_print=True):

        # 将所有type对应的操作方法存储在字典
        method = {}
        method["powershell"] = self.powershell.execute_command
        method["read_log"] = self.log.read
        method["exit"] = self.close
        method[Name_TextEditor] = TextEditor.execute

        Grammar= grammar + TextEditor_user_manual

        # 进入主循环
        while True:

            # 生成字符串，用于发送给ai
            system_msg = system_prompt.format(
                user= self.user,
                language=language,
                Time=str(datetime.now(ZoneInfo("Asia/Shanghai"))),
                num=self.round_num,
                msg=msg
            ) + Grammar

            cmd_output = user_msg.format(
                stdout= self.stdout,
                stderr= self.stderr
            )
            self.stdout = 'None'
            self.stderr = 'None'

            # 尝试得到ai的响应
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

            now_time = str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19]
            # result_json= extract_json_between_markers(self.llm_result)
            result_json= json_parser(self.llm_result)

            # 如果json解析成功
            if result_json is not None and "type" in result_json:
                Type=result_json["type"]

                if "add_log" in result_json:
                    print(result_json["add_log"].strip())
                    self.log.write(time=now_time, msg=result_json["add_log"].strip())

                # 根据Type选择相应的方法，并进行操作
                self.stdout,self.stderr = method[Type](result_json)

            # 如果json无法解析
            else:
                self.stderr=error_msg
                continue

            if stdout_print:
                print('输出:\n',self.stdout)
            if stderr_print:
                print('错误:\n',self.stderr)

            time.sleep(3)
            if max_rounds is not None and self.round_num==max_rounds:
                return

            if self.stdout=="<__exit__>":
                return

            self.round_num+=1
            print(self.round_num,'----------------------------------------------------------------------\n\n')

    # 关闭方法
    def close(self,msg):
        if msg["confirm"]=="true":
            self.log.flush_buffer()
            self.powershell.close()
            return "<__exit__>",""
        else:
            return "","未确认关闭"

if __name__ =="__main__":
    msg='''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
请你尝试使用TextEditor的操作方法，读取README.md文件，并将42到48行抄写到test.txt。
如果没有报错，README.md的英文部分全部抄入。
'''

    xxx=main_cycle()
    xxx.cycle(language="zh",max_rounds=30,msg=msg)
