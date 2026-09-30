from core import connect_device, back_to_app, click_and_wait
from apps.hellobike.config import PACKAGE_NAME, HELLOBIKE_CLOSE_BTN

def flashback(d, pattern):
    """
    完成哈啰APP中的跳转后返回
    :param d: ui2设备对象
    :param pattern: 任务名称特征
    """
    click_and_wait(d, ui_obj=d(textMatches=pattern).right(textMatches="领任务|去完成"), post_delay=5.0)
    # 首次跳转授予权限
    always_allow_cb = d(text="始终允许打开")
    if always_allow_cb.exists(timeout=1.5):
        if not always_allow_cb.info.get("checked", False):
            click_and_wait(d, always_allow_cb)
        click_and_wait(d, d(text="打开"))

    back_to_app(d, PACKAGE_NAME)
    click_and_wait(d, ui_obj=d(text="领奖励"))
    click_and_wait(d, d(text="点击广告 再得"), post_delay=3.0)
    back_to_app(d, PACKAGE_NAME)
    close_btn = d(resourceId=HELLOBIKE_CLOSE_BTN)
    if not close_btn.exists():
        click_and_wait(d, key_name="back")
    click_and_wait(d, ui_obj=close_btn)

if __name__ == "__main__":
    dev = connect_device()
    flashback(dev, pattern="去百度地图APP体验新导航")