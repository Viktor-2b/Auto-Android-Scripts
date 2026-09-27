from core import connect_device, back_to_app, click_and_wait
from apps.hellobike.config import PACKAGE_NAME, HELLOBIKE_CLOSE_BTN


def limited_ad(d):
    """
    完成哈啰APP中的显示观看广告
    :param d: ui2设备对象
    """
    click_and_wait(d, ui_obj=d(text="观看10秒广告领奖励金").right(textMatches="领任务|去浏览"))
    click_and_wait(d, ui_obj=d(text="去浏览"), post_delay=10.0)
    back_to_app(d, PACKAGE_NAME)
    click_and_wait(d, d(text="点击广告 再得"), post_delay=3.0)
    back_to_app(d, PACKAGE_NAME)
    click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))

if __name__ == "__main__":
    dev = connect_device()
    limited_ad(dev)
