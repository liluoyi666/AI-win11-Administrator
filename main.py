from main_cycle import main_cycle

def work():
    msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中，其中logs/ai_log.txt是你的日志，你可以记录一些东西，以及想对开发者说的东西。
有一个README.md，用于在github上介绍该项目，请你创建出他的中文版本，并保存在另一个文件里。
另外，直接读取文件时会导致中文字符串乱码，可能需要使用 -Encoding utf8后缀。
在你进行操作期间，开发者无法向你传递任何指令，当你遭遇不可解决的报错，请创建一个文件并记录。
'''

    xxx = main_cycle()
    xxx.cycle(max_rounds=30,msg=msg)

if __name__ =="__main__":
    work()