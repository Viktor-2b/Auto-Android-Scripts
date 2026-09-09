from utils import (connect_device, back_to_app, click_and_wait, scroll_by_ratio,
                   APP_PACKAGES, HELLOBIKE_CLOSE_BTN)

pkg = APP_PACKAGES["hellobike"]

def browse_weibo(d):
    """
    完成哈啰APP中的微博浏览
    :param d: ui2设备对象
    """
    click_and_wait(d,ui_obj=d(text="浏览微博3篇博文任务").right(textMatches="领任务|去微博"),post_delay=5.0)
    for i in range(5):
        scroll_by_ratio(d)
    back_to_app(d, pkg)
    click_and_wait(d,key_name="back")
    click_and_wait(d, ui_obj=d(text="浏览微博3篇博文任务").right(text="领奖励"))
    click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))

if __name__ == "__main__":
    dev = connect_device()
    browse_weibo(dev)