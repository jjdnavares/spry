<template>
  <div class="min-h-screen bg-gray-50 p-4 sm:p-8">
    <div class="max-w-7xl mx-auto">
      <header class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Content Writer</h1>
        <p class="text-gray-600 mt-2">Generate AI-powered content with ease</p>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Settings Panel -->
        <div class="lg:col-span-1 space-y-6">
          <LLMSettings
            v-model:provider="selectedProvider"
            v-model:model="selectedModel"
            v-model:apiKey="apiKey"
            :providers="providers"
            :models="models"
            :loading="loadingModels"
            @update:provider="handleProviderChange"
          />
          
          <WriterForm
            v-model:keyword="keyword"
            v-model:contentType="contentType"
            v-model:tone="tone"
            v-model:prompt="prompt"
            :generating="generating"
            @generate="handleGenerate"
          />
        </div>

        <!-- Content Display -->
        <div class="lg:col-span-2">
          <ContentDisplay
            :content="generatedContent"
            :loading="generating"
            :error="error"
            @delete="handleDelete"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { call } from 'frappe-ui'
import LLMSettings from '../../components/writer/LLMSettings.vue'
import WriterForm from '../../components/writer/WriterForm.vue'
import ContentDisplay from '../../components/writer/ContentDisplay.vue'

const selectedProvider = ref('openai')
const selectedModel = ref('gpt-4o')
const apiKey = ref('')
const providers = ref([])
const models = ref([])
const loadingModels = ref(false)

const keyword = ref('')
const contentType = ref('Article')
const tone = ref('professional')
const prompt = ref('')

const generatedContent = ref(null)
const generating = ref(false)
const error = ref(null)

onMounted(async () => {
  await loadProviders()
  await loadModels()
  await loadApiKey()
})

watch(selectedProvider, async () => {
  await loadModels()
  await loadApiKey()
})

async function loadProviders() {
  try {
    const response = await call('spry.writer.api.llm.get_llm_providers')
    providers.value = response
    if (response.length > 0 && !selectedProvider.value) {
      selectedProvider.value = response[0].value
    }
  } catch (err) {
    console.error('Failed to load providers:', err)
  }
}

async function loadModels() {
  if (!selectedProvider.value) return
  
  loadingModels.value = true
  try {
    const response = await call('spry.writer.api.llm.get_llm_models', {
      provider: selectedProvider.value
    })
    models.value = response
    if (response.length > 0 && !selectedModel.value) {
      selectedModel.value = response[0].value
    }
  } catch (err) {
    console.error('Failed to load models:', err)
  } finally {
    loadingModels.value = false
  }
}

async function loadApiKey() {
  if (!selectedProvider.value) return
  
  try {
    const response = await call('spry.writer.api.llm.get_llm_api_key', {
      provider: selectedProvider.value
    })
    apiKey.value = response.api_key || ''
  } catch (err) {
    console.error('Failed to load API key:', err)
  }
}

async function handleProviderChange() {
  selectedModel.value = ''
  await loadModels()
  await loadApiKey()
}

async function handleGenerate() {
  if (!keyword.value || !prompt.value) {
    error.value = 'Please fill in all required fields'
    return
  }

  if (!apiKey.value) {
    error.value = 'Please configure your API key first'
    return
  }

  generating.value = true
  error.value = null

  try {
    // Save API key if changed
    await call('spry.writer.api.llm.set_llm_api_key', {
      provider: selectedProvider.value,
      api_key: apiKey.value
    })

    // Generate content
    const response = await call('spry.writer.api.content.generate_content', {
      keyword: keyword.value,
      content_type: contentType.value,
      tone: tone.value,
      prompt: prompt.value,
      provider: selectedProvider.value,
      model: selectedModel.value
    })

    generatedContent.value = response
  } catch (err) {
    console.error('Generation failed:', err)
    error.value = err.message || 'Failed to generate content'
  } finally {
    generating.value = false
  }
}

async function handleDelete(name) {
  try {
    await call('spry.writer.api.content.delete_content', { name })
    if (generatedContent.value?.name === name) {
      generatedContent.value = null
    }
  } catch (err) {
    console.error('Delete failed:', err)
    error.value = 'Failed to delete content'
  }
}
</script>
