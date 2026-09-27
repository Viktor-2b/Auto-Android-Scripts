import time
from typing import Optional, Tuple, Union


def click_and_wait(
    d,
    ui_obj=None,
    key_name: Optional[str] = None,
    pos: Optional[Union[Tuple[float, float], list]] = None,
    timeout: float = 2.0,
    post_delay: float = 1.5,
) -> bool:
    """
    等待并点击 UI 元素，或者执行物理按键，或者坐标点击
    :param d: uiautomator2 设备对象
    :param ui_obj: 预先定义好的 uiautomator2 UI对象
    :param key_name: 物理按键名称（如 "back", "home", "enter"），传入此值将忽略其他参数
    :param pos: 坐标元组 (x, y)，支持比例坐标(0~1)或绝对像素坐标。如 (0.5, 0.25)
    :param timeout: 等待元素出现的最大时长（秒）
    :param post_delay: 操作后停顿缓冲的时长（秒）
    :return: 成功执行返回 True，否则返回 False
    """
    if key_name:
        print(f"🔙 执行物理按键操作: [{key_name}]...")
        d.press(key_name)
        time.sleep(post_delay)
        return True

    if pos and isinstance(pos, (list, tuple)) and len(pos) == 2:
        print(f"📍 执行坐标点击: [X: {pos[0]}, Y: {pos[1]}]...")
        d.click(pos[0], pos[1])
        time.sleep(post_delay)
        return True

    if ui_obj is not None:
        print(f"🔍 正在等待元素: [{ui_obj.selector}]...")
        if ui_obj.wait(timeout=timeout):
            print("🎯 成功找到并点击预定义元素")
            ui_obj.click()
            time.sleep(post_delay)
            return True
        else:
            print("⚠️ 等待超时，未找到预定义元素")
            return False

    print("⚠️ 警告: 未传入任何有效操作指令(ui_obj/key_name/pos)！")
    return False


def scroll_by_ratio(
    d,
    dy_ratio: float = -0.25,
    start_x: float = 0.5,
    start_y: float = 0.75,
    post_delay: float = 0.5,
):
    """
    根据屏幕高度比例执行竖直滑动
    :param d: uiautomator2 设备对象
    :param dy_ratio: 滑动比例。负数代表手指上滑(页面内容向下拉)，正数代表手指向下滑(页面内容向上拉)
    :param start_x: 起始X轴比例，默认 0.5 (屏幕水平中央)
    :param start_y: 起始Y轴比例，默认 0.75 (屏幕偏下区域起手)
    :param post_delay: 滑动后等待页面DOM加载渲染的时间
    """
    print(f"⏬ 正在按比例 ({dy_ratio:.3f}) 滑动屏幕...")

    end_y = start_y + dy_ratio

    # 安全锁：强制限制终点 Y 坐标在 0.05 到 0.95 之间，防止触发 Android 系统顶部/底部的全面屏手势
    end_y = max(0.05, min(0.95, end_y))

    d.swipe(start_x, start_y, start_x, end_y)
    time.sleep(post_delay)
