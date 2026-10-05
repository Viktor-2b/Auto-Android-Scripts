from utils import (connect_device, restart_app, click_and_wait,
                   APP_PACKAGES, VIP_NAME)

pkg = APP_PACKAGES["taobao"]


def get_taobao_gold_coins(d):
    click_and_wait(d, d(description="领淘金币"))
    click_and_wait(d, d(text="签到领金币"))
    click_and_wait(d, key_name="back")


def switch_taobao_account(d):
    click_and_wait(d, d(description="我的淘宝"))
    click_and_wait(d, d(description="设置"))
    click_and_wait(d, d(description="切换账号"))
    click_and_wait(d, d(text="切换"))


def buy_88vip_daily_item(d):
    click_and_wait(d, d(description="我的淘宝"))
    if not d(description=VIP_NAME).wait(timeout=3.0):
        print(f"👀 当前账号不是 [{VIP_NAME}]，跳过下单流程。")
        return
    click_and_wait(d, d(description="收藏"))
    click_and_wait(d, pos=(0.208, 0.280))  # 收藏商品
    click_and_wait(d, d(text="立即购买"))
    click_and_wait(d, pos=(0.635, 0.359))  # 88VIP2元红包
    click_and_wait(d, pos=(0.861, 0.318))  # 立即使用
    click_and_wait(d, pos=(0.521, 0.933))  # 先用后付
    click_and_wait(d, pos=(0.822, 0.374))  # 领淘金币
    for _ in range(5):
        click_and_wait(d,key_name="back")


if __name__ == "__main__":
    device = connect_device()
    restart_app(device, pkg)
    click_and_wait(device, device(description="关闭按钮"))

    for _ in range(2):
        get_taobao_gold_coins(device)
        buy_88vip_daily_item(device)
        switch_taobao_account(device)

