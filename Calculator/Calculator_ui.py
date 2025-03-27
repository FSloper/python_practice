"""
程序名: 计算器
描述: 多功能计算器
作者: fsloper
版本: 0.1.beta
日期: 2024年12月13日
描述:目标一个万能的计算器,功能包括基础加减乘除,三角函数,指数,在考虑是否加入画图功能
"""
import os
import sys
import tkinter as tk

import sympy

from hovering_tips import ToolTip
from menu import CalculatorMenu  # 导入创建好的菜单栏类

import xml.etree.ElementTree as ET


class CalculatorApp:
    def __init__(self, root):
        """
        初始化计算器应用程序类
        :param root: 主窗口对象
        """
        # try:
        #     g = win32com.client.Dispatch('Word.Application')
        #     font_collection = g.FontNames
        #     for font in font_collection:
        #         if font == 'MiSans Normal':
        #             g.Quit()
        #             self.font_mi = 'MiSans Normal'
        #             print("字体已安装")
        #     g.Quit()
        #     print("字体未安装")
        #     self.font_mi = 'Arial'
        # except:
        #     self.font_mi = 'Arial'
        #     print("无法检查字体是否安装")

        self.font_mi = 'MiSans Normal'
        self.click_count = None
        # 添加属性用于记录自动计算功能的状态，默认为True（可根据实际需求调整初始值）
        self.auto_calculate = True
        # 添加属性用于记录暗色模式的状态，默认为False（表示亮色模式，可根据实际需求调整初始值）
        self.dark_mode = False
        self.root = root
        self.language_dict = self.load_language_file()
        self.root.title(self.language_dict.get("Calculator", "Calculator"))
        self.root.bind("<Key>", self.key_pressed)

        # 创建用于显示输入表达式的文本框
        self.input_text = tk.StringVar()
        self.input_display = tk.Entry(self.root, textvariable=self.input_text, justify='right', font=(self.font_mi, 14))
        self.input_display.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky='ew')
        # 精确位数输入框
        self.precision_entry = tk.Entry(self.root, width=5, font=(self.font_mi, 12))
        self.precision_entry.insert(0, "6")  # 默认精确位数为6
        self.precision_entry.grid(row=0, column=5, padx=10, pady=10, sticky='e')

        # TODO 增加历史记录文本框

        # 创建用于显示计算结果的文本框
        self.result_text = tk.StringVar()
        self.result_display = tk.Entry(self.root, textvariable=self.result_text, justify='right',
                                       font=(self.font_mi, 14),
                                       state='readonly')
        self.result_display.grid(row=1, column=0, columnspan=5, padx=10, pady=5, sticky='ew')
        # 复制数据到剪切板按钮
        self.copy_button = tk.Button(self.root, text=self.language_dict.get("copy", "Copy"), command=self.copy_to_clipboard,
                                     font=(self.font_mi, 12))
        self.copy_button.grid(row=1, column=5, padx=10, pady=5, sticky='w')

        # 生成按钮文本及位置信息
        button_texts_and_positions = self.generate_button_info()

        # 创建按钮并添加到界面
        self.create_buttons(button_texts_and_positions)

        # 为按钮绑定相应的事件
        self.bind_button_commands(button_texts_and_positions)

        # 为按钮添加悬浮提示
        self.add_tooltips(button_texts_and_positions)

        # 创建并添加菜单栏到主窗口
        self.menu = CalculatorMenu(self.root, self)  # 将自身实例传入，方便菜单操作调用计算器相关功能

    def load_language_file(self):
        """
        加载语言文件
        """
        tree = ET.parse("./language/zh_CN.xml")
        root = tree.getroot()
        language_dict = {}
        for phrase in root.findall("phrase"):
            lang_id = phrase.get("id")
            lang_text = phrase.text
            language_dict[lang_id] = lang_text
        return language_dict

    def restart_application(self):
        """
        重启应用程序的方法
        """
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def toggle_dark_mode(self, enabled):
        """
        切换暗色模式，根据传入的参数设置界面组件的颜色主题。

        :param enabled: 布尔值，True表示启用暗色模式，False表示禁用（恢复亮色模式）
        """
        self.dark_mode = bool(enabled)
        if self.dark_mode:
            self._set_dark_mode_colors()
        else:
            self._set_light_mode_colors()

    def _set_dark_mode_colors(self):
        """
        设置暗色模式下界面组件的颜色，包括文本框、按钮等的背景色和前景色等。
        """
        bg_color = "#222222"
        fg_color = "#ffffff"
        button_bg_color = "#333333"
        # 设置窗口背景颜色为浅蓝色（这里颜色值可以替换成你想要的任何颜色代码）
        self.root.configure(bg="black")
        # FIXME 无法修改菜单栏颜色
        self.menu.menu_bar.config(bg=bg_color, fg=fg_color)
        self.input_display.config(bg=bg_color, fg=fg_color)
        self.precision_entry.config(bg=bg_color, fg=fg_color)
        self.result_display.config(bg=bg_color, fg=fg_color, readonlybackground=bg_color)
        for button in self.root.winfo_children():
            if isinstance(button, tk.Button):
                button.config(bg=button_bg_color, fg=fg_color)

    def _set_light_mode_colors(self):
        """
        设置亮色模式下界面组件的默认颜色，恢复到初始的颜色设置。
        """
        bg_color = "white"
        fg_color = "black"
        button_bg_color = "#f0f0f0"
        self.root.configure(bg="white")
        # FIXME 无法修改菜单栏颜色
        self.menu.menu_bar.config(bg=bg_color, fg=fg_color)
        self.input_display.config(bg=bg_color, fg=fg_color)
        self.precision_entry.config(bg=bg_color, fg=fg_color)
        self.result_display.config(bg=bg_color, fg=fg_color, readonlybackground=bg_color)
        for button in self.root.winfo_children():
            if isinstance(button, tk.Button):
                button.config(bg=button_bg_color, fg=fg_color)

    def copy_to_clipboard(self):
        """
        将结果复制到剪贴板
        """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_text.get())

    def key_pressed(self, event):
        """
        处理键盘事件
        :param event: 键盘事件对象
        """
        # FIXME 键盘事件处理逻辑与键盘输入冲突
        key = event.char
        # if key.isdigit() or key in ['+', '-', '*', '/', '.', '%', '(', ')']:
        #     self.append_content(key)
        if key == '\r' or key == '=':
            self.calculate_result()
        elif key == '\x08':
            self.input_text.set(self.input_text.get()[:-1])

    def generate_button_info(self):
        """
        生成计算器界面上所有按钮的文本及位置信息
        :return: 包含按钮文本及对应行列位置的列表
        """
        button_texts = []

        # 数字按钮相关文本
        nums = ['AC', 'C', '%', '7', '8', '9', '4', '5', '6', '1', '2', '3', '0', '.', '00']
        for row in range(2, 8):
            for col in range(0, 3):
                index = (row - 2) * 3 + col
                if index < len(nums):
                    button_texts.append((nums[index], row, col))

        # 运算符按钮相关文本
        operators = ['/', '*', '-', '+', '=']
        for col in range(5):
            button_texts.append((operators[col], 2 + col, 3))

        # TODO 函数按钮相关
        functions = ['sin(', 'cos(', 'tan(', 'cot(', 'sec(', 'csc(']
        for col in range(6):
            button_texts.append((functions[col], 8, col))

        # 括号按钮相关文本
        brackets = ['(', 'ln', 'log', '√', '^']
        for col in range(5):
            button_texts.append((brackets[col], 2 + col, 4))

        # 其他按钮相关文本
        others = [')', '!', 'e', 'π', '|']
        for col in range(5):
            button_texts.append((others[col], 2 + col, 5))

        return button_texts

    def create_buttons(self, button_texts_and_positions):
        """
        根据提供的按钮文本及位置信息创建按钮并添加到界面上
        :param button_texts_and_positions: 包含按钮文本及对应行列位置的列表
        """
        for text, row, col in button_texts_and_positions:
            button = tk.Button(self.root, text=text, width=5, height=2, font=(self.font_mi, 12))
            button.grid(row=row, column=col, padx=5, pady=5)

    def bind_button_commands(self, button_texts_and_positions):
        """
        为各个按钮绑定对应的命令（事件处理函数）
        :param button_texts_and_positions: 包含按钮文本及对应行列位置的列表
        """
        for text, row, col in button_texts_and_positions:
            button = tk.Button(self.root, text=text, width=5, height=2, font=(self.font_mi, 12))
            if text != "=":
                button['command'] = lambda num=text: self.append_content(num)
            if text == "AC":
                button['command'] = lambda num=text: self.input_text.set("")
            if text == "C":
                button['command'] = lambda num=text: self.input_text.set(self.input_text.get()[:-1])
            if text == "%":
                button['command'] = lambda num=text: self.input_text.set(self.input_text.get() + "/100")
            if text == "=":
                button['command'] = self.calculate_result
            if text == "√":
                button['command'] = lambda num=text: self.input_text.set(self.input_text.get() + "sqrt(")
            if text == "π":
                button['command'] = lambda num=text: self.input_text.set(self.input_text.get() + "pi")
            if text == "|":
                button['command'] = lambda num=text: self.input_text.set(self.input_text.get() + "abs(")
            if text == "e":
                button['command'] = lambda num=text: self.input_text.set(self.input_text.get() + "E")
            button.grid(row=row, column=col, padx=5, pady=5)

    def set_auto_calculate(self, enabled):
        """
        设置自动计算功能的启用或禁用状态。

        :param enabled: 布尔值，True表示启用自动计算，False表示禁用
        """
        self.auto_calculate = bool(enabled)

    def append_content(self, content):
        """
        处理向输入表达式文本框中添加内容的操作，
        :param content: 要添加的内容（数字、运算符等）
        """
        precision = int(self.precision_entry.get()) + 2
        try:
            current_text = self.input_text.get()
            self.input_text.set(current_text + content)
            # 尝试自动计算并显示结果
            if self.auto_calculate:  # 根据自动计算功能状态判断是否进行计算
                expression = self.input_text.get()
                result = sympy.sympify(expression).evalf(precision)
                self.result_text.set(str(result))
            else:
                self.result_text.set("")
        except:
            self.result_text.set("输入有误，请重新输入auto")

    def calculate_result(self):
        """
        处理等号按钮点击后计算并显示结果的操作
        """
        precision = int(self.precision_entry.get()) + 2
        try:
            # FIXME 修复表达式中的括号问题
            expr = self.input_text.get()
            stack = []
            fixed_expr = ""
            for index in range(len(expr)):
                char = expr[index]
                if char == "(":
                    stack.append(char)
                    fixed_expr += char
                elif char == ")":
                    stack.pop()
                    fixed_expr += char
                elif char.isalpha():
                    # 如果当前字符是字母（可能是函数名等），检查前面是否是函数调用且缺少括号
                    if stack and stack[-1] == "(" and fixed_expr[-1].isdigit():
                        fixed_expr = fixed_expr[:-1] + ")(" + char
                    else:
                        fixed_expr += char
                elif char.isdigit():
                    fixed_expr += char
                else:
                    # 遇到非数字、字母、括号的其他符号
                    if stack and stack[-1] == "(" and fixed_expr[-1].isdigit():
                        fixed_expr = fixed_expr[:-1] + ")" + char
                    else:
                        fixed_expr += char
            print(fixed_expr)
            if self.click_count == 0:
                result = sympy.sympify(fixed_expr).evalf(precision)
                self.click_count += 1
            else:
                result = sympy.sympify(fixed_expr)
                self.click_count = 0  # 重置点击次数
            self.result_text.set(str(result))
        except:
            self.result_text.set("输入有误，请重新输入")

    def add_tooltips(self, button_texts_and_positions):
        """
        为按钮添加悬浮提示（tooltip），根据按钮文本设置相应的提示内容。
        :param button_texts_and_positions: 包含按钮文本及对应行列位置的列表
        """
        tooltip_texts = {
            "AC": "全部清除，清空输入框内容",
            "C": "删除最后一个输入字符",
            "%": "表示百分比，例如输入50%会转换为0.5参与运算",
            ".": "小数点，用于输入小数",
            "00": "输入两个0，常用于金额等精确到分的情况",
            "/": "除法运算符",
            "*": "乘法运算符",
            "-": "减法运算符",
            "+": "加法运算符",
            "=": "计算并显示表达式的结果,点击第二次可精确计算",
            "ln": "自然对数函数，例如ln(x)表示以e为底x的对数",
            "log": "常用对数函数，例如log(x)通常表示以10为底x的对数",
            "√": "平方根函数，例如√x表示求x的算术平方根",
            "^": "指数运算符，例如2^3表示2的3次方",
            "!": "阶乘运算符，例如5!表示5的阶乘",
            "e": "自然常数e",
            "π": "圆周率π",
            "|": "绝对值函数，例如|x|表示求x的绝对值",
            "(": "左括号，用于表达式分组",
            ")": "右括号，用于表达式分组",
            "sin(": "正弦函数，例如sin(x)表示求x的正弦值",
            "cos(": "余弦函数，例如cos(x)表示求x的余弦值",
            "tan(": "正切函数，例如tan(x)表示求x的正切值",
            "cot(": "余切函数，例如cot(x)表示求x的余切值",
            "sec(": "正割函数，例如sec(x)表示求x的正割值",
            "csc(": "余割函数，例如csc(x)表示求x的余割值"
        }
        for text, row, col in button_texts_and_positions:
            button = self.root.grid_slaves(row=row, column=col)[0]
            if text in tooltip_texts:
                ToolTip(button, tooltip_texts[text])


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
