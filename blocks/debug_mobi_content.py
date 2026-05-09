import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'novel_reader'))
from file_handler import FileHandler
# 查找当前目录下的 MOBI 文件
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
test_mobi = None
for root, dirs, files in os.walk(os.getcwd()):
    for f in files:
        if f.lower().endswith('.mobi'):
            test_mobi = os.path.join(root, f)
            break
    if test_mobi: break
if not test_mobi:
    print("❌ 未找到 MOBI 测试文件，请确保目录下有 MOBI 文件")
else:
    print(f"🔍 测试文件：{test_mobi}")
    handler = FileHandler()
    content = handler.read_mobi(test_mobi)
    
    print(f"📄 内容长度：{len(content)}")
    print("\n📋 内容前 2000 字符：")
    print(content[:2000])
    
    # 检查是否有章节标题特征
    import re
    patterns = [
        r'<h[1-6]',
        r'class="chapter"',
        r'class="title"',
        r'第[一二三四五六七八九十百千万零0-9]+[章章节卷部篇集]',
        r'Chapter\s+[0-9IVXLCDM]+'
    ]
    print("\n🔎 特征匹配检查：")
    for pat in patterns:
        matches = re.findall(pat, content, re.IGNORECASE)
        print(f"  匹配 '{pat}': 找到 {len(matches)} 处")
        if matches:
            print(f"    示例：{matches[:3]}")