from main_cycle_double import main_cycle_double
from main_cycle_single import main_cycle_single

def one_AI_work():

    # What you want to say to AI, what you want AI to do, Please write below.
    msg = '''

'''

    language="Chinese"

    system = main_cycle_single(user='wqws',language=language,model_name="deepseek-chat")
    system.cycle(max_rounds=100,msg=msg)


def two_AI_work():

    # What you want to say to AI, what you want AI to do, Please write below.
    msg = '''
尝试读取README.md,然后将前二十行抄入到test.txt中
'''

    language="Chinese"

    system = main_cycle_double(user='wqws',language=language,model_name="deepseek-chat")
    system.cycle(max_rounds=100,msg=msg)


if __name__ =="__main__":
    # one_AI_work()
    two_AI_work()
