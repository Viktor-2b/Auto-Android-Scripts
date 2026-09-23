import time

from utils import (connect_device, back_to_app, click_and_wait, scroll_by_ratio,
                   APP_PACKAGES)

pkg = APP_PACKAGES["hellobike"]


def alipay(d):
    click_and_wait(d, pos=(0.764, 0.942))

if __name__ == "__main__":
    dev = connect_device()
    alipay(dev)