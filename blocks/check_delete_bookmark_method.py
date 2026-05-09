import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
print("🔍 检查删除书签方法...")
start = content.find('def delete_selected_bookmark')
if start == -1:
    print("❌ 找不到 delete_selected_bookmark 方法！这会导致删除书签时报错。")
else:
    end = content.find('\ndef ', start)
    method = content[start:end]
    print(method)