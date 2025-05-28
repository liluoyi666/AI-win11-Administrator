from main_cycle import main_cycle

def work():
    msg = '''
如果刚开始进入命令行，你会出现在该项目的主文件夹中，其中logs/ai_log.txt是你的日志，你可以记录一些东西，以及想对开发者说的东西。
主文件夹中有个空的requirements.txt，project_copy文件夹是项目的副本，供你查看项目的信息。将项目需要依赖写进requirements.txt。
另外，直接读取文件时会导致中文字符串乱码，可能需要使用 -Encoding utf8后缀。
在你进行操作期间，开发者无法向你传递任何指令，当你遭遇不可解决的报错，请创建一个文件并记录。
    '''

    xxx = main_cycle(msg=msg)
    xxx.cycle(max_rounds=30)

if __name__ =="__main__":
    work()