"""
程序名: 中国国旗的绘制
描述: 中国国旗的绘制
作者: fsloper
版本: 0.2.beta
日期: 2024年12月11日
注意:虽然我仔细阅读了国旗构成,但不保证百分百精确,还以官网图示为准,"https://www.gov.cn/guoqing/guoqi/index.htm"
"""
import turtle
import math


# 根据外接圆半径计算五角星边长的函数
def calculate_star_side_length(radius):
    """
    根据给定的外接圆半径计算五角星的边长，使用数学公式a = ((math.sqrt(5) - 1) / 4) * R
    :param radius: 外接圆半径
    :return: 五角星边长
    """
    return radius * ((math.sqrt(5) - 1) / 4)


# 绘制国旗旗面（红色矩形）
def draw_surface(scale_factor):
    """
    绘制国旗的红色矩形旗面部分
    :param scale_factor: 用于控制旗面大小的缩放因子
    """
    turtle.penup()
    turtle.goto(-3 * scale_factor / 2, 2 * scale_factor / 2)
    turtle.pendown()

    # 设置填充颜色为红色
    turtle.fillcolor('red')
    # 开始填充红色矩形
    turtle.begin_fill()

    # 绘制矩形
    for _ in range(2):
        turtle.forward(3 * scale_factor)
        turtle.right(90)
        turtle.forward(2 * scale_factor)
        turtle.right(90)

    turtle.penup()
    # 结束填充红色矩形
    turtle.end_fill()


# 绘制大五角星
def draw_big_star(scale_factor):
    """
    绘制国旗左上角的大五角星
    :param scale_factor: 用于控制五角星大小及位置的缩放因子
    """
    turtle.setheading(0)
    # 大五角星外接圆直径为旗高三分之一
    big_star_radius = 2 * scale_factor / 3
    # 计算大五角星边长
    big_star_side_length = calculate_star_side_length(big_star_radius)
    # 抬起画笔，移动到大五角星尖尖位置（通过三角函数计算坐标）
    x = -(3 * scale_factor / 2 / 3 * 2 + (2 * scale_factor / 10 * 3 / 2 * math.cos(math.radians(18))))
    y = 2 * scale_factor / 2 / 10 * 5 + (2 * scale_factor / 10 * 3 / 2 * math.sin(math.radians(18)))
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    # 设置填充颜色为黄色
    turtle.fillcolor('yellow')
    # 开始填充黄色五角星
    turtle.begin_fill()
    # 绘制五角星的循环
    for _ in range(5):
        turtle.forward(big_star_side_length)
        turtle.left(72)
        turtle.forward(big_star_side_length)
        turtle.right(144)
    turtle.penup()
    turtle.end_fill()


# 绘制小五角星
def draw_small_star(scale_factor, x_center, y_center, angle_to_target):
    """
    绘制围绕大五角星的小五角星
    :param scale_factor: 用于控制小五角星大小及位置的缩放因子
    :param x_center: 小五角星中心点的x坐标（相对坐标）
    :param y_center: 小五角星中心点的y坐标（相对坐标）
    :param angle_to_target: 小五角星指向大五角星中心的角度
    """
    turtle.fillcolor('yellow')

    # 计算小五角星外接圆半径（其外接圆直径为旗高十分之一）
    small_star_radius = 2 * scale_factor / 10
    # 计算小五角星边长
    small_star_side_length = calculate_star_side_length(small_star_radius)

    # 移动到五角星中心点位置
    turtle.penup()
    turtle.goto(-x_center, y_center)
    if angle_to_target < 45:
        turtle.setheading(angle_to_target + 180)
    else:
        turtle.setheading(angle_to_target + 90)
    turtle.forward(3 * scale_factor / 2 / 15)
    turtle.right(180 - 18)
    turtle.begin_fill()
    turtle.pendown()
    for _ in range(5):
        turtle.forward(small_star_side_length)
        turtle.left(72)
        turtle.forward(small_star_side_length)
        turtle.right(144)

    # 调整五角星角度，使其尖尖指向目标点
    turtle.right(angle_to_target)
    turtle.end_fill()


# 获取turtle的屏幕对象
screen = turtle.Screen()
# 缩放因子，用于控制国旗绘制的整体大小，可根据实际情况调整，只要屏幕放得下
scale_factor = 300

# 设置屏幕的背景颜色
screen.bgcolor("blue")

screen.setup(width=4 * scale_factor, height=3 * scale_factor)

draw_surface(scale_factor)
draw_big_star(scale_factor)
# 计算从中心点指向目标点的角度，将角度转换为度（turtle库中角度默认是度）
star_1_angle = math.degrees(math.atan(3 / 5))
star_2_angle = math.degrees(math.atan(1 / 7))
star_3_angle = math.degrees(math.atan(7 / 2))
star_4_angle = math.degrees(math.atan(5 / 4))

draw_small_star(scale_factor, 3 * scale_factor / 2 / 15 * 5, 2 * scale_factor / 2 / 10 * 8, star_1_angle)
draw_small_star(scale_factor, 3 * scale_factor / 2 / 15 * 3, 2 * scale_factor / 2 / 10 * 6, star_2_angle)
draw_small_star(scale_factor, 3 * scale_factor / 2 / 15 * 3, 2 * scale_factor / 2 / 10 * 3, star_3_angle)
draw_small_star(scale_factor, 3 * scale_factor / 2 / 15 * 5, 2 * scale_factor / 2 / 10 * 1, star_4_angle)

turtle.penup()
turtle.goto(3.1 * scale_factor, -2.1 * scale_factor)
# 保持图形窗口显示，避免绘制完成后立即关闭
turtle.done()
