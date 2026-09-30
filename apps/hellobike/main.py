import sys
from pathlib import Path


# 确保脚本无论在 IDE 中还是在命令行子目录独立运行，都能正确检索到项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core import connect_device, restart_app, click_and_wait, scroll_by_ratio
from apps.hellobike.config import PACKAGE_NAME, HELLOBIKE_CLOSE_BTN, ACTION_DIALOG_CLOSE_BTN
from apps.hellobike.tasks.subtask_sign_in import sign_in
from apps.hellobike.tasks.subtask_flashback import flashback
from apps.hellobike.tasks.subtask_limited_ad import limited_ad
from apps.hellobike.tasks.subtask_browse_weibo import browse_weibo


def handle_hello_popups(d):
    """
    处理哈啰单车首页的各类拦截弹窗
    :param d: ui2设备对象
    """
    click_and_wait(d, ui_obj=d(resourceId=HELLOBIKE_CLOSE_BTN))
    click_and_wait(d, ui_obj=d(resourceId=ACTION_DIALOG_CLOSE_BTN))


def entry_from_app(d):
    restart_app(d, PACKAGE_NAME)
    handle_hello_popups(d)
    click_and_wait(d, ui_obj=d(text="我的"))
    click_and_wait(d, ui_obj=d(text="奖励金"), post_delay=3.0)


def run_daily(d):
    """
    哈啰日常任务全流程
    """
    entry_from_app(d)

    sign_in(d)
    flashback(d, ".*百度地图.*")
    limited_ad(d)
    # TODO 看视频
    scroll_by_ratio(d, dy_ratio=-0.5)
    click_and_wait(d, ui_obj=d(textMatches="还有.*个任务"))

    browse_weibo(d)
    flashback(d, ".*同程.*")
    flashback(d, ".*飞猪.*")
    # TODO 所有任务



if __name__ == "__main__":
    dev = connect_device()
    run_daily(dev)