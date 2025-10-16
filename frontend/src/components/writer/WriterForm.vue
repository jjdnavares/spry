<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Content Settings</h2>
    
    <div class="space-y-4">
      <!-- Keyword -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Keyword / Topic <span class="text-red-500">*</span>
        </label>
        <input
          type="text"
          :value="keyword"
          @input="$emit('update:keyword', $event.target.value)"
          placeholder="e.g., Artificial Intelligence"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Content Type -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Content Type
        </label>
        <select
          :value="contentType"
          @change="$emit('update:contentType', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="Article">Article</option>
          <option value="Blog Post">Blog Post</option>
          <option value="Product Description">Product Description</option>
          <option value="Social Media Post">Social Media Post</option>
          <option value="Email">Email</option>
          <option value="Landing Page">Landing Page</option>
        </select>
      </div>

      <!-- Tone -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Tone
        </label>
        <select
          :value="tone"
          @change="$emit('update:tone', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="professional">Professional</option>
          <option value="casual">Casual</option>
          <option value="friendly">Friendly</option>
          <option value="formal">Formal</option>
          <option value="humorous">Humorous</option>
          <option value="persuasive">Persuasive</option>
        </select>
      </div>

      <!-- Prompt -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Instructions <span class="text-red-500">*</span>
        </label>
        <textarea
          :value="prompt"
          @input="$emit('update:prompt', $event.target.value)"
          placeholder="Describe what you want to generate..."
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <!-- Generate Button -->
      <button
        @click="$emit('generate')"
        :disabled="generating"
        class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="generating">Generating...</span>
        <span v-else>Generate Content</span>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  keyword: String,
  contentType: String,
  tone: String,
  prompt: String,
  generating: Boolean
})

defineEmits(['update:keyword', 'update:contentType', 'update:tone', 'update:prompt', 'generate'])
</script>
