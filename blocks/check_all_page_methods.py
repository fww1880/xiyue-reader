import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("=" * 60)
print("🔍 检查所有 prev_page/next_page 方法：")
print("=" * 60)
# 查找所有 def prev_page 和 def next_page
prev_count = 0
next_count = 0
has_animation = 0
for i, line in enumerate(lines):
    if 'def prev_page' in line:
        prev_count += 1
        # 检查下面几行是否有 QPropertyAnimation
        found_anim = False
        for j in range(i, min(len(lines), i+20)):
            if 'QPropertyAnimation' in lines[j]:
                found_anim = True
                has_animation += 1
                break
        if found_anim:
            print(f"  ✅ L{i+1} prev_page 已有动画")
        else:
            print(f"  ❌ L{i+1} prev_page 没有动画")
    if 'def next_page' in line:
        next_count += 1
        found_anim = False
        for j in range(i, min(len(lines), i+20)):
            if 'QPropertyAnimation' in lines[j]:
                found_anim = True
                has_animation += 1
                break
        if found_anim:
            print(f"  ✅ L{i+1} next_page 已有动画")
        else:
            print(f"  ❌ L{i+1} next_page 没有动画")
print(f"\n统计：{prev_count} 个 prev_page, {next_count} 个 next_page，共 {has_animation}/{prev_count+next_count} 个有动画")