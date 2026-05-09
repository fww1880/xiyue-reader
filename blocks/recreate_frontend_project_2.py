import os, json
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🏗️ 重新创建前端项目结构...")
# 创建 index.html
index_html = """<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>喜阅阅读器 - Novel Reader</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
"""
with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ 创建 index.html")
# 创建 src 目录
src_dir = os.path.join(base_dir, 'src')
os.makedirs(src_dir, exist_ok=True)
# 创建 main.js
main_js = """import { createApp } from 'vue'
import App from './App.vue'
import './style.css'
createApp(App).mount('#app')
"""
with open(os.path.join(src_dir, 'main.js'), 'w', encoding='utf-8') as f:
    f.write(main_js)
print("✅ 创建 src/main.js")
# 创建 App.vue
app_vue = """<template>
  <div id="app">
    <header class="app-header">
      <h1>📖 喜阅阅读器</h1>
      <div class="file-input">
        <label for="file-upload" class="upload-btn">打开书籍</label>
        <input id="file-upload" type="file" accept=".epub,.txt,.pdf" @change="handleFileChange" />
      </div>
    </header>
    <main class="app-main">
      <div v-if="!currentBook" class="welcome">
        <p>欢迎使用喜阅阅读器，请点击右上角打开一本小说开始阅读吧 👋</p>
        <p>支持格式：EPUB / TXT / PDF</p>
      </div>
      <div v-else id="reader-container" ref="readerContainer">
        <div class="reader-content" ref="readerContent">
          <div v-if="currentFormat === 'epub'" id="epub-container"></div>
          <div v-if="currentFormat === 'txt'" class="txt-content" v-html="formattedTxt"></div>
          <div v-if="currentFormat === 'pdf'" id="pdf-container"></div>
        </div>
      </div>
    </main>
    <footer class="app-footer">
      <span v-if="currentBook">{{ currentBook.title }}</span>
    </footer>
  </div>
</template>
<script>
import { ref, onMounted, computed } from 'vue'
import EPUBJS from 'epubjs'
import * as PDFJS from 'pdfjs-dist'
PDFJS.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.js',
  import.meta.url
).toString()
export default {
  name: 'App',
  setup() {
    const currentBook = ref(null)
    const currentFormat = ref('')
    const currentBlob = ref(null)
    const txtContent = ref('')
    const epub = ref(null)
    const pdfDoc = ref(null)
    const handleFileChange = (event) => {
      const file = event.target.files[0]
      if (!file) return
      const extension = file.name.split('.').pop().toLowerCase()
      currentFormat.value = extension
      currentBlob.value = file
      const reader = new FileReader()
      reader.onload = (e) => {
        if (extension === 'epub') {
          loadEpub(e.target.result)
        } else if (extension === 'txt') {
          loadTxt(e.target.result)
        } else if (extension === 'pdf') {
          loadPdf(e.target.result)
        }
      }
      if (extension === 'txt') {
        reader.readAsText(file, 'UTF-8')
      } else {
        reader.readAsArrayBuffer(file)
      }
      currentBook.value = {
        title: file.name,
        file: file
      }
    }
    const loadEpub = (arrayBuffer) => {
      if (epub.value) {
        epub.value.destroy()
      }
      const blob = new Blob([arrayBuffer])
      epub.value = EPUBJS(blob)
      epub.value.renderTo('epub-container')
    }
    const loadTxt = (text) => {
      txtContent.value = text
    }
    const loadPdf = async (arrayBuffer) => {
      pdfDoc.value = await PDFJS.getDocument(arrayBuffer).promise
      const container = document.getElementById('pdf-container')
      container.innerHTML = ''
      for (let i = 1; i <= pdfDoc.value.numPages; i++) {
        const page = await pdfDoc.value.getPage(i)
        const canvas = document.createElement('canvas')
        canvas.className = 'pdf-page'
        const viewport = page.getViewport({ scale: 1.5 })
        canvas.height = viewport.height
        canvas.width = viewport.width
        container.appendChild(canvas)
        const context = canvas.getContext('2d')
        await page.render({ canvasContext: context, viewport: viewport }).promise
      }
    }
    const formattedTxt = computed(() => {
      if (!txtContent.value) return ''
      return txtContent.value.replace(/\\n/g, '<br>')
    })
    const readerContainer = ref(null)
    const readerContent = ref(null)
    onMounted(() => {})
    return {
      currentBook,
      currentFormat,
      formattedTxt,
      handleFileChange,
      readerContainer,
      readerContent
    }
  }
}
</script>
<style scoped>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.app-header {
  background: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
}
.upload-btn {
  background: #42b983;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
#file-upload {
  display: none;
}
.app-main {
  flex: 1;
  overflow: auto;
  background: #f5f5f5;
  padding: 1rem;
}
.welcome {
  text-align: center;
  margin-top: 10vh;
  font-size: 1.2rem;
  color: #666;
}
#epub-container {
  background: white;
  min-height: 100%;
  padding: 2rem;
}
.txt-content {
  background: white;
  min-height: 100%;
  padding: 2rem;
  line-height: 1.8;
  font-size: 1.1rem;
}
.pdf-page {
  display: block;
  margin: 1rem auto;
  box-shadow: 0 0 5px rgba(0,0,0,0.3);
}
.app-footer {
  background: #2c3e50;
  color: #ccc;
  padding: 0.5rem 2rem;
  font-size: 0.9rem;
}
</style>
"""
with open(os.path.join(src_dir, 'App.vue'), 'w', encoding='utf-8') as f:
    f.write(app_vue)
print("✅ 创建 src/App.vue")
# 创建 style.css
style_css = """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
#app {
  width: 100%;
}
"""
with open(os.path.join(src_dir, 'style.css'), 'w', encoding='utf-8') as f:
    f.write(style_css)
print("✅ 创建 src/style.css")
# 创建 vite.config.js
vite_config = """import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
export default defineConfig({
  plugins: [vue()],
  base: '/xiyue-reader/'
})
"""
with open(os.path.join(base_dir, 'vite.config.js'), 'w', encoding='utf-8') as f:
    f.write(vite_config)
print("✅ 创建 vite.config.js")
print("\n🎉 前端项目结构重建完成！")
print(f"📁 目录结构：")
print(f"   {base_dir}/")
print(f"   ├─ index.html")
print(f"   ├─ vite.config.js")
print(f"   ├─ package.json")
print(f"   └─ src/")
print(f"      ├─ main.js")
print(f"      ├─ App.vue")
print(f"      └─ style.css")