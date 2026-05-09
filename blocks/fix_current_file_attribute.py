import os, re
novel_reader_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj\novel_reader'
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# 找到 save_bookmarks 函数
print("🔍 检查 save_bookmarks 函数...")
match = re.search(r'def save_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match:
    func_code = match.group()
    print(f"当前代码：\n{func_code}")
    # 检查是否访问了 self.current_file
    if 'self.current_file' in func_code:
        print("\n⚠️ 找到问题：save_bookmarks 访问了 self.current_file，但实际上应该是 self.current_book_path！")
        # 替换为正确的变量名，同时保留检查
        new_func = '''    def save_bookmarks(self):
        """保存书签到本地"""
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            return
        key = "bookmarks_" + hash(self.current_book_path).__str__()
        data = getattr(self, 'bookmark_list', [])
        # 保存到文件（最可靠的方式）
        bookmark_file = self.current_book_path + '.bookmarks'
        try:
            with open(bookmark_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # 也保存到 QSettings 作为备份
            self.settings.setValue(key, data)
        except Exception as e:
            print(f"⚠️ 书签保存失败：{e}")'''
        # 替换
        content = content.replace(func_code, new_func)
        print("✅ 已修复：将 self.current_file 改为 self.current_book_path")
    else:
        print("✅ 没有找到 current_file 错误")
# 检查 load_bookmarks 函数是否也有同样问题
print("\n🔍 检查 load_bookmarks 函数...")
match_load = re.search(r'def load_bookmarks\(self\):.*?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match_load:
    load_code = match_load.group()
    print(f"load_bookmarks：\n{load_code}")
    if 'self.current_file' in load_code:
        print("\n⚠️ load_bookmarks 也有问题！修复...")
        new_load = '''    def load_bookmarks(self):
        """加载书签"""
        if not hasattr(self, 'current_book_path') or not self.current_book_path:
            return
        # 先从文件加载
        bookmark_file = self.current_book_path + '.bookmarks'
        self.bookmark_list = []
        try:
            if os.path.exists(bookmark_file):
                with open(bookmark_file, 'r', encoding='utf-8') as f:
                    self.bookmark_list = json.load(f)
            else:
                # 从 QSettings 加载作为备份
                key = "bookmarks_" + hash(self.current_book_path).__str__()
                saved = self.settings.value(key, [])
                if saved:
                    self.bookmark_list = saved
            print(f"✅ 已加载 {len(self.bookmark_list)} 个书签")
        except Exception as e:
            print(f"⚠️ 书签加载失败：{e}")
            self.bookmark_list = []'''
        content = content.replace(load_code, new_load)
        print("✅ 已修复 load_bookmarks 中的 current_file 错误")
    else:
        print("✅ load_bookmarks 没有问题")
# 保存修改
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("\n💾 修改已保存")
# 语法检查
import ast
try:
    ast.parse(content)
    print("✅ 语法检查通过")
except SyntaxError as e:
    print(f"❌ 语法错误：{e} 第 {e.lineno} 行")
# 验证
print("\n📋 验证：")
if 'self.current_file' not in content:
    print("✅ 已删除所有 current_file 引用")
else:
    print("⚠️ 还有 current_file 引用，需要继续修复")
    matches = re.findall('self\.current_file', content)
    print(f"   剩余 {len(matches)} 处")