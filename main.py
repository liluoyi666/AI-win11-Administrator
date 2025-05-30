from main_cycle import main_cycle

def work():
    msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中。
由于当前项目的json解析器仍有较高的报错率，且只能检测一个json结构，我希望你根据当前项目的信息设计出一个更优秀的json解析器。
要求：
能够识别```json{...}```包裹的json。
能够识别多个连续的该类型的json，并返回一个列表。
'''

    xxx = main_cycle(log_path=r"logs\log_ai.txt")
    xxx.cycle(max_rounds=30,msg=msg)

if __name__ =="__main__":
    work()