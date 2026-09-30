from core import connect_device, back_to_app, click_and_wait, scroll_by_ratio
from apps.hellobike.config import PACKAGE_NAME, HELLOBIKE_CLOSE_BTN

def browse_weibo(d):
    """
    完成哈啰APP中的微博浏览
    :param d: ui2设备对象
    """
    click_and_wait(d,ui_obj=d(textMatches="浏览微博3篇博文任务|去浏览微博3篇博文").right(textMatches="领任务|去微博"),post_delay=8.0)
    scroll_by_ratio(d, dy_ratio=-0.5,repeat_times=5)
    back_to_app(d, PACKAGE_NAME)
    click_and_wait(d,key_name="back")
    click_and_wait(d, ui_obj=d(text="已浏览微博, 成功获得88奖励金").right(text="领奖励"))
    click_and_wait(d, d(text="点击广告 再得"), post_delay=3.0)
    back_to_app(d, PACKAGE_NAME)
    click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))

if __name__ == "__main__":
    dev = connect_device()
    browse_weibo(dev)