# -*- encoding=utf8 -*-
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import random
# ==========================================
# 1. 基础环境初始化
# ==========================================
print("正在尝试连接手机...")
auto_setup(__file__, devices=["android:///"])
print("手机连接成功！")
print("正在初始化 poco UI 服务...")
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
print("poco 服务初始化完成！")
package_name = "com.jingyao.easybike"
# ==========================================
# 2. 点击看视频触发循环
# ==========================================
print("--- 看视频循环 ---")

watch_video_btn = poco(text="看视频")

jump_ad_chars = poco(textMatches=".*(点击打开或下载第三方应用|立即抢购|了解更多|立即领取).*")
scroll_ad_chars = poco(textMatches=".*(去抖音看).*")
browse_ad_chars = poco(textMatches=".*(反馈).*")

while True:
    watch_video_btn.click()
    sleep(5.0)

    if jump_ad_chars.wait(10).exists():
        print("💡 检测到【跳转】类广告。")
        target_btn = jump_ad_chars[-1]
        pos_y = target_btn.attr("pos")[1]
        print(f"🎯 锁定最底部的按钮 (Y坐标: {pos_y:.2f})！正在执行点击...")
        target_btn.click()
        sleep(3.0)

        print("--- 正在侦测系统级应用跳转拦截弹窗 ---")
        allow_btn = poco(text="30天内允许")
        if allow_btn.wait(10).exists():
            allow_btn.click()
            print("✅ 已授权！系统应该正在拉起第三方APP...")
        else:
            print("✅ 未检测到【30天内允许】弹窗。")
        print("--- 跳回哈啰app ---")
        start_app(package_name)
        sleep(2.0)
        print("--- 退出插屏广告返回奖励金页面 ---")
        try:
            anchor_text = poco(textMatches=".*恭喜获得奖励.*")
            if anchor_text.exists():
                print("💡 找到锚点'恭喜获得奖励'！开始寻找关闭按钮...")
                siblings = anchor_text[0].parent().sibling("android.widget.FrameLayout")

                # 遍历兄弟节点，揪出最右侧的 X
                for frame in siblings:
                    img = frame.offspring("android.widget.ImageView")
                    if img.exists():
                        pos = img.attr("pos")
                        # 如果 X 坐标在屏幕右侧 80% 以外，判定为关闭按钮
                        if pos[0] > 0.8:
                            print(f"🎯 成功锁定真正的 'X' 按钮！坐标: [X: {pos[0]:.3f}, Y: {pos[1]:.3f}]")
                            img.click()
                            sleep(2.0)
                            break
            else:
                print("✅ 未发现'恭喜获得奖励'锚点，可能广告已自动退出或无需手动关闭。")
        except Exception as e:
            print(f"❌ 定位插屏广告关闭按钮时发生异常: {e}")
    elif scroll_ad_chars.exists():
        print("💡 检测到【滑动浏览】类广告。")
        start_time = time.time()
        while time.time() - start_time < 30.0:
            wait_time = random.uniform(1.5, 3.0)
            sleep(wait_time)
            current_elapsed = time.time() - start_time
            print(f"[{current_elapsed:.1f}s / 30.0s] 正在模拟人类向下滑动...")
            poco.swipe([0.5, 0.8], [0.5, 0.3], duration=0.5)
        print("✅ 30s 滑动任务结束！直接触发物理返回键...")
        keyevent("BACK")
        sleep(2.0)
    else:
        print("💡 检测到【浏览】类广告。")
        sleep(15.0)
        print("正在寻找关闭按钮...")
        close_btn = poco("close_btn")
        close_container = poco("com.jingyao.easybike:id/tobid_interstitial_skip_ll")
        if close_btn.exists():
            pos = close_btn.attr("pos")
            print(f"🎯 成功锁定 'close_btn'！节点中心坐标为: [X: {pos[0]:.3f}, Y: {pos[1]:.3f}]")
            close_btn.click()
            print("✅ 点击完成！等待观察弹窗是否正常关闭...")
            sleep(3.0)
        elif close_container.wait(10).exists():
            close_container.click()
            sleep(1.0)
        else:
            close_btn = poco(text="反馈").sibling("android.view.View")
            close_btn.click()
            print("✅ 点击完成！等待观察弹窗是否正常关闭...")
            sleep(3.0)

    print("--- 翻倍奖励领取 ---")
    double_reward_btn = poco("com.jingyao.easybike:id/tvExchangeDoubleNextVideo")
    if double_reward_btn.wait(10).exists():
        print("🎁 发现【翻倍领取】弹窗，正在点击获取双倍奖励...")
        double_reward_btn.click()
        sleep(3.0)
        keyevent("BACK")
        sleep(0.5)
    next_video_btn = poco("com.jingyao.easybike:id/rlExchangeNextVideo")
    next_video_btn.click()
    sleep(2.0)




