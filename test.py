from core import *
from apps.hellobike.config import *

pkg = PACKAGE_NAME
d = connect_device()

click_and_wait(d, ui_obj=d(text="已浏览微博, 成功获得88奖励金").right(text="领奖励"))
click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))

