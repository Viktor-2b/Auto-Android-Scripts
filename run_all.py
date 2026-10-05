import time
from core import connect_device
from apps.hellobike.main import run_daily as hellobike_daily
from apps.taobao.main import run_daily as taobao_daily


def main():
    print("=" * 40)
    print("🚀 开始执行每日全自动日常任务...")
    print("=" * 40)

    # 1. 连接设备
    d = connect_device()

    # 2. 执行哈啰任务
    print("\n🚴 [1/2] 开始执行【哈啰单车】日常任务...")
    try:
        hellobike_daily(d)
        print("✅ 【哈啰单车】任务执行完毕！")
    except Exception as e:
        print(f"❌ 【哈啰单车】执行异常: {e}")

    time.sleep(3.0)

    # 3. 执行淘宝任务
    print("\n🛍️ [2/2] 开始执行【淘宝】日常任务...")
    try:
        taobao_daily(d)
        print("✅ 【淘宝】任务执行完毕！")
    except Exception as e:
        print(f"❌ 【淘宝】执行异常: {e}")

    print("\n" + "=" * 40)
    print("🎉 今日全部自动化日常任务已结束！")
    print("=" * 40)


if __name__ == "__main__":
    main()
