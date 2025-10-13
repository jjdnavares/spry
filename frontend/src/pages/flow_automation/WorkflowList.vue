<template>
  <div class="space-y-6">
    <!-- Header with Stats -->
    <div class="flex justify-between items-start">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Overview</h1>
        <p class="mt-1 text-sm text-gray-500">
          All the workflows, credentials and data tables you have access to
        </p>
      </div>
      <Button
        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg shadow-sm font-medium"
        @click="createWorkflow"
      >
        Create Workflow
      </Button>
    </div>

    <!-- Statistics Cards -->
    <div v-if="!loading && workflows.length > 0" class="grid grid-cols-1 md:grid-cols-5 gap-4">
      <div class="bg-white rounded-lg border border-gray-200 p-5">
        <div class="text-xs text-gray-500 mb-1">Prod. executions</div>
        <div class="text-sm text-gray-400 mb-2">Last 7 days</div>
        <div class="text-3xl font-semibold text-gray-900">{{ stats.prodExecutions }}</div>
      </div>
      <div class="bg-white rounded-lg border border-gray-200 p-5">
        <div class="text-xs text-gray-500 mb-1">Failed prod. executions</div>
        <div class="text-sm text-gray-400 mb-2">Last 7 days</div>
        <div class="text-3xl font-semibold text-gray-900">{{ stats.failedExecutions }}</div>
      </div>
      <div class="bg-white rounded-lg border border-gray-200 p-5">
        <div class="text-xs text-gray-500 mb-1">Failure rate</div>
        <div class="text-sm text-gray-400 mb-2">Last 7 days</div>
        <div class="text-3xl font-semibold text-gray-900">{{ stats.failureRate }}%</div>
      </div>
      <div class="bg-white rounded-lg border border-gray-200 p-5">
        <div class="text-xs text-gray-500 mb-1">Time saved</div>
        <div class="text-sm text-gray-400 mb-2">Last 7 days</div>
        <div class="text-3xl font-semibold text-gray-900">{{ stats.timeSaved }}</div>
      </div>
      <div class="bg-white rounded-lg border border-gray-200 p-5">
        <div class="text-xs text-gray-500 mb-1">Run time (avg.)</div>
        <div class="text-sm text-gray-400 mb-2">Last 7 days</div>
        <div class="text-3xl font-semibold text-gray-900">{{ stats.avgRunTime }}</div>
      </div>
    </div>

    <!-- Tabs and Content -->
    <div class="bg-white rounded-lg border border-gray-200">
      <!-- Tab Navigation -->
      <div class="border-b border-gray-200">
        <nav class="flex space-x-8 px-6" aria-label="Tabs">
          <button
            @click="activeTab = 'workflows'"
            :class="[
              activeTab === 'workflows'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
            ]"
          >
            Workflows
          </button>
          <button
            @click="activeTab = 'credentials'"
            :class="[
              activeTab === 'credentials'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
            ]"
          >
            Credentials
          </button>
          <button
            @click="activeTab = 'executions'"
            :class="[
              activeTab === 'executions'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
            ]"
          >
            Executions
          </button>
        </nav>
      </div>

      <!-- Tab Content -->
      <div class="p-6">
        <!-- Workflows Tab -->
        <div v-if="activeTab === 'workflows'">
          <!-- Search and Filter Bar -->
          <div v-if="!loading && workflows.length > 0" class="flex items-center justify-between mb-6">
            <div class="flex-1 max-w-lg">
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search workflows..."
                  class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>
            </div>
            <div class="flex items-center space-x-3 ml-4">
              <select
                v-model="sortBy"
                class="border border-gray-300 rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="modified">Sort by last updated</option>
                <option value="name">Sort by name</option>
                <option value="created">Sort by created</option>
              </select>
              <button class="p-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Workflows List -->
          <div v-if="loading" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p class="mt-2 text-sm text-gray-500">Loading workflows...</p>
          </div>
          <div v-else-if="!filteredWorkflows.length" class="text-center py-16">
            <!-- Welcome Message -->
            <div class="mb-8">
              <h2 class="text-2xl font-semibold text-gray-900 mb-2">
                👋 Welcome {{ userName }}!
              </h2>
              <p class="text-gray-600">Create your first workflow</p>
            </div>

            <!-- Action Cards -->
            <div class="flex items-center justify-center gap-6 max-w-2xl mx-auto">
              <!-- Start from scratch card -->
              <button
                @click="createWorkflow"
                class="group flex-1 max-w-xs bg-gray-50 hover:bg-gray-100 rounded-lg p-8 transition-all duration-200 cursor-pointer border-2 border-gray-200 hover:border-blue-300 hover:shadow-md"
              >
                <div class="flex flex-col items-center">
                  <div class="mb-4">
                    <svg class="h-16 w-16 text-gray-500 group-hover:text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900">Start from scratch</h3>
                </div>
              </button>

              <!-- Try a pre-built agent card -->
              <button
                @click="showTemplates"
                class="group flex-1 max-w-xs bg-gray-50 hover:bg-gray-100 rounded-lg p-8 transition-all duration-200 cursor-pointer border-2 border-gray-200 hover:border-blue-300 hover:shadow-md"
              >
                <div class="flex flex-col items-center">
                  <div class="mb-4">
                    <svg class="h-16 w-16 text-gray-500 group-hover:text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900">Try a pre-built agent</h3>
                </div>
              </button>
            </div>
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="workflow in filteredWorkflows"
              :key="workflow.name"
              class="group border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-sm transition-all cursor-pointer"
              @click="editWorkflow(workflow)"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center space-x-3">
                    <h3 class="text-base font-medium text-gray-900 truncate">
                      {{ workflow.workflow_name }}
                    </h3>
                    <span
                      class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                      :class="workflow.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                    >
                      {{ workflow.active ? 'Active' : 'Inactive' }}
                    </span>
                    <span class="inline-flex items-center text-xs text-gray-500">
                      <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Personal
                    </span>
                  </div>
                  <div class="mt-1 flex items-center text-sm text-gray-500">
                    <span>Last updated {{ formatRelativeTime(workflow.modified) }}</span>
                    <span class="mx-2">•</span>
                    <span>Created {{ formatRelativeTime(workflow.creation) }}</span>
                  </div>
                </div>
                <div class="flex items-center space-x-2 ml-4">
                  <button
                    @click.stop="runWorkflow(workflow)"
                    class="opacity-0 group-hover:opacity-100 p-2 text-green-600 hover:bg-green-50 rounded-lg transition-opacity"
                    title="Execute workflow"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </button>
                  <button
                    @click.stop="viewExecutions(workflow)"
                    class="opacity-0 group-hover:opacity-100 p-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-opacity"
                    title="View executions"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </button>
                  <button
                    @click.stop="openMenu(workflow)"
                    class="opacity-0 group-hover:opacity-100 p-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-opacity"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="filteredWorkflows.length > 0" class="mt-6 flex items-center justify-between">
            <div class="text-sm text-gray-500">
              Total {{ filteredWorkflows.length }}
            </div>
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-700">1</span>
              <span class="text-sm text-gray-500">50/page</span>
            </div>
          </div>
        </div>

        <!-- Credentials Tab -->
        <div v-if="activeTab === 'credentials'" class="text-center py-16">
          <p class="text-gray-500">Credentials view - Navigate to dedicated page</p>
          <Button
            class="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
            @click="$router.push('/credentials')"
          >
            Manage Credentials
          </Button>
        </div>

        <!-- Executions Tab -->
        <div v-if="activeTab === 'executions'" class="text-center py-16">
          <p class="text-gray-500">Recent executions across all workflows</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'WorkflowList',
  setup() {
    const router = useRouter()
    const workflows = ref([])
    const loading = ref(true)
    const activeTab = ref('workflows')
    const searchQuery = ref('')
    const sortBy = ref('modified')
    
    // Statistics
    const stats = ref({
      prodExecutions: 0,
      failedExecutions: 0,
      failureRate: 0,
      timeSaved: '0s',
      avgRunTime: '0s'
    })

    const userName = computed(() => {
      return window.frappe?.session?.user_fullname || 'there'
    })

    const filteredWorkflows = computed(() => {
      let filtered = workflows.value

      // Apply search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(w => 
          w.workflow_name.toLowerCase().includes(query) ||
          (w.description && w.description.toLowerCase().includes(query))
        )
      }

      // Apply sorting
      filtered = [...filtered].sort((a, b) => {
        if (sortBy.value === 'name') {
          return a.workflow_name.localeCompare(b.workflow_name)
        } else if (sortBy.value === 'created') {
          return new Date(b.creation) - new Date(a.creation)
        } else {
          // Default: sort by modified
          return new Date(b.modified) - new Date(a.modified)
        }
      })

      return filtered
    })

    const fetchWorkflows = async () => {
      try {
        loading.value = true
        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.workflow.get_workflow_list'
        })
        workflows.value = response.message || []
      } catch (error) {
        console.error('Error fetching workflows:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchStats = async () => {
      try {
        // TODO: Implement stats API endpoint
        // For now, using placeholder data
        stats.value = {
          prodExecutions: 0,
          failedExecutions: 0,
          failureRate: 0,
          timeSaved: '0s',
          avgRunTime: '0s'
        }
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }

    const createWorkflow = () => {
      router.push({
        name: 'WorkflowEditor',
        params: { id: 'new' }
      })
    }

    const editWorkflow = (workflow) => {
      router.push({
        name: 'WorkflowEditor',
        params: { id: workflow.name }
      })
    }

    const runWorkflow = async (workflow) => {
      try {
        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.workflow.execute_workflow',
          args: { name: workflow.name }
        })
        
        if (response.message && response.message.success) {
          alert('Workflow execution started')
        } else {
          alert('Failed to execute workflow: ' + (response.message?.error || 'Unknown error'))
        }
      } catch (error) {
        console.error('Error executing workflow:', error)
        alert('Error executing workflow')
      }
    }

    const viewExecutions = (workflow) => {
      router.push({
        name: 'WorkflowExecutions',
        params: { id: workflow.name }
      })
    }

    const openMenu = (workflow) => {
      // TODO: Implement context menu
      console.log('Open menu for', workflow.workflow_name)
    }

    const showTemplates = () => {
      // TODO: Implement templates/pre-built agents view
      alert('Templates feature coming soon!')
    }

    const formatRelativeTime = (dateString) => {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffSecs = Math.floor(diffMs / 1000)
      const diffMins = Math.floor(diffSecs / 60)
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)
      const diffWeeks = Math.floor(diffDays / 7)
      
      if (diffSecs < 60) return 'just now'
      if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`
      if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
      if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
      if (diffWeeks < 4) return `${diffWeeks} week${diffWeeks > 1 ? 's' : ''} ago`
      
      return date.toLocaleDateString()
    }

    onMounted(() => {
      fetchWorkflows()
      fetchStats()
    })

    return {
      workflows,
      loading,
      activeTab,
      searchQuery,
      sortBy,
      stats,
      userName,
      filteredWorkflows,
      createWorkflow,
      editWorkflow,
      runWorkflow,
      viewExecutions,
      openMenu,
      showTemplates,
      formatRelativeTime
    }
  }
}
</script>
