from utils import (connect_device, click_and_wait,
                   APP_PACKAGES)
from subsubtask_beetle_news import beetle_news

pkg = APP_PACKAGES["hellobike"]

def click(d):
    """
    完成哈啰APP中的点一点 领金币任务
    :param d: ui2设备对象
    """
    click_and_wait(d,ui_obj=d(textMatches="点一点 领金币.*").right(textMatches="领任务|去完成"),post_delay=5.0)
    click_and_wait(d, ui_obj=d(text="开心收下"))
    if d(text="推荐任务").exists():
        click_and_wait(d, key_name="back")
    if d(text="+85奖励金").exists():
        beetle_news(d)


if __name__ == "__main__":
    dev = connect_device()
    click(dev)