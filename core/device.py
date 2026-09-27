import time
import uiautomator2 as u2


def connect_device():
    """
    基础环境初始化与设备连接
    :return: uiautomator2 设备对象
    """
    print("🔄 正在尝试连接手机...")
    try:
        d = u2.connect()
        brand = d.device_info.get("brand", "")
        model = d.device_info.get("model", "")
        print(f"✅ 手机连接成功！设备型号: {brand} {model}")

        # 保持屏幕常亮并解锁
        d.screen_on()
        return d
    except Exception as e:
        print(f"❌ 手机连接失败: {e}")
        exit(1)


def restart_app(d, package_name: str, wait_time: float = 5.0):
    """
    强制杀后台并重新拉起指定 APP，确保纯净初始环境
    :param d: uiautomator2 设备对象
    :param package_name: 应用包名
    :param wait_time: 启动后预留的加载缓冲时间
    """
    print(f"🧹 正在清理后台进程: {package_name}...")
    d.app_stop(package_name)
    time.sleep(1.0)

    print(f"🚀 正在启动 APP: {package_name}...")
    d.app_start(package_name)

    print(f"⏳ 等待 APP 加载，预留 {wait_time} 秒...")
    time.sleep(wait_time)


def back_to_app(d, package_name: str):
    """
    检查当前前台 APP 是否偏离，若偏离则强制拉回
    :param d: uiautomator2 设备对象
    :param package_name: 期望保持前台的应用包名
    """
    current_pkg = d.app_current().get("package")
    if current_pkg != package_name:
        print(f"⚠️ 发现当前偏离到其它APP ({current_pkg})，正在强制拉回({package_name})...")
        d.app_start(package_name)
        time.sleep(2.5)
