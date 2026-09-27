from core import connect_device, click_and_wait
from apps.hellobike.config import PACKAGE_NAME as pkg


def alipay(d):
    click_and_wait(d, pos=(0.764, 0.942))

if __name__ == "__main__":
    dev = connect_device()
    alipay(dev)