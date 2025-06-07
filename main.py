from main_cycle_dual import main_cycle_dual
from main_cycle_single import main_cycle_single
def one_AI_work(user,language,msg,max_rounds):
    system = main_cycle_single(user=user,language=language,model_name="deepseek-chat")
    system.cycle(max_rounds=max_rounds,msg=msg)
def two_AI_work(user,language,msg,max_rounds):
    system = main_cycle_dual(user=user,language=language,model_name="deepseek-chat")
    system.cycle(max_rounds=max_rounds,msg=msg)
def run(user,language,msg,max_rounds=30):
    print("请选择模式(单AI或双AI)/please select a mode(Single-AI or Dual-AI)")
    select=int(input("1 or 2:").strip())
    if select==1:
        one_AI_work(user, language, msg, max_rounds=30)
    if select==2:
        two_AI_work(user, language, msg, max_rounds)

if __name__ =="__main__":
    user = "wqws"
    # 你希望对AI说什么，让它做什么？请写进msg /What do you want to say to AI and want AI to do? Please write in the "msg".
    msg="""
请尝试读取README.md，将其前20行抄写在test.txt文件中
"""

    # 语言/language
    language="Zh"

    # 最大轮数/max_rounds
    max_rounds=30






    run(user,msg,language)
