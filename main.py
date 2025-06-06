from main_cycle_double import main_cycle_double
from main_cycle_single import main_cycle_single


def one_AI_work():

    # What you want to say to AI, what you want AI to do, Please write below.
    msg = '''

'''

    # The language you use
    language="Chinese"

    system = main_cycle_single(model_name="deepseek-chat")
    system.cycle(language=language,max_rounds=100,msg=msg)



def two_AI_work():

    # What you want to say to AI, what you want AI to do, Please write below.
    msg = '''
我修改了json的解析方法，你现在可以在一次输入中包含多个json，系统会按顺序执行json中的命令。
你们先获取当前文件夹位置。
然后请你尝试在一次输入中，连续创建并写入三个文件，在当前文件夹，下一次输入一次性读取这些文件
'''

    # The language you use
    language="Chinese"

    system = main_cycle_double(model_name="deepseek-chat")
    system.cycle(language=language,max_rounds=100,msg=msg)


if __name__ =="__main__":
    # one_AI_work()
    two_AI_work()
