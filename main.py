from main_cycle_double import main_cycle_double
from main_cycle_single import main_cycle_single

def work():

    # What you want to say to AI, what you want AI to do, Please write below.
    msg = '''
帮我创建个文件夹，在里面写一个gan图像生成代码。生成器，判别器，模型主体分开三个文件。并验证前向传播。
'''

    # The language you use
    language="Chinese"

    system = main_cycle_single(model_name="deepseek-chat", log_path=r"logs/log_ai_executor.txt")
    system.cycle(language=language,max_rounds=100,msg=msg)

if __name__ =="__main__":
    work()
