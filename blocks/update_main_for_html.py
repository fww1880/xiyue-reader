# 读取main.py
with open('novel_reader/main.py', 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 load_book 方法中的设置文本部分
old_code = """            content = handler.read_file(file_path)
            self.text_edit.setPlainText(content)"""
new_code = """            content = handler.read_file(file_path)
            
            # 智能识别内容类型：如果是HTML则使用富文本显示，支持图片
            is_html = False
            stripped = content.strip()
            if stripped.startswith('<html') or stripped.startswith('<!DOCTYPE') or '<img' in stripped:
                is_html = True
            
            if is_html:
                self.text_edit.setHtml(content)
            else:
                self.text_edit.setPlainText(content)"""
# 替换
new_content = content.replace(old_code, new_code)
# 写回
with open('novel_reader/main.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("✅ main.py 已更新，支持自动识别并显示HTML和图片！")
utils.set_state(success=True)