import subprocess
import threading
import queue
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import uuid

"""
创建一个持久化的powershell窗口，能够输入和输出
"""


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
        threading.Thread(target=reader, args=(self.stdout_queue, self.process.stdout), daemon=True).start()
        threading.Thread(target=reader, args=(self.stderr_queue, self.process.stderr), daemon=True).start()

    def execute_command(self, command, timeout=10):
        with self.lock:  # 确保命令顺序执行
            if self.process.poll() is not None:     #如果进程不存在
                raise RuntimeError("PowerShell process is not running")
            command=command["command"]

            if command == 'exit':
                self.close()

            end_marker = str(uuid.uuid4())
            start_time = time.time()
            beijing_time = datetime.now(ZoneInfo("Asia/Shanghai"))
            full_cmd = f'''{command}\n
'''      #组合命令
            self.process.stdin.write(full_cmd)      #输入
            self.process.stdin.write(f"# 该命令开始执行的时间{beijing_time}。end_marker'{end_marker}'\n")
            self.process.stdin.flush()

            output = []
            while True:
                try:
                    line = self.stdout_queue.get(timeout=3)
                    # if end_marker in line:
                    #     break
                    output.append(line.strip())
                    if end_marker in line:
                        break
                except queue.Empty:
                    if time.time() - start_time > timeout:
                        raise TimeoutError("Command execution timed out")

            # 可选：读取错误流中的内容
            stderr_output = []
            while not self.stderr_queue.empty():
                stderr_output.append(self.stderr_queue.get().strip())
            return '\n'.join(output),'\n'.join(stderr_output)

    def close(self):
        if self.process and self.process.poll() is None:
            self.process.stdin.write("exit\n")
            self.process.stdin.flush()
            self.process.wait(timeout=5)

if __name__ =="__main__":
    powershell = PowerShellSession()
    try:
        result,err=powershell.execute_command('''Set-Content -Path SimpleRNN.py -Value \"import torch\nimport torch.nn as nn\n\nclass SimpleRNN(nn.Module):\n    def __init__(self, input_size, hidden_size, num_layers, num_classes):\n        super(SimpleRNN, self).__init__()\n        self.hidden_size = hidden_size\n        self.num_layers = num_layers\n        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)\n        self.fc = nn.Linear(hidden_size, num_classes)\n    \n    def forward(self, x):\n        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)\n        out, _ = self.rnn(x, h0)\n        out = self.fc(out[:, -1, :])\n        return out\" -Encoding utf8''')

        print("1:\n", result)
        result,err=powershell.execute_command("Get-ChildItem")
        print("1:\n", result)

    finally:
        powershell.close()