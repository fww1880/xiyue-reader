import os
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 修复 restore_state 中的方法名
old_call = '            self.open_book(last_book)'
new_call = '            self.load_book(last_book)'
content = content.replace(old_call, new_call)
print("✅ 已将 restore_state 中的 open_book 改为 load_book")
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("💾 已保存修改")