
import win32com.client

def is_font_installed():
    try:
        font_name = 'MiSans Normal'
        g = win32com.client.Dispatch('Word.Application')
        font_collection = g.FontNames
        for font in font_collection:
            if font == font_name:
                g.Quit()
                print("字体已安装")
        g.Quit()
        print("字体未安装")

    except:
        print("无法检查字体是否安装")

# 示例用法
is_font_installed()
