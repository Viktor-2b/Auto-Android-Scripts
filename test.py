from utils import (connect_device, restart_app, back_to_app, click_and_wait, scroll_by_ratio,
                   APP_PACKAGES, HELLOBIKE_CLOSE_BTN)
import time

pkg = APP_PACKAGES["hellobike"]
d = connect_device()
click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))