<template>
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
      return txtContent.value.replace(/\n/g, '<br>')
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
