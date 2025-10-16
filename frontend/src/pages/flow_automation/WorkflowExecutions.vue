<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <div class="flex items-center space-x-2">
        <button
          @click="navigateBack"
          class="p-1 rounded-full hover:bg-gray-200"
          title="Back to workflows"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <h2 class="text-2xl font-semibold text-gray-800">
          Workflow Executions: {{ workflowName }}
        </h2>
      </div>
      <Button
        class="bg-blue-600 hover:bg-blue-700 text-white"
        @click="runWorkflow"
      >
        Run Now
      </Button>
    </div>

    <div v-if="loading" class="p-4 bg-white rounded-lg shadow text-center">
      <p>Loading executions...</p>
    </div>
    <div v-else-if="!executions.length" class="p-8 bg-white rounded-lg shadow text-center">
      <h3 class="text-lg font-medium text-gray-700 mb-2">No executions yet</h3>
      <p class="text-gray-500 mb-4">Run the workflow to see executions here</p>
      <Button
        class="bg-blue-600 hover:bg-blue-700 text-white"
        @click="runWorkflow"
      >
        Run Workflow
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
              Execution ID
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Status
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Started
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Duration
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Triggered By
            </th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">Actions</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="execution in executions"
            :key="execution.name"
            class="hover:bg-gray-50"
          >
            <td class="px-6 py-4 text-sm font-mono">
              {{ execution.execution_id }}
            </td>
            <td class="px-6 py-4">
              <span
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                :class="getStatusClass(execution.status)"
              >
                {{ execution.status }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              {{ formatDate(execution.start_time) }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              {{ calculateDuration(execution.start_time, execution.end_time) }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              {{ execution.triggered_by }}
            </td>
            <td class="px-6 py-4 text-right text-sm font-medium">
              <button
                @click="viewExecutionDetails(execution)"
                class="text-blue-600 hover:text-blue-900"
              >
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiCall } from '../../utils/api'

export default {
  name: 'WorkflowExecutions',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const workflowId = ref(route.params.id)
    const workflowName = ref('')
    const executions = ref([])
    const loading = ref(true)

    const navigateBack = () => {
      router.push('/')
    }

    const fetchWorkflowDetails = async () => {
      try {
        const response = await apiCall(
          'spry.spry_automation.api.workflow.get_workflow',
          { name: workflowId.value }
        )

        if (response.message) {
          workflowName.value = response.message.workflow_name
        }
      } catch (error) {
        console.error('Error fetching workflow details:', error)
      }
    }

    const fetchExecutions = async () => {
      try {
        loading.value = true
        const response = await apiCall(
          'spry.spry_automation.api.workflow.get_workflow_executions',
          { workflow_name: workflowId.value }
        )
        executions.value = response.message || []
      } catch (error) {
        console.error('Error fetching executions:', error)
      } finally {
        loading.value = false
      }
    }

    const runWorkflow = async () => {
      try {
        const response = await apiCall(
          'spry.spry_automation.api.workflow.execute_workflow',
          { name: workflowId.value }
        )
        
        if (response.message && response.message.success) {
          alert('Workflow execution started')
          fetchExecutions() // Refresh the list
        } else {
          alert('Failed to execute workflow: ' + (response.message?.error || 'Unknown error'))
        }
      } catch (error) {
        console.error('Error executing workflow:', error)
        alert('Error executing workflow')
      }
    }

    const viewExecutionDetails = (execution) => {
      router.push({
        name: 'ExecutionDetail',
        params: { executionId: execution.execution_id }
      })
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

    onMounted(() => {
      fetchWorkflowDetails()
      fetchExecutions()
    })

    return {
      workflowId,
      workflowName,
      executions,
      loading,
      navigateBack,
      runWorkflow,
      viewExecutionDetails,
      getStatusClass,
      formatDate,
      calculateDuration
    }
  }
}
</script>
