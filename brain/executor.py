import subprocess
import threading
import queue
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import uuid


class PowerShellSession:
    def __init__(self):
        self.process = None
        self.stdout_queue = queue.Queue()
        self.stderr_queue = queue.Queue()
        self.lock = threading.Lock()  # 线程锁防止并发冲突

        self._start_process()         # 调用函数, 生成powershell类
        self._start_output_reader()   # 启动输出读取线程

    # 生成powershell类
    def _start_process(self):
        self.process = subprocess.Popen(
            ['powershell.exe', '-NoExit'],
            stdin=subprocess.PIPE,      # 输入通道
            stdout=subprocess.PIPE,     # 输出通道
            stderr=subprocess.PIPE,     # 错误通道
            text=True,
            bufsize=1,
            universal_newlines=True
        )

    # 输出读取线程
    def _start_output_reader(self):
        # 定义一个用于读取的函数
        def reader(queue, stream):
            while True:
                line = stream.readline()
                if not line:  # 流关闭时退出循环
                    break
                queue.put(line)

        # 定义两个保护进程，并启动
        threading.Thread(target=reader, args=(self.stdout_queue, self.process.stdout), daemon=False).start()
        threading.Thread(target=reader, args=(self.stderr_queue, self.process.stderr), daemon=False).start()

    def execute_command(self, command, timeout=10):
        with self.lock:  # 确保命令顺序执行
            if self.process.poll() is not None:     #如果进程不存在
                raise RuntimeError("PowerShell process is not running")

            end_marker = str(uuid.uuid4())
            start_time = time.time()
            beijing_time = datetime.now(ZoneInfo("Asia/Shanghai"))
            full_cmd = f"{command}; Write-Output '该命令开始执行的时间{beijing_time}'\n Write-Output '{end_marker}'\n"      #组合命令
            self.process.stdin.write(full_cmd)      #输入
            self.process.stdin.flush()

            output = []
            while True:
                try:
                    line = self.stdout_queue.get(timeout=3)
                    if end_marker in line:
                        break
                    output.append(line.strip())
                except queue.Empty:
                    if time.time() - start_time > timeout:
                        raise TimeoutError("Command execution timed out")
            # 可选：读取错误流中的内容
            stderr_output = []
            while not self.stderr_queue.empty():
                stderr_output.append(self.stderr_queue.get().strip())
            return {
                'stdout': '\n'.join(output),        # 标准输出
                'stderr': '\n'.join(stderr_output)  # 标准错误
            }

    def close(self):
        if self.process and self.process.poll() is None:
            self.process.stdin.write("exit\n")
            self.process.stdin.flush()
            self.process.wait(timeout=5)

if __name__ =="__main__":
    powershell = PowerShellSession()
    try:
        result = powershell.execute_command(r'cd C:\Users\liluoyi')
        result = powershell.execute_command('XXXXYG')
        print("STDOUT:\n", result['stdout'])
        print("STDERR:\n", result['stderr'])
    finally:
        powershell.close()