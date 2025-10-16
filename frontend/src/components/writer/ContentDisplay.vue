<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-semibold text-gray-900">Generated Content</h2>
      <button
        v-if="content"
        @click="$emit('delete', content.name)"
        class="text-red-600 hover:text-red-700 text-sm font-medium"
      >
        Delete
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
      <p class="text-red-800">{{ error }}</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!content" class="text-center py-12">
      <svg
        class="mx-auto h-12 w-12 text-gray-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
        />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No content yet</h3>
      <p class="mt-1 text-sm text-gray-500">
        Fill in the form and click "Generate Content" to get started
      </p>
    </div>

    <!-- Content Display -->
    <div v-else class="space-y-4">
      <!-- Title -->
      <div>
        <h3 class="text-xl font-semibold text-gray-900">{{ content.title }}</h3>
        <div class="flex items-center gap-4 mt-2 text-sm text-gray-500">
          <span>{{ content.content_type }}</span>
          <span>•</span>
          <span>{{ content.provider }} / {{ content.model }}</span>
          <span>•</span>
          <span>{{ formatDate(content.creation) }}</span>
        </div>
      </div>

      <!-- Generated Text -->
      <div class="prose max-w-none">
        <div class="bg-gray-50 rounded-md p-4 border border-gray-200">
          <pre class="whitespace-pre-wrap font-sans text-gray-800">{{ content.generated_text }}</pre>
        </div>
      </div>

      <!-- Metadata -->
      <div class="border-t pt-4 space-y-2 text-sm">
        <div>
          <span class="font-medium text-gray-700">Keyword:</span>
          <span class="text-gray-600 ml-2">{{ content.keyword }}</span>
        </div>
        <div>
          <span class="font-medium text-gray-700">Tone:</span>
          <span class="text-gray-600 ml-2">{{ content.tone }}</span>
        </div>
        <div>
          <span class="font-medium text-gray-700">Prompt:</span>
          <p class="text-gray-600 mt-1">{{ content.prompt }}</p>
        </div>
      </div>

      <!-- Copy Button -->
      <div class="flex justify-end">
        <button
          @click="copyToClipboard"
          class="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors"
        >
          {{ copied ? 'Copied!' : 'Copy to Clipboard' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  content: Object,
  loading: Boolean,
  error: String
})

defineEmits(['delete'])

const copied = ref(false)

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function copyToClipboard() {
  if (!props.content?.generated_text) return
  
  try {
    await navigator.clipboard.writeText(props.content.generated_text)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>
