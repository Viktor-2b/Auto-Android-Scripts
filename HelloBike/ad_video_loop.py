# -*- encoding=utf8 -*-
# 文件名: ad_utils.py
import time
import random

def back_to_hellobike(d, package_name):
    current_pkg = d.app_current().get('package')
    if current_pkg != package_name:
        print(f"⚠️ 发现当前偏离到其它APP ({current_pkg})，正在强制拉回哈啰...")
        d.app_start(package_name)
        time.sleep(2.5)

def third_app_allow(d):
    allow_btn = d(text="30天内允许")
    print("--- 正在侦测系统级应用跳转拦截弹窗 ---")
    if allow_btn.wait(timeout=10.0):
        allow_btn.click()
        print("✅ 已授权！系统应该正在拉起第三方APP...")
    else:
        print("✅ 未检测到【30天内允许】弹窗。")
def start_video_ad_loop(d, package_name="com.jingyao.easybike"):
    """
    封装好的核心视频广告处理循环模块
    :param d: uiautomator2 的设备连接对象
    :param package_name: 需要保持的前台应用包名
    """
    print("\n🚀 [模块启动] 初始化视频广告自动化流...")

    # 动态获取当前设备的屏幕尺寸
    screen_width = d.info['displayWidth']
    screen_height = d.info['displayHeight']

    # 四大广告类型特征
    fast_ad_chars = d(textMatches=".*(我要更快拿奖|我要减广告时长|我要立即领奖|立即前往加速).*")
    scroll_ad_chars = d(textMatches=".*(去抖音看|进入直播间|月销量|滑).*")
    jump_ad_chars = d(textMatches=".*(点击打开或下载第三方应用|立即抢购|了解更多).*")
    browse_ad_chars = d(textMatches=".*(反馈).*")

    # 弹窗与关闭/领奖按钮
    anchor_text = d(textMatches=".*恭喜获得奖励.*")
    close_btn_id = d(resourceId="close_btn")
    close_container = d(resourceId="com.jingyao.easybike:id/tobid_interstitial_skip_ll")
    double_reward_btn = d(resourceId="com.jingyao.easybike:id/tvExchangeDoubleNextVideo")
    next_video_btn = d(resourceId="com.jingyao.easybike:id/rlExchangeNextVideo")

    print("--- 正式进入看视频循环 ---")

    # --- 2. 核心状态机循环 ---
    while True:
        try:
            # [优先级 1]：限时快手/抖音等秒杀弹窗
            if fast_ad_chars.wait(timeout=5.0):
                print("⚡ 发现【10秒更快拿奖】限时弹窗！优先执行拦截...")
                fast_ad_chars.click()
                time.sleep(2.0)
                third_app_allow(d)
                print("⏳ 正在第三方APP浏览，等待 12 秒 (满足10秒+容错)...")
                time.sleep(12.0)
                print("🔄 浏览达标！切回哈啰APP...")
                d.app_start(package_name)
                time.sleep(3.0)
            # [优先级 3]：滑动浏览类广告
            elif scroll_ad_chars.exists:
                print("💡 检测到【滑动浏览】类广告。")
                start_time = time.time()
                while time.time() - start_time < 30.0:
                    wait_time = random.uniform(1.5, 3.0)
                    time.sleep(wait_time)
                    current_elapsed = time.time() - start_time
                    print(f"[{current_elapsed:.1f}s / 30.0s] 正在模拟人类向下滑动...")
                    d.swipe(0.5, 0.8, 0.5, 0.3, duration=0.5)
                print("✅ 30s 滑动任务结束！直接触发物理返回键...")
                d.press("back")
                time.sleep(2.0)
            # [优先级 2]：普通跳转类广告
            elif jump_ad_chars.wait(timeout=5.0):
                print("💡 检测到【跳转】类广告。")
                target_btn = jump_ad_chars[-1]
                target_btn.click()
                time.sleep(15.0)

                third_app_allow(d)


                print("--- 跳回哈啰app ---")
                d.app_start(package_name)
                time.sleep(2.0)

                print("--- 退出插屏广告返回奖励金页面 ---")
                try:
                    if anchor_text.exists:
                        print("💡 找到锚点'恭喜获得奖励'！开始寻找关闭按钮...")
                        x_imgs = anchor_text.sibling(className="android.widget.FrameLayout").child(
                            className="android.widget.ImageView")
                        for img in x_imgs:
                            img_bounds = img.info['bounds']
                            img_center_x = ((img_bounds['left'] + img_bounds['right']) / 2) / screen_width
                            img_center_y = ((img_bounds['top'] + img_bounds['bottom']) / 2) / screen_height
                            if img_center_x > 0.8:
                                print(
                                    f"🎯 成功锁定真正的 'X' 按钮！坐标比例: [X: {img_center_x:.3f}, Y: {img_center_y:.3f}]")
                                img.click()
                                time.sleep(2.0)
                                break
                    else:
                        print("✅ 未发现'恭喜获得奖励'锚点，可能广告已自动退出或无需手动关闭。")
                except Exception as e:
                    print(f"❌ 定位插屏广告关闭按钮时发生异常: {e}")



            # [兜底方案]：常规浏览广告
            else:
                print("💡 检测到【浏览】类广告。")
                time.sleep(60.0)
                print("正在寻找关闭按钮...")
                hint_sibling = d.xpath('//android.widget.TextView[@text="已获得惊喜奖励"]/../../../android.widget.FrameLayout')
                if close_btn_id.exists:
                    print("🎯 成功锁定 'close_btn'！")
                    close_btn_id.click()
                    time.sleep(3.0)
                elif close_container.wait(timeout=10.0):
                    close_container.click()
                    time.sleep(1.0)
                elif d(text="已获得惊喜奖励").exists:
                    hint_sibling.click()
                    time.sleep(3.0)
                elif d(text="反馈").exists:
                    close_landscape = d(text="反馈").sibling(className="android.widget.TextView", text="")
                    close_portrait = d(text="反馈").sibling(className="android.view.View")
                    if close_landscape.exists:
                        print("🎯 成功锁定【横屏】隐藏关闭按钮！")
                        close_landscape.click()
                    elif close_portrait.exists:
                        print("🎯 成功锁定【竖屏】隐藏关闭按钮！")
                        close_portrait.click()
                    time.sleep(3.0)
                else:
                    print("⚠️ 第一次尝试未找到任何关闭特征，触发物理返回键...")
                    d.press("back")
                    time.sleep(2.0)

                third_app_allow(d)
                back_to_hellobike(d,package_name)
                if close_btn_id.exists:
                    print("🎯 成功锁定 'close_btn'！")
                    close_btn_id.click()
                    time.sleep(3.0)
                elif close_container.wait(timeout=10.0):
                    close_container.click()
                    time.sleep(1.0)
                elif d(text="跳过").exists:  # <--- 【新增】专门克制右上角出现“跳过”的广告
                    print("🎯 发现【跳过】按钮，奖励已到手，直接退出！")
                    d(text="跳过").click()
                    time.sleep(3.0)
                elif d(text="已获得惊喜奖励").exists:
                    hint_sibling.click()
                    time.sleep(3.0)
                elif d(text="反馈").exists:
                    close_landscape = d(text="反馈").sibling(className="android.widget.TextView", text="")
                    close_portrait = d(text="反馈").sibling(className="android.view.View")
                    if close_landscape.exists:
                        print("🎯 成功锁定【横屏】隐藏关闭按钮！")
                        close_landscape.click()
                    elif close_portrait.exists:
                        print("🎯 成功锁定【竖屏】隐藏关闭按钮！")
                        close_portrait.click()
                    time.sleep(3.0)
            back_to_hellobike(d,package_name)

            print("--- 翻倍奖励领取 ---")
            if double_reward_btn.wait(timeout=3.0):
                print("🎁 发现【翻倍领取】弹窗，正在点击获取双倍奖励...")
                double_reward_btn.click()
                time.sleep(3.0)
                d.press("back")
                time.sleep(0.5)
            back_to_hellobike(d,package_name)
            if next_video_btn.exists:
                next_video_btn.click()
            else:
                d.press("back")
                time.sleep(0.5)
            time.sleep(2.0)

        except Exception as e:
            print(f"⚠️ 核心循环发生异常: {e}")
            time.sleep(2.0)