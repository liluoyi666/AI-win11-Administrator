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
    def __init__(self,user='wqws',system='win11',language='En',model_name="deepseek-chat",temperature=0.75,
                 log_path=r"logs\log_ai_executor.txt",
                 LLM_print=True, stderr_print=True, stdout_print=True):

        self.test_model = model_name        # 模型名称
        self.user=user                      # 用户
        self.system=system                  # 计算机系统
        self.language=language              # 用户语言
        self.temperature=temperature        # 生成自由度

        self.LLM_print=LLM_print            # 是否打印AI输出
        self.stderr_print=stderr_print      # 是否打印系统输出
        self.stdout_print=stdout_print      # 是否打印系统错误

        self.powershell = PowerShellSession()                           # 创建powershell

        self.client, self.test_model = create_client(self.test_model)   # 创建API客户端
        self.log=log(log_path)                                          # 创建日志服务
        self.executor_memory = None                                     # AI记忆

        self.stdout = ''            # 系统输出
        self.stderr = ''            # 系统报错
        self.exit = 0               # 退出标记

        # 将所有type对应的操作方法存储在字典
        self.method = {}
        self.method["powershell"] = self.powershell.execute_command
        self.method["read_log"] = self.log.read
        self.method["exit"] = self.exit
        self.method[Name_TextEditor] = TextEditor.execute

        # AI用操作手册
        self.Grammar= executor_grammar + TextEditor_user_manual

        print('系统初始化完成')

# ----------------------------------------------------------------------------------------------------------------------
    # 循环
    def cycle(self,max_rounds=None,msg='无'):
        round_num = 1
        while True:
            # 获取AI的响应
            executor_result=self.get_result_executor(msg,round_num)

            # 解析响应，并执行指令
            self.execute(executor_result)

            time.sleep(1)

            if max_rounds is not None and round_num==max_rounds:
                break
            if self.exit==1:
                break

            round_num+=1
            print(round_num,'---------------------------------------------------------------------------------\n\n')
        self.close()

# ----------------------------------------------------------------------------------------------------------------------
    # 获取执行者响应
    def get_result_executor(self,msg,round_num):
        system_msg = system_prompt(
            user=self.user,
            system=self.system,
            language=self.language,
            time=str(datetime.now(ZoneInfo("Asia/Shanghai"))),
            num=round_num,
            msg=msg,
            grammar=self.Grammar
        )
        cmd_output = user_msg(
            stdout=self.stdout,
            stderr=self.stderr
        )

        # 尝试得到ai的响应
        try:
            executor_result, self.executor_memory = get_response_from_llm(
                msg=cmd_output,
                client=self.client,
                model=self.test_model,
                system_message=system_msg,
                msg_history=self.executor_memory,
                print_debug=False,  # 开启调试输出
                temperature=self.temperature
            )
            if self.LLM_print:
                print('executor_result:\n', executor_result)
        except Exception as e:
            print(f"\n运行时错误: {str(e)}")
            if "AuthenticationError" in str(e):
                print("请检查API密钥是否正确设置")
            elif "RateLimitError" in str(e):
                print("API调用限额已用尽，请稍后重试")

        return executor_result

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
                    self.log.write(time=now_time, msg=cmd["add_log"].strip())

                # 根据Type选择相应的方法，并进行操作, 如果没有该Type, 使用报错函数
                Type = cmd["type"]
                stdout, stderr = self.method.get(Type, self.none)(cmd)

            else:
                stderr = error_msg

            self.stdout += f'第{id + 1}条json的输出:\n{stdout}\n'
            self.stderr += f'第{id + 1}条json的报错:\n{stderr}\n'

        if self.stdout_print:
            print('输出:\n', self.stdout)
        if self.stderr_print:
            print('错误:\n', self.stderr)

# ----------------------------------------------------------------------------------------------------------------------
    # 退出工作状态
    def exit(self,msg):
        if msg["confirm"]=="true":
            self.exit=1
            return "停止工作",""
        else:
            return "","未确认关闭"

    # 完全关闭
    def close(self):
        self.log.flush_buffer()
        self.powershell.close()

    # type不存在
    def none(self,msg):
        return "","使用了不存在的type，请重试"

if __name__ =="__main__":
    msg='''
尝试读取README.md,然后将前二十行抄入到test.txt中
'''

    xxx=main_cycle_single(language="zh",model_name="deepseek-chat")
    xxx.cycle(max_rounds=30,msg=msg)
