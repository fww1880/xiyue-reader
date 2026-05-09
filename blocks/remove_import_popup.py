import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到导入完成后的弹窗
old_import_popup = '''            QMessageBox.information(self, "导入完成", f"文件夹 {category_name} 已导入书架\\n共导入 {total_files} 本小说")'''
new_no_popup = '''            # 去掉导入确认弹窗，直接导入
            print(f"文件夹 {category_name} 已导入书架，共导入 {total_files} 本小说")'''
content = content.replace(old_import_popup, new_no_popup)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 修改完成！导入文件夹不再弹出确认弹窗")