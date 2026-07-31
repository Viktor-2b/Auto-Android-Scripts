from utils import connect_device

print("🔄 正在尝试连接手机读取屏幕分辨率...")
d = connect_device()

screen_w = d.info['displayWidth']
screen_h = d.info['displayHeight']
print(f"✅ 读取成功！当前设备分辨率: {screen_w} x {screen_h}")
print("=" * 45)

while True:
    try:
        user_input = input("\n👉 请输入坐标 (格式: x,y)，输入 q 退出: ")

        if user_input.lower().strip() == 'q':
            print("👋 退出换算工具。")
            break

        # 解析输入的坐标
        x_str, y_str = user_input.split(',')
        x = float(x_str.strip())
        y = float(y_str.strip())

        # 计算比例并保留三位小数
        ratio_x = x / screen_w
        ratio_y = y / screen_h

        print("-" * 45)
        print(f"📍 输入物理坐标 : X={int(x)}, Y={int(y)}")
        print(f"✨ 请直接复制以下代码 :")
        print(f"pos=({ratio_x:.3f}, {ratio_y:.3f})")
        print("-" * 45)

    except ValueError:
        print("⚠️ 输入格式错误！请确保使用英文逗号分隔，例如: 1240,1024")
    except Exception as e:
        print(f"⚠️ 发生未知错误: {e}")
