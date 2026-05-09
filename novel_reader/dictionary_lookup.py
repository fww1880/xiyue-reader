import requests
import json
class DictionaryLookup:
    """联网查词典工具类"""
    
    def __init__(self):
        self.history = []
        self.api_url = "https://dict.api.aipyaipy.com/lookup"
        self.search_url = "https://search.api.aipyaipy.com/search"
        
    def lookup_word(self, word, source="general"):
        """查询单词/成语/生僻字"""
        try:
            # 使用免费开放的词典API
            params = {
                "word": word,
                "source": source
            }
            response = requests.get(self.api_url, params=params, timeout=5)
            if response.status_code == 200:
                result = response.json()
                
                # 保存到历史记录
                self.history.append({
                    "word": word,
                    "result": result,
                    "type": "lookup"
                })
                
                return True, result
            else:
                return False, f"查询失败，HTTP状态码: {response.status_code}"
                
        except Exception as e:
            return False, str(e)
            
    def web_search(self, query):
        """搜索词义/背景"""
        try:
            params = {
                "q": query
            }
            response = requests.get(self.search_url, params=params, timeout=10)
            if response.status_code == 200:
                result = response.json()
                
                self.history.append({
                    "word": query,
                    "result": result,
                    "type": "search"
                })
                
                return True, result
            else:
                return False, f"搜索失败，HTTP状态码: {response.status_code}"
                
        except Exception as e:
            return False, str(e)
            
    def format_result(self, result):
        """格式化查询结果为可读文本"""
        output = []
        
        if "word" in result:
            output.append(f"词语：{result['word']}")
            
        if "pinyin" in result:
            output.append(f"拼音：{result['pinyin']}")
            
        if "word_type" in result:
            output.append(f"词性：{result['word_type']}")
            
        if "definition" in result:
            output.append(f"\n释义：")
            definitions = result['definition']
            if isinstance(definitions, list):
                for i, defin in enumerate(definitions, 1):
                    output.append(f"  {i}. {defin}")
            else:
                output.append(f"  {definitions}")
                
        if "examples" in result and result['examples']:
            output.append(f"\n例句：")
            for example in result['examples']:
                output.append(f"  - {example}")
                
        if "abstract" in result:
            output.append(f"\n摘要：{result['abstract']}")
            
        return '\n'.join(output)
        
    def get_history(self):
        """获取查询历史"""
        return self.history
        
    def export_history(self, output_path):
        """导出查询历史"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)