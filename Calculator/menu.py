import tkinter as tk
from tkinter import messagebox


class CalculatorMenu:
    def __init__(self, root, calculator_app):
        """
        初始化菜单栏类，创建并添加各种菜单及菜单项到主窗口的菜单栏上。

        :param root: 主窗口对象（tkinter的Tk实例）
        :param calculator_app: CalculatorApp类的实例，用于关联菜单操作与计算器的功能
        """
        self.root = root
        self.calculator_app = calculator_app
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 创建"文件"菜单及相关菜单项
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)
        self.file_menu.add_command(label="保存历史记录", command=self.save_history)
        self.file_menu.add_command(label="打开历史记录", command=self.open_history)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=self.root.quit)

        # 创建"查看"菜单及相关菜单项（添加自动计算复选框菜单项）
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="查看", menu=self.view_menu)
        self.auto_calculate_var = tk.IntVar()  # 创建用于存储自动计算复选框状态的变量
        self.auto_calculate_var.set(1)  # 设置变量的值为1，这样复选框就会默认打勾
        self.view_menu.add_checkbutton(label="自动计算结果", variable=self.auto_calculate_var,
                                       command=self.toggle_auto_calculate)
        self.dark_mode_var = tk.IntVar()  # 创建用于存储暗色模式复选框状态的变量
        self.view_menu.add_checkbutton(label="暗色模式", variable=self.dark_mode_var,
                                       command=self.toggle_dark_mode)
        self.view_menu.add_command(label="显示历史记录面板", command=self.show_history_panel)

        # 创建"帮助"菜单及相关菜单项
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="帮助", menu=self.help_menu)
        self.help_menu.add_command(label="关于", command=self.show_about_info)
        # 创建"重启软件"菜单项，添加到"帮助"菜单下（你也可根据需求调整放置的菜单位置）
        self.help_menu.add_command(label="重启软件", command=self.calculator_app.restart_application)

    def save_history(self):
        """
        保存计算历史记录的方法，这里只是占位，实际需要实现具体的保存逻辑，比如将历史记录写入文件等。
        """
        print("待实现：保存计算历史记录功能")

    def open_history(self):
        """
        打开历史记录的方法，这里只是占位，实际可从文件等读取历史记录并展示在相应界面上。
        """
        print("待实现：打开历史记录功能")

    def show_history_panel(self):
        """
        显示历史记录面板的方法，同样是占位，后续要实现显示对应界面的功能。
        """
        print("待实现：显示历史记录面板功能")

    def show_about_info(self):
        """
        显示关于计算器的信息，例如版本号、作者等基本情况，可弹出一个消息框展示这些内容。
        """
        about_text = "计算器版本：0.1.beta\n作者：fsloper\n这是一个多功能计算器程序"
        messagebox.showinfo("关于", about_text)

    def toggle_auto_calculate(self):
        """
        切换自动计算功能的方法，根据复选框的选中状态来设置计算器是否自动计算。
        """
        self.calculator_app.set_auto_calculate(self.auto_calculate_var.get())

    def toggle_dark_mode(self):
        """
        切换暗色模式的方法，根据复选框的选中状态调用计算器应用程序中的方法来切换界面颜色主题。
        """
        self.calculator_app.toggle_dark_mode(self.dark_mode_var.get())