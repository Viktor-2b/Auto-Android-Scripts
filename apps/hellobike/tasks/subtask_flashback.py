from core import connect_device, back_to_app, click_and_wait
from apps.hellobike.config import PACKAGE_NAME, HELLOBIKE_CLOSE_BTN

def flashback(d, text):
    """
    完成哈啰APP中的跳转后返回
    :param d: ui2设备对象
    :param text: 任务名称
    """
    click_and_wait(d, ui_obj=d(text=text).right(textMatches="领任务|去完成"), post_delay=5.0)
    back_to_app(d, PACKAGE_NAME)
    click_and_wait(d, ui_obj=d(text=text).right(text="领奖励"))
    double_btn = d(textMatches=".*(翻倍|再领.*奖励金|开心收下|去领取).*")
    if double_btn.exists(timeout=3.0):
        print(f"🎉 发现奖励按钮 [{double_btn.get_text()}]，正在点击...")
        click_and_wait(d, double_btn, post_delay=3.0)
    else:
        print("ℹ️ 未检测到翻倍按钮，尝试按一次关闭...")
        click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))

if __name__ == "__main__":
    dev = connect_device()
    flashback(dev, text="去百度地图APP体验新导航")