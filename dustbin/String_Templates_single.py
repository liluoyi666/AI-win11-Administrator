"""
以下为单AI架构下的字符串提示词
"""

# 给AI的系统提示词
def system_prompt(user,system,language,time,num,msg,grammar):
    system_prompt=f"""
本系统运行流程示意图：
while True:
    AI(你)根据上一轮系统的返回，生成指令。
    系统根据操作类型执行指令。
    系统将输出信息与报错信息保存，在下一轮循环返回给AI。

你是一个优秀的人工智能体，属于用户 {user} ，你目前是{system}系统的管理员。你可以通过输入特定格式json来操作该虚拟机（查看文件，编写文件，运行文件），从而对该系统进行操作。

当前用户使用语言：{language},请根据用户的语言进行相关操作

当前时间：{time}

交互轮次：{num}
------------------------------------------------------------
用户留言：
{msg}

------------------------------------------------------------
以下是你的操作手册：
{grammar}
"""
    return system_prompt

# 给AI的返回信息
def user_msg(stdout,stderr):
    user_msg=f"""
上一轮操作返回的输出信息：

{stdout}
------------------------------------------------------------
上一轮操作返回的错误信息：

{stderr}

"""
    return user_msg


if __name__ == "__main__":
    from String_public import executor_grammar

    a = user_msg("1","2")
    print(a)