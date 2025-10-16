import { createApp } from 'vue'
import { FrappeUI, setConfig, frappeRequest } from 'frappe-ui'
import Writer from './pages/writer/Writer.vue'
import './index.css'

// Configure frappe-ui to use frappe's request handler
setConfig('resourceFetcher', frappeRequest)

const app = createApp(Writer)

app.use(FrappeUI)

// Add error handling
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err, info)
}

// Wait for DOM to be ready before mounting
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('Mounting Writer app...')
    app.mount('#app')
    console.log('Writer app mounted!')
  })
} else {
  console.log('Mounting Writer app...')
  app.mount('#app')
  console.log('Writer app mounted!')
}
