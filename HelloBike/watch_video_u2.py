# -*- encoding=utf8 -*-
import time
import uiautomator2 as u2
from HelloBike.ad_video_loop import start_video_ad_loop

package_name = "com.jingyao.easybike"
print("正在尝试连接手机...")
d = u2.connect()
print(f"手机连接成功！")

watch_video_btn = d(text="看视频")
if watch_video_btn.exists:
    watch_video_btn.click()
time.sleep(5.0)
start_video_ad_loop(d, package_name)