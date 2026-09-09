from utils import (connect_device, back_to_app, click_and_wait,
                   APP_PACKAGES, HELLOBIKE_CLOSE_BTN)

pkg = APP_PACKAGES["hellobike"]


def sign_in(d):
    """
    完成哈啰APP中的日常签到
    :param d: ui2设备对象
    """
    sign_in_btn = d(textMatches="点击广告再领.*奖励金")

    if not sign_in_btn.exists():
        click_and_wait(d, ui_obj=d(text="今日签到"))
    click_and_wait(d, ui_obj=sign_in_btn, post_delay=3.0)
    back_to_app(d, pkg)
    if sign_in_btn.exists():
        click_and_wait(d, ui_obj=sign_in_btn, post_delay=3.0)
        back_to_app(d, pkg)
    click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))


if __name__ == "__main__":
    dev = connect_device()
    sign_in(dev)