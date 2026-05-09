import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 检查1050-1070行
print("🔍 检查错误区域 (行号 1050-1070):")
for i in range(1049, min(1070, len(lines))):
    print(f"L{i+1}: {repr(lines[i])}")
# 修复缩进
# 一般这种情况是函数定义下没有缩进内容
if len(lines) >= 1059:
    # 查看函数定义行
    def_line = lines[1058].rstrip()
    print(f"\n函数定义行: {repr(def_line)}")
    if 'def ' in def_line and lines[1059].strip() and not lines[1059].startswith(' '):
        # 需要缩进
        lines[1059] = '        ' + lines[1059].lstrip()
        print("✅ 已修复缩进！")
        with open(main_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    else:
        print("⚠️ 未找到预期错误，手动检查")