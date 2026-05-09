import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 修复 1404-1420 行的正确缩进
# 函数定义是 4 空格，内容是 8 空格
fixed_lines = []
for i, line in enumerate(lines):
    if i == 1404:
        # 函数定义：4 空格
        fixed_lines.append('    def save_bookmarks(self):\n')
    elif i == 1405:
        # docstring：8 空格
        fixed_lines.append('        """保存书签到本地"""\n')
    elif i == 1406:
        fixed_lines.append('        if not hasattr(self, \'current_book_path\') or not self.current_book_path:\n')
    elif i == 1407:
        fixed_lines.append('            return\n')
    elif i == 1408:
        fixed_lines.append('        key = "bookmarks_" + hash(self.current_book_path).__str__()\n')
    elif i == 1409:
        fixed_lines.append('        data = getattr(self, \'bookmark_list\', [])\n')
    elif i == 1410:
        fixed_lines.append('        # 保存到文件（最可靠的方式）\n')
    elif i == 1411:
        fixed_lines.append('        bookmark_file = self.current_book_path + \'.bookmarks\'\n')
    elif i == 1412:
        fixed_lines.append('        try:\n')
    elif i == 1413:
        fixed_lines.append('            with open(bookmark_file, \'w\', encoding=\'utf-8\') as f:\n')
    elif i == 1414:
        fixed_lines.append('                json.dump(data, f, ensure_ascii=False, indent=2)\n')
    elif i == 1415:
        fixed_lines.append('            # 也保存到 QSettings 作为备份\n')
    elif i == 1416:
        fixed_lines.append('            self.settings.setValue(key, data)\n')
    elif i == 1417:
        fixed_lines.append('        except Exception as e:\n')
    elif i == 1418:
        fixed_lines.append('            print(f"⚠️ 书签保存失败：{e}")\n')
    else:
        fixed_lines.append(line)
# 重新组合
content = ''.join(fixed_lines)
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 已修复缩进")
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
    lines = content.split('\n')
    for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+5)):
        print(f"{i+1:4d}: {repr(lines[i])}")