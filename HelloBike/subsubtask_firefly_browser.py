import time

from utils import (connect_device, back_to_app, click_and_wait, scroll_by_ratio,
                   APP_PACKAGES)

pkg = APP_PACKAGES["hellobike"]


def beetle_news(d):
    status_1 = d(textMatches=".*点击1次广告，继续倒计时.*")
    status_2 = d(textMatches=".*滑动1次页面.*")
    status_3 = d(textMatches=".*确认领取.*")
    status_4 = d(textMatches=".*继续领取.*")

    btn_confirm = d(resourceId="com.beetle.app:id/btn_confirm")
    btn_continue = d(text="继续领奖")
    btn_end = d(text="开心收下")
    btn_continue_2 = d(text="继续领取")

    while True:
        try:
            if status_1.exists:
                print("💡 状态1：点击屏幕...")
                click_and_wait(d, pos=(0.5, 0.106))

            elif status_2.exists:
                print("💡 状态2：滑动页面...")
                scroll_by_ratio(d)

            elif status_3.exists:
                print("💡 状态3：确认领取...")
                click_and_wait(d, ui_obj=btn_confirm)
                back_to_app(d, pkg)
                if btn_continue.wait(timeout=5.0):
                    click_and_wait(d, ui_obj=btn_continue)
                else:
                    click_and_wait(d, ui_obj=btn_end)
                    break
            elif status_4.exists:
                print("💡 状态4：重启任务...")
                click_and_wait(d, ui_obj=btn_continue_2)
                click_and_wait(d, pos=(0.5, 0.4))
            time.sleep(1.5)

        except Exception as e:
            # 捕获异常，防止脚本因为某个意外崩溃而停止挂机
            print(f"⚠️ 运行中出现异常: {e}")
            time.sleep(2.0)

if __name__ == "__main__":
    dev = connect_device()
    beetle_news(dev)