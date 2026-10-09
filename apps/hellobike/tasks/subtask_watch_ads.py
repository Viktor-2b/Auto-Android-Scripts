from core import connect_device, back_to_app, click_and_wait
from apps.hellobike.config import PACKAGE_NAME, HELLOBIKE_CLOSE_BTN

def watch_ads(d):
    """
    完成哈啰APP中的观看广告
    :param d: ui2设备对象
    """
    watch_btn = d(text="看视频")
    while watch_btn.exists():
        click_and_wait(d, ui_obj=watch_btn, post_delay=5.0)
        speed_up_btn = d(textMatches=".*我要.*")
        if speed_up_btn.exists(timeout=2.5):
            click_and_wait(d, ui_obj=speed_up_btn, post_delay=15.0)
        back_to_app(d, PACKAGE_NAME)
        return_btn = d(textMatches=".*跳过.*")
        if return_btn.exists(timeout=1.5):
            click_and_wait(d, ui_obj=return_btn)
        click_and_wait(d, d(text="翻倍领取"), post_delay=3.0)
        back_to_app(d, PACKAGE_NAME)
        click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))

if __name__ == "__main__":
    dev = connect_device()
    watch_ads(dev)