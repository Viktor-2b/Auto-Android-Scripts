from utils import (connect_device, restart_app, back_to_app, click_and_wait, scroll_by_ratio,
                   APP_PACKAGES, HELLOBIKE_CLOSE_BTN)
from subtask_sign_in import sign_in
from subtask_browse_weibo import browse_weibo
from HelloBike.subtask_watch_ads import watch_ads
from subtask_click import click

pkg = APP_PACKAGES["hellobike"]


def handle_hello_popups(d):
    """
    处理哈啰单车首页的各类拦截弹窗
    :param d: ui2设备对象
    """
    click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))
    click_and_wait(d, ui_obj=d(resourceId=pkg + ":id/actionDialogClose"))

def entry_from_app(d):
    restart_app(d, pkg)

    my_tab = d(text="我的")
    if not my_tab.exists():
        handle_hello_popups(d)

    click_and_wait(d, ui_obj=my_tab)
    click_and_wait(d, ui_obj=dev(text="奖励金"), post_delay=3.0)


if __name__ == "__main__":
    dev = connect_device()

    entry_from_app(dev)

    sign_in(dev)

    scroll_by_ratio(dev, dy_ratio=-0.466)
    click_and_wait(dev, ui_obj=dev(textMatches="还有.*个任务"))
    scroll_by_ratio(dev, dy_ratio=-0.656)

    browse_weibo(dev)

    watch_ads(dev)

    click(dev)

