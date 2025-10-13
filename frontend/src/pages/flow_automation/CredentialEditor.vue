<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <div class="flex items-center space-x-2">
        <button
          @click="navigateBack"
          class="p-1 rounded-full hover:bg-gray-200"
          title="Back to credentials"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <h2 class="text-2xl font-semibold text-gray-800">
          {{ isNewCredential ? 'Add Credential' : 'Edit Credential' }}
        </h2>
      </div>
      <div class="flex space-x-2">
        <Button
          class="bg-green-600 hover:bg-green-700 text-white"
          :disabled="!credentialName || !credentialType"
          @click="saveCredential"
        >
          Save
        </Button>
        <Button
          v-if="!isNewCredential"
          class="bg-blue-600 hover:bg-blue-700 text-white"
          @click="testCredential"
        >
          Test
        </Button>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6">
      <div class="grid grid-cols-1 gap-6">
        <div>
          <label for="credential_name" class="block text-sm font-medium text-gray-700">
            Credential Name
          </label>
          <input
            id="credential_name"
            v-model="credentialName"
            type="text"
            class="mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Enter credential name"
          />
        </div>

        <div>
          <label for="credential_type" class="block text-sm font-medium text-gray-700">
            Credential Type
          </label>
          <select
            id="credential_type"
            v-model="credentialType"
            class="mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            @change="onCredentialTypeChange"
          >
            <option value="">Select credential type</option>
            <option
              v-for="type in credentialTypes"
              :key="type.type"
              :value="type.type"
            >
              {{ type.name }}
            </option>
          </select>
        </div>

        <!-- Dynamic credential fields based on the selected type -->
        <div v-if="selectedCredentialType">
          <h3 class="text-lg font-medium text-gray-800 mb-4">
            {{ selectedCredentialType.name }} Details
          </h3>
          
          <div 
            v-for="field in selectedCredentialType.fields"
            :key="field.name"
            class="mb-4"
          >
            <label 
              :for="field.name" 
              class="block text-sm font-medium text-gray-700"
            >
              {{ field.name }} {{ field.required ? '*' : '' }}
            </label>
            <input
              v-if="field.type !== 'password'"
              :id="field.name"
              v-model="credentialData[field.name]"
              :type="field.type === 'password' ? 'password' : 'text'"
              class="mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              :placeholder="`Enter ${field.name}`"
              :required="field.required"
            />
            <input
              v-else
              :id="field.name"
              v-model="credentialData[field.name]"
              type="password"
              class="mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              :placeholder="`Enter ${field.name}`"
              :required="field.required"
              autocomplete="new-password"
            />
            <p v-if="field.description" class="mt-1 text-sm text-gray-500">
              {{ field.description }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'CredentialEditor',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const credentialId = ref(route.params.id)
    const isNewCredential = computed(() => credentialId.value === 'new')
    const credentialName = ref('')
    const credentialType = ref('')
    const credentialData = ref({})
    const credentialTypes = ref([])
    const loading = ref(true)

    const selectedCredentialType = computed(() => {
      if (!credentialType.value) return null
      return credentialTypes.value.find(type => type.type === credentialType.value)
    })

    const navigateBack = () => {
      router.push('/credentials')
    }

    const fetchCredentialTypes = async () => {
      try {
        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.credential.get_credential_types'
        })
        
        credentialTypes.value = response.message || []
      } catch (error) {
        console.error('Error fetching credential types:', error)
      }
    }

    const fetchCredential = async () => {
      if (isNewCredential.value) {
        credentialName.value = ''
        credentialType.value = ''
        credentialData.value = {}
        return
      }

      try {
        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.credential.get_credential',
          args: { name: credentialId.value }
        })

        if (response.message) {
          const credential = response.message
          credentialName.value = credential.credential_name
          credentialType.value = credential.credential_type
          // Note: credential data is not returned for security reasons
        }
      } catch (error) {
        console.error('Error fetching credential:', error)
        alert('Failed to load credential')
      }
    }

    const onCredentialTypeChange = () => {
      // Reset credential data when type changes
      credentialData.value = {}
      
      // Set default values for the selected type
      if (selectedCredentialType.value) {
        selectedCredentialType.value.fields.forEach(field => {
          if (field.default) {
            credentialData.value[field.name] = field.default
          }
        })
      }
    }

    const saveCredential = async () => {
      if (!credentialName.value) {
        alert('Please enter a credential name')
        return
      }
      
      if (!credentialType.value) {
        alert('Please select a credential type')
        return
      }
      
      // Validate required fields
      if (selectedCredentialType.value) {
        const missingFields = selectedCredentialType.value.fields
          .filter(field => field.required && !credentialData.value[field.name])
          .map(field => field.name)
          
        if (missingFields.length > 0) {
          alert(`Please fill in the following required fields: ${missingFields.join(', ')}`)
          return
        }
      }

      try {
        const data = {
          credential_name: credentialName.value,
          credential_type: credentialType.value,
          credential_data: credentialData.value
        }

        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.credential.save_credential',
          args: { data }
        })

        if (response.message) {
          alert('Credential saved successfully')
          
          if (isNewCredential.value) {
            // Navigate to the credential list
            router.push('/credentials')
          }
        }
      } catch (error) {
        console.error('Error saving credential:', error)
        alert('Failed to save credential')
      }
    }

    const testCredential = async () => {
      if (isNewCredential.value) {
        alert('Please save the credential first')
        return
      }

      try {
        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.credential.test_credential',
          args: { 
            name: credentialId.value
          }
        })
        
        if (response.message && response.message.success) {
          alert('Credential test successful')
        } else {
          alert('Credential test failed: ' + (response.message?.message || 'Unknown error'))
        }
      } catch (error) {
        console.error('Error testing credential:', error)
        alert('Error testing credential')
      }
    }

    onMounted(async () => {
      await fetchCredentialTypes()
      await fetchCredential()
      loading.value = false
    })

    return {
      credentialId,
      isNewCredential,
      credentialName,
      credentialType,
      credentialData,
      credentialTypes,
      selectedCredentialType,
      loading,
      navigateBack,
      onCredentialTypeChange,
      saveCredential,
      testCredential
    }
  }
}
</script>
