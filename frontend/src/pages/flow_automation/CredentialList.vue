<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Credentials</h2>
      <Button
        class="bg-blue-600 hover:bg-blue-700 text-white"
        @click="createCredential"
      >
        Add Credential
      </Button>
    </div>

    <div v-if="loading" class="p-4 bg-white rounded-lg shadow text-center">
      <p>Loading credentials...</p>
    </div>
    <div v-else-if="!credentials.length" class="p-8 bg-white rounded-lg shadow text-center">
      <h3 class="text-lg font-medium text-gray-700 mb-2">No credentials yet</h3>
      <p class="text-gray-500 mb-4">Add credentials to use in your workflows</p>
      <Button
        class="bg-blue-600 hover:bg-blue-700 text-white"
        @click="createCredential"
      >
        Add Credential
      </Button>
    </div>
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Name
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Type
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Last Modified
            </th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">Actions</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="credential in credentials"
            :key="credential.name"
            class="hover:bg-gray-50"
          >
            <td class="px-6 py-4 text-sm font-medium text-gray-900">
              {{ credential.credential_name }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              {{ credential.credential_type }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              {{ formatDate(credential.modified) }}
            </td>
            <td class="px-6 py-4 text-right text-sm font-medium">
              <div class="flex justify-end space-x-2">
                <button
                  @click="editCredential(credential)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  Edit
                </button>
                <button
                  @click="deleteCredential(credential)"
                  class="text-red-600 hover:text-red-900"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiCall } from '../../utils/api'

export default {
  name: 'CredentialList',
  setup() {
    const router = useRouter()
    const credentials = ref([])
    const loading = ref(true)

    const fetchCredentials = async () => {
      try {
        loading.value = true
        const response = await apiCall(
          'spry.spry_automation.api.credential.get_credential_list'
        )
        credentials.value = response.message || []
      } catch (error) {
        console.error('Error fetching credentials:', error)
      } finally {
        loading.value = false
      }
    }

    const createCredential = () => {
      router.push({
        name: 'CredentialEditor',
        params: { id: 'new' }
      })
    }

    const editCredential = (credential) => {
      router.push({
        name: 'CredentialEditor',
        params: { id: credential.name }
      })
    }

    const deleteCredential = async (credential) => {
      if (!confirm(`Are you sure you want to delete the credential "${credential.credential_name}"?`)) {
        return
      }
      
      try {
        const response = await apiCall(
          'spry.spry_automation.api.credential.delete_credential',
          { name: credential.name }
        )
        
        if (response.message && response.message.success) {
          fetchCredentials() // Refresh the list
        } else {
          alert('Failed to delete credential')
        }
      } catch (error) {
        console.error('Error deleting credential:', error)
        alert('Error deleting credential')
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString()
    }

    onMounted(() => {
      fetchCredentials()
    })

    return {
      credentials,
      loading,
      createCredential,
      editCredential,
      deleteCredential,
      formatDate
    }
  }
}
</script>
