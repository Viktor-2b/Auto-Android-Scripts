import xml.etree.ElementTree as ElementTree
from utils import connect_device


d = connect_device()

print("--- 正在侦测系统前台环境 ---")
current_app = d.app_current()
current_pkg = current_app.get('package', '')
current_act = current_app.get('activity', '')
print(f"📱 当前打开的 APP 包名: {current_pkg}")
print(f"📄 当前所处的 Activity: {current_act}")

print("\n--- 开始读取并分析当前屏幕 UI ---")

try:
    print("【正在一次性获取整棵 UI 树 (dump)】...")
    # u2 直接获取 Android 底层的 XML 格式 UI 树
    ui_tree_xml = d.dump_hierarchy()

    # 存入本地 XML 文件 (注意后缀变成了 xml)
    with open("debug/ui_tree_dump.xml", "w", encoding="utf-8") as f:
        f.write(ui_tree_xml)
    print("✅ 完整的 UI 树数据已保存到 ui_tree_dump.xml！")

    # --- 在 Python 本地解析 XML 提取文字 ---
    print("\n【当前屏幕上的文字有】：")

    # 将字符串形式的 XML 解析为树对象
    root = ElementTree.fromstring(ui_tree_xml)

    # 遍历所有 <node> 标签
    for node in root.iter('node'):
        # 在 Android 原生 XML 中，文字主要存在于 text 和 content-desc 属性中
        text = node.attrib.get('text', '')
        content_desc = node.attrib.get('content-desc', '')

        # 优先获取 text，如果没有 text 但有 content-desc (无障碍描述) 也抓取下来
        display_text = text if text else content_desc

        # 过滤掉空字符串
        if display_text and display_text.strip():
            print(f"-> {display_text.strip()}")

except Exception as e:
    print(f"❌ 读取 UI 树时发生错误: {e}")

print("\n侦查脚本运行结束。")