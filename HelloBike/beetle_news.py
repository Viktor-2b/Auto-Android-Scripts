# -*- encoding=utf8 -*-
import uiautomator2 as u2
import time

# ==========================================
# 1. 基础环境初始化
# ==========================================
print("正在尝试连接手机...")
d = u2.connect()
print(f"手机连接成功！设备型号: {d.info.get('model')}")

# ==========================================
# 2. 预先定义 UI 元素
# ==========================================
# textMatches 依然支持正则表达式
status_0 = d(textMatches=".*点击广告后开始计时.*")
status_1 = d(textMatches=".*点击1次广告，继续倒计时.*")
status_2 = d(textMatches=".*滑动1次页面.*")
status_3 = d(textMatches=".*确认领取.*")
status_4 = d(textMatches=".*继续完成.*")

news_container = d(resourceIdMatches=".*newsContainer.*")
btn_confirm = d(resourceId="com.beetle.app:id/btn_confirm")
btn_continue = d(text="继续领奖")
btn_end = d(text="开心收下")
btn_continue_2 = d(text="继续完成")

package_name = "com.jingyao.easybike"

# ==========================================
# 3. 点击甲壳虫资讯广告触发计时
# ==========================================


def ad_container_click():
    if news_container.exists:
        news_container.click()
    else:
        d.press("back")

print("\n--- 触发资讯广告点击 ---")

while True:
    try:
        if status_0.exists:
            print("💡 状态0：启动任务...")
            ad_container_click()

        elif status_1.exists:
            print("💡 状态1：退出后重进广告...")
            d.press("back")
            time.sleep(2.0)
            ad_container_click()

        elif status_2.exists:
            print("💡 状态2：滑动页面...")
            # u2 的 swipe 直接支持比例坐标 (startX, startY, endX, endY)
            d.swipe(0.5, 0.8, 0.5, 0.3)

        elif status_3.exists:
            print("💡 状态3：确认领取...")
            btn_confirm.click()
            d.app_start(package_name)
            time.sleep(1.5)
            if btn_continue.wait(timeout=5.0):
                btn_continue.click()
            else:
                btn_end.click()
                break
        elif status_4.exists:
            print("💡 状态4：重启任务...")
            btn_continue_2.click()
            d.click(0.5,0.4)
        time.sleep(3.0)

    except Exception as e:
        # 捕获异常，防止脚本因为某个意外崩溃而停止挂机
        print(f"⚠️ 运行中出现异常: {e}")
        time.sleep(2.0)