

# ==========================================
# 4. 看视频任务循环
# ==========================================
max_tasks = 5  # 任务次数
task_count = 0
while task_count < max_tasks:
    task_count += 1
    print(f"\n>>> 正在执行第 {task_count}/{max_tasks} 次任务循环 <<<")
    print("正在寻找【看视频】任务...")
    video_task_title = poco(text="看视频领大量奖励金")

    if video_task_title.wait(10).exists():
        print("✅ 找到【看视频领大量奖励金】任务！")
        accept_btn = video_task_title.parent().sibling(text="领任务")
        watch_btn = video_task_title.parent().sibling(text="去观看")
        if accept_btn.exists():
            print("🎯 锁定目标按钮，正在点击...")
            accept_btn.click()
            print("已点击！等待视频任务页面弹出...")
            sleep(5.0)
        elif watch_btn.exists():
            print("🎯 锁定目标按钮，正在点击...")
            watch_btn.click()
            print("已点击！等待视频任务页面弹出...")
            sleep(5.0)
        else:
            raise Exception("❌ 未能在'奖励金'页面找到按钮。")
    else:
        raise Exception("❌ 未能在'奖励金'页面找到【看视频】入口。")
    # 定义各类广告的特征锚点
    jump_ad_chars = poco(textMatches=".*(点击打开或下载第三方应用|立即抢购|了解更多|立即领取).*")
    scroll_ad_chars = poco(textMatches=".*(去抖音看).*")
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
            print("⚠️ 未能找到 'close_btn'，请确认界面是否变化。")
        raise Exception("❌ 广告关闭定位过程中发生异常: {e}")

    print("--- 奖励金页面领取奖励 ---")
    reward_btn = poco(text="领奖励")
    if reward_btn.wait(10).exists():
        print("💰 发现【领奖励】按钮！点击...")
        reward_btn.click()
        print("✅ 奖励已领取！准备进行下一次循环。")
        sleep(2.0)  # 给领奖动画留点时间
    else:
        raise Exception("❌ 未能在'奖励金'页面找到按钮。")
    print("--- 检测是否有限时奖励弹出 ---")
    limit_time_btn = poco("com.jingyao.easybike:id/btnRewardClickWithAds")
    if limit_time_btn.exists():
        print("🎁 发现【限时奖励】！正在点击追加奖励...")
        limit_time_btn.click()
        sleep(3.0)
        start_app(package_name)
        sleep(2.0)
        close_btn =  poco("com.jingyao.easybike:id/ivClose")
        if close_btn.exists():
            print("⚠️ 发现关闭按钮！正在点击中下方的 'X' 按钮关闭...")
            close_btn.click()
            sleep(0.5)
    else:
        print("✅ 未发现【限时奖励】弹窗。")
print("自动脚本运行结束。")