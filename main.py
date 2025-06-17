from work_cycle import work_cycle
def run(user,language,model_name,system,num_AI,max_rounds,msg):
    cycle=work_cycle(user,language,model_name,system)
    cycle.cycle(num_AI,max_rounds,msg)
    cycle.close()

if __name__ =="__main__":
# 你希望对AI说什么，让它做什么？请写进msg /What do you want to say to AI and want AI to do? Please write in the "msg".
    msg="""
我希望你能编写一个huggingface transformers的电子教材，包括其基础语法，以及模型调用，参数微调，模型结构修改等操作实例。
你可以进行多次追加写入，读取。使用markdown文件写入，把文件创建在当前文件夹
"""
    user = "wqws"               # 你的名字/Your name
    language="Zh"               # 语言/Language
    model_name="deepseek-chat"  # 模型名称/Model name
    max_rounds=30               # AI操作轮次/AI operation rounds
    system='win11'              # 电脑系统(只能win)/Computer system(only win)
    num_AI=1                    # AI个数(1或2)/Number of AI(1 or 2)

    run(user,language,model_name,system,num_AI,max_rounds,msg)
