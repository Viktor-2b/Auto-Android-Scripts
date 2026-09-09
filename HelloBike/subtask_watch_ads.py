from utils import (connect_device, back_to_app, click_and_wait,
                   APP_PACKAGES, HELLOBIKE_CLOSE_BTN)


pkg = APP_PACKAGES["hellobike"]

def watch_ads(d):
    """
    完成哈啰APP中的观看广告
    :param d: ui2设备对象
    """
    click_and_wait(d,ui_obj=d(textMatches="观看.*秒广告领奖励金").right(textMatches="领任务|去浏览"),post_delay=5.0)
    click_and_wait(d,ui_obj=d(text="去浏览"),post_delay=10.0)
    back_to_app(d,pkg)
    click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))

if __name__ == "__main__":
    dev = connect_device()
    watch_ads(dev)