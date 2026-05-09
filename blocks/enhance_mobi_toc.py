import os
novel_reader_dir = os.path.join(os.getcwd(), 'novel_reader')
main_file = os.path.join(novel_reader_dir, 'main.py')
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()
# ===== 增强 HTML 格式的目录识别逻辑 =====
old_html_parse = '''        if is_html:
            # HTML格式：匹配<h1>-<h6>标签作为章节
            pattern = r'<h[1-6][^>]*>(.*?)</h[1-6]>'
            for match in re.finditer(pattern, content, re.IGNORECASE):
                title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                pos = match.start()
                if title:
                    self.chapter_positions.append((title, pos))'''
new_html_parse = '''        if is_html:
            # HTML格式：多重策略识别章节标题
            import re
            from bs4 import BeautifulSoup
            
            # 策略1：优先匹配<h1>-<h6>标签
            h_pattern = r'<h[1-6][^>]*>(.*?)</h[1-6]>'
            for match in re.finditer(h_pattern, content, re.IGNORECASE):
                title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                # 过滤太短或包含广告词的标题
                if title and len(title) > 2 and not any(kw in title for kw in ['Copyright', '版权', 'www.', 'http']):
                    self.chapter_positions.append((title, match.start()))
            
            # 策略2：如果<h1>-<h6>没找到，尝试匹配常见章节class/id
            if not self.chapter_positions:
                soup = BeautifulSoup(content, 'html.parser')
                chapter_patterns = [
                    {'name': True, 'class': lambda c: c and any('chapter' in str(x).lower() or 'title' in str(x).lower() for x in c)},
                    {'name': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']},
                    {'name': 'p', 'class': lambda c: c and any('title' in str(x).lower() or 'chapter' in str(x).lower() for x in c)},
                    {'name': 'div', 'class': lambda c: c and any('chapter' in str(x).lower() or 'title' in str(x).lower() for x in c)},
                ]
                
                for tag in soup.find_all(lambda tag: any(
                    (pattern.get('name') is None or pattern.get('name') == True or tag.name == pattern['name']) and
                    (pattern.get('class') is None or (tag.get('class') and pattern['class'](tag.get('class'))))
                    for pattern in chapter_patterns
                )):
                    title = tag.get_text(strip=True)
                    # 检查是否像章节标题
                    if title and len(title) > 2 and len(title) < 100:
                        if re.match(r'^\\s*(第 [一二三四五六七八九十百千万零 0-9]+[章章节卷部篇集]|Chapter\\s+[0-9IVXLCDM]+|Part\\s+[0-9IVXLCDM]+)', title, re.IGNORECASE):
                            # 找到在原始content中的位置
                            pos = content.find(title)
                            if pos != -1:
                                self.chapter_positions.append((title, pos))
                                if len(self.chapter_positions) >= 5:  # 找到几个就够了
                                    break
            
            # 策略3：如果还是没找到，尝试从文本内容中查找（兼容纯文本风格的HTML）
            if not self.chapter_positions:
                text_content = BeautifulSoup(content, 'html.parser').get_text('\\n')
                lines = text_content.split('\\n')
                chapter_patterns_text = [
                    r'^\\s*第 [一二三四五六七八九十百千万零 0-9]+[章章节卷部篇集]\\s*.*$',
                    r'^\\s*Chapter\\s+[0-9IVXLCDM]+[.:、\\s].*$',
                    r'^\\s*Part\\s+[0-9IVXLCDM]+[.:、\\s].*$',
                ]
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if not stripped or len(stripped) > 100:
                        continue
                    for pat in chapter_patterns_text:
                        if re.match(pat, stripped, re.IGNORECASE):
                            pos = text_content[:i].count('\\n')  # 估算位置
                            self.chapter_positions.append((stripped, pos))
                            break'''
content = content.replace(old_html_parse, new_html_parse)
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ MOBI目录识别增强完成！")
print("改进内容：")
print("1. 优先匹配<h1>-<h6>标准标题标签")
print("2. 其次匹配带有chapter/title类名的标签")
print("3. 最后从HTML提取的纯文本中查找章节标题")
print("4. 过滤广告词和过短的无效标题")