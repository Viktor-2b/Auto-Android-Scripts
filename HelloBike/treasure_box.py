# -*- encoding=utf8 -*-
import uiautomator2 as u2
import time
import random

# ==========================================
# 1. 基础环境初始化
# ==========================================
print("正在尝试连接手机...")
d = u2.connect()
print(f"手机连接成功！设备型号: {d.info.get('model')}")
package_name = "com.jingyao.easybike"
screen_width = d.info['displayWidth']
screen_height = d.info['displayHeight']

print("正在寻找悬浮宝箱...")
treasure_box = d(resourceId="treasure_box_float")
if treasure_box.exists:
    print("🎁 发现宝箱 ID，正在点击...")
    treasure_box.click()
else:
    print("⚠️ UI树中未找到宝箱，尝试物理坐标盲点...")
    d.click(0.85, 0.85)
time.sleep(1.0)

btn_38 = d(text="选38奖励金")
btn_watch = d(text="看视频最高再领10000币")
if btn_38.exists:
    print("🎯 发现【选38奖励金】大额按钮，执行点击！")
    btn_38.click()
elif btn_watch.exists:
    print("🎯 发现【看视频最高再领10000币】按钮，执行点击！")
    btn_watch.click()

time.sleep(2.0)

watch_video_btn = d(text="看视频")
jump_ad_chars = d(textMatches=".*(点击打开或下载第三方应用|立即抢购|了解更多|立即领取).*")
scroll_ad_chars = d(textMatches=".*(去抖音看).*")
browse_ad_chars = d(textMatches=".*(反馈).*")
fast_ad_chars = d(textMatches=".*(我要更快拿奖|我要减广告时长|我要立即领奖).*")

# 提前定义好后续要用的各种关闭/领奖按钮
allow_btn = d(text="30天内允许")
anchor_text = d(textMatches=".*恭喜获得奖励.*")
close_btn_id = d(resourceId="close_btn")
close_container = d(resourceId="com.jingyao.easybike:id/tobid_interstitial_skip_ll")
double_reward_btn = d(resourceId="com.jingyao.easybike:id/tvExchangeDoubleNextVideo")
next_video_btn = d(resourceId="com.jingyao.easybike:id/rlExchangeNextVideo")

# ==========================================
# 3. 点击看视频触发循环
# ==========================================
print("--- 看视频循环 ---")

while True:
    try:
        if watch_video_btn.exists:
            watch_video_btn.click()

        time.sleep(5.0)
        if fast_ad_chars.exists:
            print("⚡ 发现【10秒更快拿奖】限时弹窗！优先执行拦截...")
            fast_ad_chars.click()
            time.sleep(2.0)

            if allow_btn.exists:
                allow_btn.click()
                print("✅ 已授权跳转...")

            print("⏳ 正在第三方APP浏览，等待 12 秒 (满足10秒+容错)...")
            time.sleep(12.0)

            print("🔄 浏览达标！切回哈啰APP...")
            d.app_start(package_name)
            time.sleep(3.0)
        elif jump_ad_chars.wait(timeout=5.0):
            print("💡 检测到【跳转】类广告。")
            target_btn = jump_ad_chars[-1]
            target_btn.click()
            time.sleep(15.0)

            print("--- 正在侦测系统级应用跳转拦截弹窗 ---")
            if allow_btn.wait(timeout=10.0):
                allow_btn.click()
                print("✅ 已授权！系统应该正在拉起第三方APP...")
            else:
                print("✅ 未检测到【30天内允许】弹窗。")

            print("--- 跳回哈啰app ---")
            d.app_start(package_name)
            time.sleep(2.0)

            print("--- 退出插屏广告返回奖励金页面 ---")
            try:
                if anchor_text.exists:
                    print("💡 找到锚点'恭喜获得奖励'！开始寻找关闭按钮...")

                    # u2 支持直接链式查找兄弟节点下的子节点，并且可以直接用 for 循环遍历
                    x_imgs = anchor_text.sibling(className="android.widget.FrameLayout").child(
                        className="android.widget.ImageView")

                    for img in x_imgs:
                        img_bounds = img.info['bounds']
                        # 取 X 轴的中心像素点，除以屏幕总宽，得到 0~1 的比例
                        img_center_x = ((img_bounds['left'] + img_bounds['right']) / 2) / screen_width
                        img_center_y = ((img_bounds['top'] + img_bounds['bottom']) / 2) / screen_height

                        # 如果 X 坐标在屏幕右侧 80% 以外，判定为关闭按钮
                        if img_center_x > 0.8:
                            print(f"🎯 成功锁定真正的 'X' 按钮！坐标比例: [X: {img_center_x:.3f}, Y: {img_center_y:.3f}]")
                            img.click()
                            time.sleep(2.0)
                            break
                else:
                    print("✅ 未发现'恭喜获得奖励'锚点，可能广告已自动退出或无需手动关闭。")
            except Exception as e:
                print(f"❌ 定位插屏广告关闭按钮时发生异常: {e}")

        elif scroll_ad_chars.exists:
            print("💡 检测到【滑动浏览】类广告。")
            start_time = time.time()
            while time.time() - start_time < 30.0:
                wait_time = random.uniform(1.5, 3.0)
                time.sleep(wait_time)
                current_elapsed = time.time() - start_time
                print(f"[{current_elapsed:.1f}s / 30.0s] 正在模拟人类向下滑动...")
                # u2 滑动也是传入 0~1 的比例
                d.swipe(0.5, 0.8, 0.5, 0.3, duration=0.5)

            print("✅ 30s 滑动任务结束！直接触发物理返回键...")
            d.press("back")
            time.sleep(2.0)

        else:
            print("💡 检测到【浏览】类广告。")
            time.sleep(30.0)
            print("正在寻找关闭按钮...")

            # 定位反馈按钮的兄弟节点
            feedback_sibling = d(text="反馈").sibling(className="android.view.View")

            if close_btn_id.exists:
                bounds = close_btn_id.info['bounds']
                cx = ((bounds['left'] + bounds['right']) / 2) / screen_width
                cy = ((bounds['top'] + bounds['bottom']) / 2) / screen_height
                print(f"🎯 成功锁定 'close_btn'！节点中心坐标为: [X: {cx:.3f}, Y: {cy:.3f}]")
                close_btn_id.click()
                print("✅ 点击完成！等待观察弹窗是否正常关闭...")
                time.sleep(3.0)

            elif close_container.wait(timeout=10.0):
                close_container.click()
                time.sleep(1.0)

            elif d(text="反馈").exists:
                feedback_sibling.click()
                print("✅ 点击完成！等待观察弹窗是否正常关闭...")
                time.sleep(3.0)
        current_pkg = d.app_current().get('package')
        if current_pkg != package_name:
            print(f"⚠️ 发现当前偏离到其它APP ({current_pkg})，正在强制拉回哈啰...")
            d.app_start(package_name)
            time.sleep(2.5)  # 给 APP 从后台唤醒和页面渲染预留充足时间
        print("--- 翻倍奖励领取 ---")
        if double_reward_btn.wait(timeout=3.0):
            print("🎁 发现【翻倍领取】弹窗，正在点击获取双倍奖励...")
            double_reward_btn.click()
            time.sleep(3.0)
            d.press("back")
            time.sleep(0.5)

        if next_video_btn.exists:
            next_video_btn.click()

        time.sleep(2.0)

    except Exception as e:
        print(f"⚠️ 核心循环发生异常: {e}")
        time.sleep(2.0)