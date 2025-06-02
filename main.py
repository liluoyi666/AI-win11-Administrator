from main_cycle import main_cycle

def work():

    # 你想对AI说的，希望AI做的，请写在下面。
    # What you want to say to AI, what you want AI to do, Please write below.
    msg = '''
请帮我生成一个cnn模型文件，并保存在该文件夹。
Please help me generate a cnn model file and save it in this folder
'''

    # 你使用的语言
    # The language you use
    language="Chinese"

    system = main_cycle(model_name="deepseek-reasoner ",log_path=r"logs\log_ai.txt")
    system.cycle(language=language,max_rounds=100,msg=msg)

if __name__ =="__main__":
    work()
