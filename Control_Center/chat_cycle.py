from datetime import datetime
from sys import stdout
from zoneinfo import ZoneInfo
import json
import time

from brain import executor_chat_prompt,supervisor_chat_prompt
from brain import PowerShellSession
from brain import create_client, get_response_from_llm

from Control_Center import setting,status

class chat:
    def __init__(self,set:set,status:status):

        self.set = set
        self.status = status

        self.to_executor = ''
        self.to_supervisor = ''

        self.status.executor_result = ''
        self.status.supervisor_result = ''


    def cycle(self):
        while True:
            # 在每次循环开始时，接收用户是否exit,增加msg,切换AI个数
            if self.status.exit != 1:
                break

