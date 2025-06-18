import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QLineEdit, QPushButton, QLabel, QSplitter,
                             QGroupBox, QStatusBar, QAction, QMenu, QMenuBar, QComboBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QTextCursor

from Control_Center import setting,status
from Control_Center import work_cycle,chat_cycle

def get_time():
    return str(datetime.now(ZoneInfo("Asia/Shanghai")))[:19]

# 主线程
class AIDesktopAssistant1(QMainWindow):
    def __init__(self, setting, status):
        super().__init__()
        self.setting = setting
        self.status = status
        self.initUI()
        self.init_work_thread()
        self.init_chat_thread()

# ----------------------------------------------------------------------------------------------------------------------
    # 初始化窗口

    def initUI(self):
        # 设置主窗口
        self.setWindowTitle('AI桌面助手')
        self.setGeometry(300, 300, 1000, 700)
        self.setWindowIcon(QIcon('ai_icon.png'))

        # 应用全局样式
        self.applyLightTheme()

        # 创建菜单栏
        self.createMenuBar()

        # 创建主控件
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # 增加内边距

        # 创建状态栏
        status_bar = self.statusBar()
        self.status_label = QLabel(
            f"状态: {'工作中' if self.status.exit == 0 else '聊天中'} | AI数量: {1 if self.status.single_or_dual == 1 else 2}")
        status_bar.addWidget(self.status_label)
        status_bar.setStyleSheet("background-color: #f5f5f5; color: #555; border-top: 1px solid #e0e0e0;")

        # 创建左右分割视图
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(5)  # 增加分割线宽度
        splitter.setStyleSheet("QSplitter::handle { background-color: #e0e0e0; }")

        # 左侧面板 - 聊天/工作区
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)  # 移除内边距

        # 聊天/工作显示区
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 10))  # 使用更现代的字体
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        # 用户输入区
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("输入消息...")
        self.user_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4da6ff;
            }
        """)

        self.send_button = QPushButton("发送")
        self.send_button.setFixedSize(100, 40)  # 增大按钮尺寸
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4da6ff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3d8bdf;
            }
            QPushButton:pressed {
                background-color: #2c7ad9;
            }
        """)
        self.send_button.clicked.connect(self.sendMessage)

        input_layout.addWidget(self.user_input, 9)  # 输入框占9份空间
        input_layout.addWidget(self.send_button, 1)  # 按钮占1份空间

        left_layout.addWidget(self.chat_display, 8)  # 聊天区占8份空间
        left_layout.addWidget(input_widget, 2)  # 输入区占2份空间

        # 右侧面板 - 控制区
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignTop)
        right_layout.setContentsMargins(0, 0, 0, 0)  # 移除内边距
        right_layout.setSpacing(15)  # 增加控件间距

        # 工作控制组
        work_group = QGroupBox("工作控制")
        work_group.setStyleSheet("QGroupBox { font-weight: bold; color: #4da6ff; }")
        work_layout = QVBoxLayout(work_group)
        work_layout.setSpacing(10)  # 增加按钮间距

        self.start_work_button = QPushButton("开始工作")
        self.start_work_button.setStyleSheet(self.getButtonStyle("#4da6ff"))
        self.start_work_button.clicked.connect(self.startWork)
        self.start_work_button.setMinimumHeight(40)  # 增加按钮高度

        self.stop_work_button = QPushButton("开始聊天")
        self.stop_work_button.setStyleSheet(self.getButtonStyle("#4da6ff"))
        self.stop_work_button.clicked.connect(self.startChat)
        self.stop_work_button.setEnabled(False)
        self.stop_work_button.setMinimumHeight(40)

        self.add_comment_button = QPushButton("添加工作留言")
        self.add_comment_button.setStyleSheet(self.getButtonStyle("#4da6ff"))
        self.add_comment_button.clicked.connect(self.addWorkComment)
        self.add_comment_button.setEnabled(True)
        self.add_comment_button.setMinimumHeight(40)

        work_layout.addWidget(self.start_work_button)
        work_layout.addWidget(self.stop_work_button)
        work_layout.addWidget(self.add_comment_button)

        # AI控制组
        ai_group = QGroupBox("AI控制")
        ai_group.setStyleSheet("QGroupBox { font-weight: bold; color: #4da6ff; }")
        ai_layout = QVBoxLayout(ai_group)
        ai_layout.setSpacing(10)

        ai_count_label = QLabel("AI数量:")
        ai_count_label.setStyleSheet("font-weight: normal;")

        self.ai_count_combo = QComboBox()
        self.ai_count_combo.addItem("1个AI")
        self.ai_count_combo.addItem("2个AI")
        self.ai_count_combo.setCurrentIndex(0 if self.status.single_or_dual == 1 else 1)
        self.ai_count_combo.currentIndexChanged.connect(self.changeAICount)
        self.ai_count_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        self.ai_status_label = QLabel(f"当前: {1 if self.status.single_or_dual == 1 else 2}个AI")
        self.ai_status_label.setStyleSheet("font-weight: normal;")

        ai_layout.addWidget(ai_count_label)
        ai_layout.addWidget(self.ai_count_combo)
        ai_layout.addWidget(self.ai_status_label)

        # 系统信息组
        sys_group = QGroupBox("系统信息")
        sys_group.setStyleSheet("QGroupBox { font-weight: bold; color: #4da6ff; }")
        sys_layout = QVBoxLayout(sys_group)
        sys_layout.setSpacing(8)

        self.model_label = QLabel(f"模型: {self.setting.test_model}")
        self.temp_label = QLabel(f"生成自由度: {self.setting.temperature}")
        self.lang_label = QLabel(f"语言: {self.setting.language}")
        self.user_label = QLabel(f"用户: {self.setting.user}")

        # 设置信息标签样式
        for label in [self.model_label, self.temp_label, self.lang_label, self.user_label]:
            label.setStyleSheet(
                "font-weight: normal; padding: 5px; border-radius: 5px; background-color: rgba(77, 166, 255, 0.1);")

        sys_layout.addWidget(self.model_label)
        sys_layout.addWidget(self.temp_label)
        sys_layout.addWidget(self.lang_label)
        sys_layout.addWidget(self.user_label)

        right_layout.addWidget(work_group)
        right_layout.addWidget(ai_group)
        right_layout.addWidget(sys_group)

        # 添加左右面板到分割器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 300])

        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 添加初始消息
        self.addMessage("系统", "AI桌面助手已启动", "system")

    def applyLightTheme(self):
        # 应用全局浅色主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f9f9f9;
            }
            QWidget {
                background-color: #f9f9f9;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 1.5ex;
                padding-top: 10px;
                padding-bottom: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
            QLabel {
                color: #333;
            }
        """)

    def getButtonStyle(self, color):
        # 统一的按钮样式
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.lightenColor(color, 20)};
            }}
            QPushButton:pressed {{
                background-color: {self.darkenColor(color, 20)};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #888888;
            }}
        """

    def lightenColor(self, hex_color, percent):
        # 颜色变亮
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = min(255, r + int(percent * 2.55))
        g = min(255, g + int(percent * 2.55))
        b = min(255, b + int(percent * 2.55))
        return f"#{r:02x}{g:02x}{b:02x}"

    def darkenColor(self, hex_color, percent):
        # 颜色变暗
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = max(0, r - int(percent * 2.55))
        g = max(0, g - int(percent * 2.55))
        b = max(0, b - int(percent * 2.55))
        return f"#{r:02x}{g:02x}{b:02x}"


    def createMenuBar(self):
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件')

        exit_action = QAction(QIcon('exit.png'), '退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出应用')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 视图菜单
        view_menu = menubar.addMenu('视图')

        dark_mode_action = QAction('深色模式', self, checkable=True)
        dark_mode_action.triggered.connect(self.toggleDarkMode)
        view_menu.addAction(dark_mode_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助')

        about_action = QAction('关于', self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)

    def addMessage(self, sender, message, msg_type="user"):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)

        # 根据消息类型设置样式
        if msg_type == "system":
            color = "#6A5ACD"  # 紫色
            prefix = "[系统] "
        elif msg_type == "executor":
            color = "#1E90FF"  # 蓝色
            prefix = "[执行者] "
        elif msg_type == "supervisor":
            color = "#32CD32"  # 绿色
            prefix = "[监查者] "
        elif msg_type == "output":
            color = "#FF8C00"  # 橙色
            prefix = "[输出] "
        elif msg_type == "error":
            color = "#FF4500"  # 红色
            prefix = "[错误] "
        else:
            color = "#4da6ff"  # 主题蓝色
            prefix = "[用户] "

        # 添加时间戳
        timestamp = get_time()
        self.chat_display.setTextColor(QColor("#999999"))
        self.chat_display.setFontWeight(QFont.Normal)
        self.chat_display.setFontPointSize(9)
        self.chat_display.insertPlainText(f"{timestamp} ")

        # 添加消息前缀
        self.chat_display.setTextColor(QColor(color))
        self.chat_display.setFontWeight(QFont.Bold)
        self.chat_display.setFontPointSize(10)
        self.chat_display.insertPlainText(prefix)

        # 添加消息内容
        self.chat_display.setFontWeight(QFont.Normal)
        self.chat_display.setTextColor(QColor("#333333"))
        self.chat_display.insertPlainText(message + "\n\n")

        # 滚动到底部
        self.chat_display.ensureCursorVisible()


    def init_work_thread(self):
        """初始化工作线程并连接信号"""
        self.work_thread = work_cycle()
        self.work_thread.send_status(self.setting, self.status)

        # 连接工作线程的信号到主窗口的槽函数
        self.work_thread.Round_num.connect(self.update_round_num)
        self.work_thread.executor_output.connect(self.update_executor_output)
        self.work_thread.supervisor_output.connect(self.update_supervisor_output)
        self.work_thread.system_stdout.connect(self.update_system_stdout)
        self.work_thread.system_stderr.connect(self.update_system_stderr)
        self.work_thread.work_exit.connect(self.thread_exited)
        self.work_thread.Setting.connect(self.update_settings)

    def init_chat_thread(self):
        """初始化工作线程并连接信号"""
        self.chat_thread = chat_cycle()
        self.work_thread.send_status(self.setting, self.status)

        # 连接工作线程的信号到主窗口的槽函数
        self.chat_thread.Round_num.connect(self.update_round_num)
        self.chat_thread.executor_output.connect(self.update_executor_output)
        self.chat_thread.supervisor_output.connect(self.update_supervisor_output)
        self.chat_thread.system_stderr.connect(self.update_system_stderr)
        self.chat_thread.work_exit.connect(self.thread_exited)
        self.chat_thread.Setting.connect(self.update_settings)

        # 初始化为聊天模式
        self.status.exit=1
        self.chat_thread.send_status(self.setting,self.status)
        self.chat_thread.start()

# ----------------------------------------------------------------------------------------------------------------------
    # 主线程对工作线程的控制

    def startWork(self):
        self.status_label.setText(f"状态: 即将开始工作 | AI数量: {1 if self.status.single_or_dual == 1 else 2}")
        self.chat_thread.Exit()

    def startChat(self):
        self.status_label.setText(f"状态: 即将开始聊天 | AI数量: {1 if self.status.single_or_dual == 1 else 2}")
        self.work_thread.Exit()


    def addWorkComment(self):
        """添加工作留言到工作线程"""
        message = self.user_input.text().strip()
        if message:
            self.addMessage("用户", f"[工作留言]{message}")
            self.user_input.clear()

            self.work_thread.add_msg(f"{get_time()}{message}")

    def changeAICount(self, index):
        self.status.single_or_dual = 1 if index == 0 else 2
        self.ai_status_label.setText(f"当前: {index + 1}个AI")
        self.status_label.setText(f"状态: {'工作中' if self.status.exit == 0 else '聊天中'} | AI数量: {index + 1}")

        self.work_thread.num_AI()
        self.chat_thread.num_AI()

    def sendMessage(self):
        message = f"({get_time()}){self.user_input.text().strip()}"
        if message:
            self.addMessage("用户", message)
            self.user_input.clear()

            self.chat_thread.send_user_msg(message)


# ----------------------------------------------------------------------------------------------------------------------
    # 线程对主线程的控制
    def update_round_num(self, round_num):
        """更新轮次显示"""
        self.status_label.setText(
            f"状态:  轮次: {round_num} | AI数量: {1 if self.status.single_or_dual == 1 else 2}")

    def update_executor_output(self, output):
        """更新执行者输出"""
        self.addMessage("执行者", output, "executor")

    def update_supervisor_output(self, output):
        """更新监察者输出"""
        self.addMessage("监察者", output, "supervisor")

    def update_system_stdout(self, output):
        """更新系统标准输出"""
        self.addMessage("系统输出", output, "output")

    def update_system_stderr(self, output):
        """更新系统错误输出"""
        self.addMessage("系统错误", output, "error")

    def thread_exited(self, exit_code):
        self.status.exit = exit_code

        if exit_code == 1:
            print("to 1")
            self.chat_thread.send_status(self.setting, self.status)
            self.chat_thread.start()

            self.start_work_button.setEnabled(True)
            self.send_button.setEnabled(True)
            self.stop_work_button.setEnabled(False)
            self.addMessage("系统", "工作已停止，进入聊天状态", "system")
            self.status_label.setText(f"状态: 聊天中 | AI数量: {1 if self.status.single_or_dual == 1 else 2}")

        if exit_code == 0:
            print("to 0")
            self.work_thread.send_status(self.setting, self.status)
            self.work_thread.start()

            self.send_button.setEnabled(False)
            self.start_work_button.setEnabled(False)
            self.stop_work_button.setEnabled(True)
            self.addMessage("系统", "聊天已中断，进入工作状态", "system")
            self.status_label.setText(f"状态: 工作中 | AI数量: {1 if self.status.single_or_dual == 1 else 2}")

    def update_settings(self, settings):
        """更新设置"""
        self.setting = settings

# ----------------------------------------------------------------------------------------------------------------------
    # 其他功能
    # 深色模式
    def toggleDarkMode(self, checked):
        if checked:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            QApplication.setPalette(palette)
        else:
            # 浅色模式
            QApplication.setPalette(QApplication.style().standardPalette())

    def showAbout(self):
        self.addMessage("系统", "AI桌面助手 v1.0\n基于Python和PyQt5开发\n提供AI辅助工作和聊天功能,聊天状态下可与发送信息与AI交流，在聊天或工作中可以增加工作留言，在工作状态下AI可以读取该留言", "system")

if __name__ == '__main__':
    # 示例设置和状态
    app_setting = setting()
    app_status = status()

    app = QApplication(sys.argv)
    ex = AIDesktopAssistant1(app_setting, app_status)
    ex.show()
    sys.exit(app.exec_())