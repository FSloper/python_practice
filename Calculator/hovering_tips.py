"""
这个模块用于为计算器应用程序中的按钮添加悬浮提示（tooltip）功能。
通过创建ToolTip类来实现鼠标悬停在按钮上时显示相应的提示信息。
"""

import tkinter as tk


class ToolTip:
    """
    创建用于显示悬浮提示（tooltip）的类。
    当鼠标悬停在绑定的控件上时，会显示指定的提示文本，鼠标移开则隐藏提示。
    """

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        """
        当鼠标进入绑定的控件时触发的方法，用于安排显示提示窗口。
        """
        self.schedule()

    def leave(self, event=None):
        """
        当鼠标离开绑定的控件或者按下鼠标按钮时触发的方法，用于取消提示窗口的显示。
        """
        self.unschedule()
        self.hidetip()

    def schedule(self):
        """
        安排显示提示窗口，如果当前没有正在等待显示的提示窗口，则设置一个延迟任务来显示它。
        """
        self.unschedule()
        self.id = self.widget.after(200, self.showtip)

    def unschedule(self):
        """
        取消之前安排的显示提示窗口的延迟任务（如果存在的话）。
        """
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self):
        """
        实际显示提示窗口的方法，创建一个顶层窗口并在其中显示提示文本。
        """
        if self.tip_window:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tip_window, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1)
        label.pack(ipadx=1)

    def hidetip(self):
        """
        隐藏提示窗口（如果存在的话），并销毁对应的顶层窗口对象。
        """
        tip_window = self.tip_window
        self.tip_window = None
        if tip_window:
            tip_window.destroy()
