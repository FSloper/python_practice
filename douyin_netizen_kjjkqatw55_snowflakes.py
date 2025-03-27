"""
程序名: 雪花
作者: fsloper
版本: 0.1.beta
日期: 2024年12月11日
注意:科赫曲线是一种像雪花的几何曲线，所以又称为雪花曲线，它是de Rham曲线的特例。科赫曲线是出现在海里格·冯·科赫的论文中，是分形曲线中的一种。
"""

import turtle


def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order - 1, size / 3)
            t.left(angle)


# 绘制不同阶数的科赫曲线
def draw_koch_curves(order):
    screen = turtle.Screen()
    # 根据屏幕大小调节,也可以固定大小
    screen.setup(320 * multiple, 200 * multiple)
    t = turtle.Turtle()
    # 不知道速度能不能再快了,使用多线程同时画也许可以
    t.speed(0)
    t.pencolor("blue")
    t.penup()
    t.goto(-100 * multiple, 40 * order)
    t.pendown()
    # 正常一次只画三分之一
    for _ in range(3):
        # 防止太小看不清 100 * order
        koch_curve(t, order, 170 * order)
        t.right(120)

    turtle.done()


if __name__ == "__main__":
    # 绘制不同阶数的科赫曲线,一般情况5以后就看不起了
    multiple = 5
    draw_koch_curves(multiple)
