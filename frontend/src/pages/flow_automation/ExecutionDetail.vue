<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <div class="flex items-center space-x-2">
        <button
          @click="navigateBack"
          class="p-1 rounded-full hover:bg-gray-200"
          title="Back to executions"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <h2 class="text-2xl font-semibold text-gray-800">
          Execution Details
        </h2>
      </div>
      <div class="flex space-x-2">
        <Button
          v-if="execution && execution.status === 'running'"
          class="bg-red-600 hover:bg-red-700 text-white"
          @click="stopExecution"
        >
          Stop Execution
        </Button>
      </div>
    </div>

    <div v-if="loading" class="p-4 bg-white rounded-lg shadow text-center">
      <p>Loading execution details...</p>
    </div>
    <div v-else-if="!execution" class="p-8 bg-white rounded-lg shadow text-center">
      <h3 class="text-lg font-medium text-gray-700 mb-2">Execution not found</h3>
      <p class="text-gray-500 mb-4">The execution you're looking for doesn't exist or has been deleted</p>
      <Button
        class="bg-blue-600 hover:bg-blue-700 text-white"
        @click="navigateBack"
      >
        Back to Executions
      </Button>
    </div>
    <div v-else>
      <!-- Execution Summary -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <div class="grid grid-cols-2 gap-6">
          <div>
            <h3 class="text-sm font-medium text-gray-500">Execution ID</h3>
            <p class="mt-1 text-lg font-mono">{{ execution.execution_id }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500">Status</h3>
            <p class="mt-1">
              <span
                class="px-2 py-1 inline-flex text-sm leading-5 font-semibold rounded-full"
                :class="getStatusClass(execution.status)"
              >
                {{ execution.status }}
              </span>
            </p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500">Started</h3>
            <p class="mt-1">{{ formatDate(execution.start_time) }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500">Finished</h3>
            <p class="mt-1">{{ execution.end_time ? formatDate(execution.end_time) : 'Running...' }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500">Duration</h3>
            <p class="mt-1">{{ calculateDuration(execution.start_time, execution.end_time) }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500">Triggered By</h3>
            <p class="mt-1">{{ execution.triggered_by }}</p>
          </div>
        </div>
      </div>

      <!-- Error Message (if any) -->
      <div v-if="execution.error_message" class="bg-red-50 border border-red-200 rounded-lg shadow p-6 mb-6">
        <h3 class="text-lg font-medium text-red-800 mb-2">Error</h3>
        <pre class="whitespace-pre-wrap text-red-700 font-mono text-sm">{{ execution.error_message }}</pre>
      </div>

      <!-- Input Data -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h3 class="text-lg font-medium text-gray-800 mb-4">Input Data</h3>
        <pre v-if="execution.input_data" class="bg-gray-50 p-4 rounded border border-gray-200 overflow-auto max-h-60">{{ formatJson(execution.input_data) }}</pre>
        <p v-else class="text-gray-500">No input data</p>
      </div>

      <!-- Output Data -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium text-gray-800 mb-4">Output Data</h3>
        <pre v-if="execution.output_data" class="bg-gray-50 p-4 rounded border border-gray-200 overflow-auto max-h-60">{{ formatJson(execution.output_data) }}</pre>
        <p v-else class="text-gray-500">
          {{ execution.status === 'running' ? 'Execution is still running...' : 'No output data' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiCall } from '../../utils/api'

export default {
  name: 'ExecutionDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const executionId = ref(route.params.executionId)
    const execution = ref(null)
    const loading = ref(true)

    const navigateBack = () => {
      if (execution.value && execution.value.workflow) {
        router.push({
          name: 'WorkflowExecutions',
          params: { id: execution.value.workflow }
        })
      } else {
        router.push('/')
      }
    }

    const fetchExecution = async () => {
      try {
        loading.value = true
        const response = await apiCall(
          'spry.spry_automation.api.workflow.get_workflow_execution',
          { execution_id: executionId.value }
        )
        
        if (response.message) {
          execution.value = response.message
        }
      } catch (error) {
        console.error('Error fetching execution details:', error)
        execution.value = null
      } finally {
        loading.value = false
      }
    }

    const stopExecution = async () => {
      if (!execution.value || execution.value.status !== 'running') {
        return
      }
      
      if (!confirm('Are you sure you want to stop this workflow execution?')) {
        return
      }

      try {
        const response = await apiCall(
          'spry.spry_automation.api.workflow.stop_workflow_execution',
          { execution_id: executionId.value }
        )
        
        if (response.message && response.message.success) {
          alert('Execution stopped')
          fetchExecution() // Refresh the data
        } else {
          alert('Failed to stop execution')
        }
      } catch (error) {
        console.error('Error stopping execution:', error)
        alert('Error stopping execution')
      }
    }

    const getStatusClass = (status) => {
      switch (status) {
        case 'success':
          return 'bg-green-100 text-green-800'
        case 'error':
          return 'bg-red-100 text-red-800'
        case 'running':
          return 'bg-blue-100 text-blue-800'
        case 'waiting':
          return 'bg-yellow-100 text-yellow-800'
        case 'terminated':
          return 'bg-gray-100 text-gray-800'
        default:
          return 'bg-gray-100 text-gray-800'
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString()
    }

    const calculateDuration = (startTime, endTime) => {
      if (!startTime || !endTime) {
        return startTime && !endTime ? 'Running...' : 'N/A'
      }
      
      const start = new Date(startTime)
      const end = new Date(endTime)
      const durationMs = end - start
      
      if (durationMs < 1000) {
        return `${durationMs}ms`
      } else if (durationMs < 60000) {
        return `${Math.round(durationMs / 1000)}s`
      } else {
        const minutes = Math.floor(durationMs / 60000)
        const seconds = Math.round((durationMs % 60000) / 1000)
        return `${minutes}m ${seconds}s`
      }
    }

    const formatJson = (jsonString) => {
      if (!jsonString) return ''
      
      try {
        const obj = typeof jsonString === 'string' ? JSON.parse(jsonString) : jsonString
        return JSON.stringify(obj, null, 2)
      } catch (e) {
        return String(jsonString)
      }
    }

    onMounted(() => {
      fetchExecution()
    })

    return {
      executionId,
      execution,
      loading,
      navigateBack,
      stopExecution,
      getStatusClass,
      formatDate,
      calculateDuration,
      formatJson
    }
  }
}
</script>
