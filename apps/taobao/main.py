import sys
from pathlib import Path

# 确保脚本无论在 IDE 中还是在命令行子目录独立运行，都能正确检索到项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core import *
from apps.taobao.config import PACKAGE_NAME, VIP_NAME


def get_taobao_gold_coins(d):
    click_and_wait(d, d(description="领淘金币"))
    click_and_wait(d, d(text="签到领金币"))
    click_and_wait(d, key_name="back")
    click_and_wait(d, d(description="首页"))


def switch_taobao_account(d):
    click_and_wait(d, d(description="我的淘宝"))
    click_and_wait(d, d(description="设置"))
    click_and_wait(d, d(description="切换账号"))
    click_and_wait(d, d(text="切换"))


def buy_88vip_daily_item(d):
    click_and_wait(d, d(description="收藏"))
    click_and_wait(d, pos=(0.208, 0.280))  # 收藏商品
    click_and_wait(d, d(textMatches=r".*购买.*"))
    click_and_wait(d, pos=(0.635, 0.339))  # 88VIP2元红包
    click_and_wait(d, pos=(0.861, 0.318))  # 立即使用
    click_and_wait(d, pos=(0.521, 0.933))  # 先用后付
    click_and_wait(d, pos=(0.822, 0.374))  # 领淘金币
    click_and_wait(d, d(text="签到领金币"))
    click_and_wait(d, key_name="back", repeat_times=4)


def buy_savings_card_daily_item(d, target_count=5, max_scrolls=6):
    """
    淘宝省钱卡：自动寻找并集齐指定数量的商品流红包
    """
    click_and_wait(d, d(description="省钱卡"), post_delay=5.0)
    click_and_wait(d, d(description="立即领取"))
    click_and_wait(d, d(text="点击红包解锁"))
    print(f"🚀 开始执行【寻找 {target_count} 个省钱卡红包】任务...")
    scroll_count = 0
    while scroll_count < max_scrolls:
        # 动态检测当前进度
        progress_node = d(textMatches=r"\d+/\d+")
        if progress_node.exists():
            curr_progress = progress_node.get_text()
            print(f"📊 当前红包收集进度: [{curr_progress}]")

            if "/" in curr_progress:
                current_num, total_num = curr_progress.split("/")
                # 如果集齐 8 个最终是1元红包，跳过
                if total_num != str(target_count):
                    click_and_wait(d, key_name="back", repeat_times=2)
                    return
                # 如果集齐 5/5
                if current_num == total_num:
                    print(f"🎉 太棒了！已成功集齐 {target_count} 个红包！")
                    break
        # 检测当前屏幕是否有未点击的红包
        red_packet = d(resourceIdMatches=".*feeds-red-packet-task.*")
        if red_packet.exists(timeout=1.5):
            # 底部字条会遮挡点击，需要屏蔽
            _, center_y = red_packet.center()
            y_ratio = center_y / d.info['displayHeight']
            if y_ratio > 0.84:
                scroll_by_ratio(d)
                continue
            click_and_wait(d, red_packet)
            click_and_wait(d, key_name="back")
            # 点完退出来后，向下滑动翻过该商品，寻找下一个
            scroll_by_ratio(d, dy_ratio=-0.66)
            continue
        # 当前屏幕无红包，向下翻页巡航
        print(f"⏬ 当前屏无红包，向下滑动巡航 (第 {scroll_count + 1}/{max_scrolls} 次)...")
        scroll_by_ratio(d, dy_ratio=-0.66, post_delay=1.5)
        scroll_count += 1
        # 如果没找到重进一下
        if scroll_count >= max_scrolls:
            click_and_wait(d, key_name="back")
            click_and_wait(d, d(text="点击红包解锁"))
            scroll_count=0
    # 任务完成后的领取
    click_and_wait(d, d(text="领红包"))
    click_and_wait(d, d(text="限时领"))
    click_and_wait(d, d(text="确认领取"))
    click_and_wait(d, key_name="back",repeat_times=2)

    # 购买商品
    click_and_wait(d, d(description="我的淘宝"))
    click_and_wait(d, d(description="收藏"))
    click_and_wait(d, pos=(0.208, 0.280))  # 收藏商品
    click_and_wait(d, d(textMatches=r".*购买.*"))
    click_and_wait(d, pos=(0.521, 0.933))  # 先用后付
    click_and_wait(d, key_name="back", repeat_times=3)


def run_daily(d):
    """
    淘宝日常任务全流程
    """
    restart_app(d, PACKAGE_NAME)
    click_and_wait(d, d(description="关闭按钮"))

    for _ in range(2):
        click_and_wait(d, d(description="我的淘宝"))
        if not d(description=VIP_NAME).wait(timeout=3.0):
            get_taobao_gold_coins(d)
            buy_savings_card_daily_item(d)
        else:
            buy_88vip_daily_item(d)
        switch_taobao_account(d)


if __name__ == "__main__":
    device = connect_device()
    run_daily(device)