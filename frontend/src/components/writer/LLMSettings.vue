<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">LLM Settings</h2>
    
    <div class="space-y-4">
      <!-- Provider Selection -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Provider
        </label>
        <select
          :value="provider"
          @change="$emit('update:provider', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option v-for="p in providers" :key="p.value" :value="p.value">
            {{ p.name }}
          </option>
        </select>
      </div>

      <!-- Model Selection -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Model
        </label>
        <select
          :value="model"
          @change="$emit('update:model', $event.target.value)"
          :disabled="loading"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
        >
          <option v-if="loading" value="">Loading models...</option>
          <option v-for="m in models" :key="m.value" :value="m.value">
            {{ m.name }}
          </option>
        </select>
      </div>

      <!-- API Key -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          API Key
        </label>
        <input
          type="password"
          :value="apiKey"
          @input="$emit('update:apiKey', $event.target.value)"
          placeholder="Enter your API key"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p class="text-xs text-gray-500 mt-1">
          Your API key is stored securely and only visible to you
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  provider: String,
  model: String,
  apiKey: String,
  providers: Array,
  models: Array,
  loading: Boolean
})

defineEmits(['update:provider', 'update:model', 'update:apiKey'])
</script>
