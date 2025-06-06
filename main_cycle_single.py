from datetime import datetime
from sys import stdout
from zoneinfo import ZoneInfo
import json
import time

from brain import PowerShellSession
from brain import system_prompt, executor_grammar, user_msg, error_msg
from brain import create_client, get_response_from_llm
from brain import json_parser,json_parser_push
from brain import log

from more_Types import Name_TextEditor,TextEditor_user_manual,TextEditor

"""
while Ture:
    得到LLM响应
    执行命令
    输出传回LLM
"""

class main_cycle_single:
    def __init__(self,user='wqws',system='win11',model_name="deepseek-chat",
                 log_path=r"logs\log_ai_executor.txt"):
        self.test_model = model_name
        self.user=user
        self.system=system

        self.powershell = PowerShellSession()                         # 创建powershell
        self.client, self.test_model = create_client(self.test_model) # 创建客户端
        self.log=log(log_path)                                        # 打开日志

        self.msg_history = None
        self.llm_result = None
        self.stdout = ''
        self.stderr = ''
        self.round_num = 1

        self.exit=0
        print('系统初始化完成----------------------------------------------------------------------')

    def cycle(self,language,max_rounds=None,temperature=0.75,msg='无',
              LLM_print=True, stderr_print=True, stdout_print=True):

        # 将所有type对应的操作方法存储在字典
        method = {}
        method["powershell"] = self.powershell.execute_command
        method["read_log"] = self.log.read
        method["exit"] = self.close
        method[Name_TextEditor] = TextEditor.execute

        Grammar= executor_grammar + TextEditor_user_manual

        # 进入主循环
        while True:

            # 生成字符串，用于发送给ai
            system_msg = system_prompt(
                user= self.user,
                system=self.system,
                language=language,
                time=str(datetime.now(ZoneInfo("Asia/Shanghai"))),
                num=self.round_num,
                msg=msg,
                grammar=Grammar
            )

            cmd_output = user_msg(
                stdout= self.stdout,
                stderr= self.stderr
            )

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
            result_json = json_parser_push(self.llm_result)

            self.stdout = ''
            self.stderr = ''

            # 执行列表中的所有指令
            for id,cmd in enumerate(result_json):
                stdout = 'Empty'
                stderr = 'Empty'
                # 如果json解析成功
                if cmd is not None and "type" in cmd:

                    if "add_log" in cmd:
                        self.log.write(time=now_time, msg=cmd["add_log"].strip())

                    # 根据Type选择相应的方法，并进行操作, 如果没有该Type, 使用报错函数
                    Type = cmd["type"]
                    stdout, stderr = method.get(Type, self.none)(cmd)

                # 如果json无法解析
                else:
                    stderr = error_msg

                self.stdout += f'第{id + 1}条json的输出:\n{stdout}\n'
                self.stderr += f'第{id + 1}条json的报错:\n{stderr}\n'

            if stdout_print:
                print('输出:\n',self.stdout)
            if stderr_print:
                print('错误:\n',self.stderr)

            time.sleep(1)
            if max_rounds is not None and self.round_num==max_rounds:
                return

            if self.exit==1:
                return

            self.round_num+=1
            print(self.round_num,'----------------------------------------------------------------------\n\n')

    # 关闭方法
    def close(self,msg):
        if msg["confirm"]=="true":
            self.log.flush_buffer()
            self.powershell.close()
            self.exit=1
            return "停止工作",""
        else:
            return "","未确认关闭"

    def none(self,msg):
        return "","使用了不存在的type，请重试"

if __name__ =="__main__":
    msg='''
我修改了json的解析方法，你现在可以在一次输入中包含多个json，系统会按顺序执行json中的命令。
你先获取当前文件夹位置。
然后请你尝试在一次输入中，连续创建并写入三个文件，在当前文件夹，下一次输入一次性读取这些文件
'''

    xxx=main_cycle_single()
    xxx.cycle(language="zh",max_rounds=30,msg=msg)
