import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'novel_reader'))
with open(os.path.join(os.getcwd(), 'novel_reader', 'main.py'), 'r', encoding='utf-8') as f:
    content = f.read()
print(content)