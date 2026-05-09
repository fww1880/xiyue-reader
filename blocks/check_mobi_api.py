import mobi
print("详细检查mobi库API...")
# 看看具体有哪些函数可用
print("mobi库的主要函数:")
for attr in dir(mobi):
    if not attr.startswith('_'):
        print(f"  {attr}")
# 看看extract函数
if hasattr(mobi, 'extract'):
    print("\nmobi.extract函数:")
    print(f"  {mobi.extract}")
else:
    print("\n✗ mobi库没有extract函数")
utils.set_state(success=True)