import re
class TextProcessor:
    """文本处理工具类，提供文本清理优化功能"""
    
    def clean_text(self, text):
        """清理文本：去多余空行、去广告杂质、去乱码"""
        # 移除多余空行（超过2个空行变成1个）
        cleaned = re.sub(r'\n\s*\n', '\n\n', text)
        
        # 移除常见广告水印
        ad_patterns = [
            r'网站:.*\n',
            r'网址:.*\n',
            r'更多.*请访问.*\n',
            r'.*手打小说网.*\n',
            r'.*更新最快.*\n',
            r'本章未完.*\n',
        ]
        for pattern in ad_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
            
        # 移除乱码控制字符
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned)
        
        # 去掉首尾空白
        cleaned = cleaned.strip()
        
        return cleaned
        
    def simple_to_traditional(self, text):
        """简体转繁体（简单实现，完整版需要opencc）"""
        # 这里用一个简单的映射示例，实际建议使用opencc库
        simple_map = {
            '为': '為', '会': '會', '可以': '可以',
            # 实际完整转换需要字典，这里占位
        }
        result = text
        for s, t in simple_map.items():
            result = result.replace(s, t)
        return result
        
    def traditional_to_simple(self, text):
        """繁体转简体"""
        traditional_map = {
            '為': '为', '會': '会',
        }
        result = text
        for t, s in traditional_map.items():
            result = result.replace(t, s)
        return result
        
    def batch_replace(self, text, replacements):
        """批量替换文本
        replacements: 字典 {old: new}
        """
        result = text
        for old, new in replacements.items():
            result = result.replace(old, new)
        return result
        
    def detect_chapters(self, text):
        """智能识别章节，生成章节列表"""
        # 常见章节匹配规则
        chapter_patterns = [
            r'^第[一二三四五六七八九十百千]+章.*$',
            r'^第\d+章.*$',
            r'^Chapter\s*\d+.*$',
        ]
        
        chapters = []
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            for pattern in chapter_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    chapters.append({
                        'title': line,
                        'line_number': i
                    })
                    break
                    
        return chapters
        
    def generate_table_of_contents(self, text):
        """生成目录文本"""
        chapters = self.detect_chapters(text)
        if not chapters:
            return "未识别到章节，无法生成目录\n"
            
        toc = ["目录\n=====\n\n"]
        for i, chap in enumerate(chapters, 1):
            toc.append(f"{i}. {chap['title']}\n")
            
        return ''.join(toc)