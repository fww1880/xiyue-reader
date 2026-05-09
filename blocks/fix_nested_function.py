import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# 把嵌套的 refresh_bookmark_list 挪出来，修复缩进
# 从行1059开始，整个方法都多了一层缩进，需要去掉一层
# 找出从哪里开始到哪里结束
start_line = 1058  # 从函数定义开始
end_line = start_line
while end_line < len(lines) and (lines[end_line].startswith('        ') or lines[end_line].strip() == ''):
    end_line += 1
# end_line 现在是下一个顶级函数（缩进4）或者结尾
print(f"🔍 嵌套方法范围：行 {start_line+1} - {end_line}")
# 去掉一层缩进（每个行去掉前8个空格，即4个缩进）
for i in range(start_line, end_line):
    if lines[i].startswith('        '):  # 8个空格
        lines[i] = lines[i][4:]
print("✅ 已去除一层缩进，将方法拉出嵌套")
# 保存
with open(main_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("🚀 修复完成！")