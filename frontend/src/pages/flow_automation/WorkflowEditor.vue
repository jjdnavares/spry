<template>
  <div class="fixed inset-0 bg-gray-50 flex flex-col">
    <!-- Top Navigation Bar -->
    <header class="bg-white border-b border-gray-200 flex items-center justify-between px-6 py-3">
      <!-- Left: Back button and workflow info -->
      <div class="flex items-center space-x-4">
        <button
          @click="navigateBack"
          class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          title="Back to workflows"
        >
          <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <div class="flex items-center space-x-3">
          <div class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span class="text-sm text-gray-500">Personal</span>
          </div>
          
          <input
            v-model="workflowName"
            type="text"
            class="text-lg font-semibold text-gray-900 bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
            placeholder="My workflow"
            @blur="autoSave"
          />
          
          <button
            class="text-sm text-gray-500 hover:text-gray-700 px-2 py-1 hover:bg-gray-100 rounded"
          >
            + Add tag
          </button>
        </div>
      </div>

      <!-- Center: Tabs -->
      <nav class="flex space-x-1">
        <button
          @click="activeTab = 'editor'"
          :class="[
            activeTab === 'editor'
              ? 'bg-gray-100 text-gray-900'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors'
          ]"
        >
          Editor
        </button>
        <button
          @click="activeTab = 'executions'"
          :class="[
            activeTab === 'executions'
              ? 'bg-gray-100 text-gray-900'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors'
          ]"
        >
          Executions
        </button>
        <button
          @click="activeTab = 'settings'"
          :class="[
            activeTab === 'settings'
              ? 'bg-gray-100 text-gray-900'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors'
          ]"
        >
          Settings
        </button>
      </nav>

      <!-- Right: Actions -->
      <div class="flex items-center space-x-3">
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-500">{{ active ? 'Active' : 'Inactive' }}</span>
          <button
            @click="active = !active"
            :class="[
              active ? 'bg-green-500' : 'bg-gray-300',
              'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            ]"
          >
            <span
              :class="[
                active ? 'translate-x-5' : 'translate-x-0',
                'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out'
              ]"
            />
          </button>
        </div>
        
        <button
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Share
        </button>
        
        <button
          @click="saveWorkflow"
          :disabled="saving"
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ saving ? 'Saving...' : 'Save' }}
        </button>
        
        <button
          class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
          </svg>
        </button>
      </div>
    </header>

    <!-- Main Content Area -->
    <div class="flex-1 flex overflow-hidden">
      <!-- Canvas Area -->
      <div class="flex-1 relative overflow-hidden"
        style="background-color: #f9fafb; background-image: radial-gradient(circle, #d1d5db 1px, transparent 1px); background-size: 20px 20px;"
        @click="onCanvasClick"
        @mousemove="draggingNodeId ? onNodeDrag($event) : (draggingConnection ? onConnectionDrag($event) : null)"
        @mouseup="draggingNodeId ? stopDragging() : null"
      >
        <div
          v-if="activeTab === 'editor'"
          class="absolute inset-0"
        >
          <!-- Canvas Content -->
          <div class="absolute inset-0 flex items-center justify-center">
            <div
              v-if="canvasNodes.length === 0"
              class="text-center"
            >
              <button
                @click="addFirstNode"
                class="group"
              >
                <div class="w-32 h-32 border-2 border-dashed border-gray-400 rounded-lg flex items-center justify-center hover:border-blue-500 hover:bg-blue-50 transition-all">
                  <svg class="h-12 w-12 text-gray-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </div>
                <p class="mt-3 text-sm font-medium text-gray-600 group-hover:text-blue-600">Add first step...</p>
              </button>
            </div>
            
            <!-- Canvas with nodes and connections -->
            <div v-else class="absolute inset-0">
              <!-- SVG Layer for Connections -->
              <svg class="absolute inset-0 w-full h-full" style="z-index: 1;">
                <!-- Render connections -->
                <g v-for="connection in connections" :key="`${connection.from}-${connection.to}`">
                  <!-- Invisible wider path for easier clicking -->
                  <path
                    :d="getConnectionPath(connection)"
                    stroke="transparent"
                    stroke-width="20"
                    fill="none"
                    class="cursor-pointer"
                    @click.stop="selectConnection(connection)"
                  />
                  <!-- Visible connection path -->
                  <path
                    :d="getConnectionPath(connection)"
                    :stroke="selectedConnection && selectedConnection.from === connection.from && selectedConnection.to === connection.to ? '#EF4444' : '#3B82F6'"
                    :stroke-width="selectedConnection && selectedConnection.from === connection.from && selectedConnection.to === connection.to ? '3' : '2'"
                    fill="none"
                    class="connection-path pointer-events-none"
                  />
                </g>
                <!-- Temporary connection while dragging -->
                <path
                  v-if="draggingConnection"
                  :d="getTempConnectionPath()"
                  stroke="#93C5FD"
                  stroke-width="2"
                  fill="none"
                  stroke-dasharray="5,5"
                  class="pointer-events-none"
                />
              </svg>
              
              <!-- Nodes Layer -->
              <div class="absolute inset-0 p-8" style="z-index: 2;">
                <div
                  v-for="node in canvasNodes"
                  :key="node.id"
                  :ref="el => setNodeRef(node.id, el)"
                  class="absolute bg-white rounded-lg shadow-md border-2 border-gray-200 hover:border-blue-400 transition-all"
                  :class="{ 'border-blue-500': selectedNodeId === node.id }"
                  :style="{ left: node.x + 'px', top: node.y + 'px', width: '200px' }"
                  @mousedown="startDragging($event, node.id)"
                  @click="selectNode(node.id, $event)"
                >
                  <!-- Node Header -->
                  <div class="p-4 cursor-move">
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-sm font-medium text-gray-900">{{ node.name }}</span>
                      <button 
                        class="text-gray-400 hover:text-red-600 transition-colors" 
                        @click.stop="removeNode(node.id)"
                      >
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                    <p class="text-xs text-gray-500">{{ node.type }}</p>
                  </div>
                  
                  <!-- Connection Points -->
                  <div class="relative">
                    <!-- Input Connection Point (Left) -->
                    <div
                      v-if="canHaveInput(node)"
                      class="absolute left-0 top-1/2 transform -translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-blue-500 rounded-full border-2 border-white cursor-pointer hover:scale-125 transition-transform"
                      :class="{ 'ring-2 ring-blue-300': isValidConnectionTarget(node.id) }"
                      @mouseup.stop="endConnection(node.id)"
                      title="Input"
                    ></div>
                    
                    <!-- Output Connection Point (Right) -->
                    <div
                      class="absolute right-0 top-1/2 transform translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-green-500 rounded-full border-2 border-white cursor-pointer hover:scale-125 transition-transform"
                      @mousedown.stop="startConnection($event, node.id)"
                      title="Output"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Executions Tab Content -->
        <div
          v-if="activeTab === 'executions'"
          class="absolute inset-0 bg-white p-6 overflow-auto"
        >
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Workflow Executions</h3>
          <p class="text-gray-500">No executions yet. Run this workflow to see execution history.</p>
        </div>

        <!-- Settings Tab Content -->
        <div
          v-if="activeTab === 'settings'"
          class="absolute inset-0 bg-white p-6 overflow-auto"
        >
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Workflow Settings</h3>
          <div class="max-w-2xl space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                v-model="description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter workflow description"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Execution Settings
              </label>
              <div class="space-y-3">
                <div class="flex items-center">
                  <input
                    type="checkbox"
                    id="saveExecutionProgress"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label for="saveExecutionProgress" class="ml-2 text-sm text-gray-700">
                    Save execution progress
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    type="checkbox"
                    id="saveManualExecutions"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label for="saveManualExecutions" class="ml-2 text-sm text-gray-700">
                    Save manual executions
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Bottom Toolbar -->
        <div class="absolute bottom-4 left-4 flex items-center space-x-2 bg-white rounded-lg shadow-md border border-gray-200 p-2">
          <button
            @click="resetZoom"
            class="p-2 hover:bg-gray-100 rounded transition-colors"
            title="Reset zoom"
          >
            <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
            </svg>
          </button>
          <button
            @click="zoomOut"
            class="p-2 hover:bg-gray-100 rounded transition-colors"
            title="Zoom out"
          >
            <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7" />
            </svg>
          </button>
          <span class="text-sm text-gray-600 px-2">{{ zoomLevel }}%</span>
          <button
            @click="zoomIn"
            class="p-2 hover:bg-gray-100 rounded transition-colors"
            title="Zoom in"
          >
            <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
            </svg>
          </button>
          <button
            @click="fitToScreen"
            class="p-2 hover:bg-gray-100 rounded transition-colors"
            title="Fit to screen"
          >
            <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
            </svg>
          </button>
        </div>

        <!-- Delete Connection Button (appears when connection is selected) -->
        <div
          v-if="selectedConnection"
          class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white rounded-lg shadow-md border border-gray-200 p-2 flex items-center space-x-2"
        >
          <span class="text-sm text-gray-600 px-2">Connection selected</span>
          <button
            @click="deleteSelectedConnection"
            class="px-3 py-1.5 bg-red-50 text-red-600 hover:bg-red-100 rounded transition-colors text-sm font-medium"
            title="Delete connection"
          >
            Delete
          </button>
        </div>

        <!-- Toggle Sidebar Button -->
        <button
          v-if="!showRightSidebar"
          @click="showRightSidebar = true"
          class="absolute top-4 right-4 p-2 bg-white rounded-lg shadow-md border border-gray-200 hover:bg-gray-50 transition-colors"
          title="Show sidebar"
        >
          <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      <!-- Right Sidebar - Dynamic -->
      <div v-if="showRightSidebar" class="w-80 bg-white border-l border-gray-200 flex flex-col">
        <!-- Node Palette (when no node selected) -->
        <div v-if="!selectedNodeId" class="flex flex-col h-full">
          <!-- Sidebar Header -->
          <div class="p-4 border-b border-gray-200 flex items-center justify-between">
            <h3 class="text-sm font-semibold text-gray-900">{{ showTriggers ? 'What triggers this workflow?' : 'Add Node' }}</h3>
            <button
              @click="showRightSidebar = false"
              class="p-1 hover:bg-gray-100 rounded transition-colors"
              title="Hide sidebar"
            >
              <svg class="h-4 w-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Trigger Selection -->
          <div v-if="showTriggers" class="flex-1 overflow-auto p-4">
            <p class="text-xs text-gray-500 mb-4">A trigger is a step that starts your workflow</p>
            
            <!-- Search -->
            <div class="mb-4">
              <div class="relative">
                <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  v-model="triggerSearch"
                  type="text"
                  placeholder="Search nodes..."
                  class="w-full pl-10 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <!-- Trigger Options -->
            <div class="space-y-2">
              <button
                v-for="trigger in filteredTriggers"
                :key="trigger.type"
                @click="addTriggerNode(trigger)"
                class="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all group"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center group-hover:bg-blue-100">
                    <svg class="h-5 w-5 text-gray-600 group-hover:text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path v-if="trigger.type === 'manual'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                      <path v-if="trigger.type === 'manual'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      <path v-if="trigger.type === 'webhook'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                      <path v-if="trigger.type === 'schedule'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      <path v-if="trigger.type === 'app_event'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                      <path v-if="trigger.type === 'form_submission'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      <path v-if="trigger.type === 'workflow_call'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      <path v-if="trigger.type === 'chat_message'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="text-sm font-medium text-gray-900">{{ trigger.name }}</div>
                    <div class="text-xs text-gray-500">{{ trigger.description }}</div>
                  </div>
                </div>
              </button>
            </div>

            <button
              @click="showTriggers = false"
              class="mt-4 w-full text-sm text-blue-600 hover:text-blue-700 py-2"
            >
              ← Back to all nodes
            </button>
          </div>
          
          <!-- Node Palette -->
          <div v-else class="flex-1 overflow-auto p-4">
            <!-- Show trigger button if no trigger node exists -->
            <button
              v-if="!hasTriggerNode"
              @click="showTriggers = true"
              class="w-full mb-4 p-4 rounded-lg border-2 border-dashed border-blue-400 bg-blue-50 hover:bg-blue-100 transition-all text-left"
            >
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                  <svg class="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <div class="text-sm font-semibold text-blue-900">Add Trigger</div>
                  <div class="text-xs text-blue-700">Choose what starts this workflow</div>
                </div>
              </div>
            </button>

            <div class="space-y-2">
              <button
                v-for="nodeType in availableNodeTypes"
                :key="nodeType.type"
                @click="addNode(nodeType)"
                class="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all group"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center group-hover:bg-blue-100">
                    <svg class="h-5 w-5 text-gray-600 group-hover:text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="text-sm font-medium text-gray-900">{{ nodeType.name }}</div>
                    <div class="text-xs text-gray-500">{{ nodeType.description }}</div>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Node Configuration Panel (when node selected) -->
        <div v-else class="flex flex-col h-full">
          <!-- Panel Header -->
          <div class="p-4 border-b border-gray-200 flex items-center justify-between">
            <h3 class="text-sm font-semibold text-gray-900">{{ selectedNode?.name || 'Configure Node' }}</h3>
            <button
              @click="closeConfigPanel"
              class="p-1 hover:bg-gray-100 rounded transition-colors"
              title="Close"
            >
              <svg class="h-4 w-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Configuration Content -->
          <div class="flex-1 overflow-auto p-4">
            <div class="space-y-6">
              <!-- Node Name -->
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-2">
                  Node Name
                </label>
                <input
                  v-model="selectedNode.name"
                  type="text"
                  class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter node name"
                />
              </div>

              <!-- Node Type Display -->
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-2">
                  Type
                </label>
                <div class="px-3 py-2 text-sm bg-gray-50 border border-gray-200 rounded-lg text-gray-600">
                  {{ selectedNode.type }}
                </div>
              </div>

              <!-- HTTP Request Configuration -->
              <div v-if="selectedNode.type === 'http'">
                <h4 class="text-xs font-semibold text-gray-900 mb-3">HTTP Request Settings</h4>
                
                <div class="space-y-4">
                  <!-- Method -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-2">
                      Method
                    </label>
                    <select
                      v-model="selectedNode.config.method"
                      class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="GET">GET</option>
                      <option value="POST">POST</option>
                      <option value="PUT">PUT</option>
                      <option value="PATCH">PATCH</option>
                      <option value="DELETE">DELETE</option>
                    </select>
                  </div>

                  <!-- URL -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-2">
                      URL
                    </label>
                    <input
                      v-model="selectedNode.config.url"
                      type="text"
                      class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="https://api.example.com/endpoint"
                    />
                  </div>

                  <!-- Headers -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-2">
                      Headers (JSON)
                    </label>
                    <textarea
                      v-model="selectedNode.config.headers"
                      rows="3"
                      class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
                      placeholder='{"Content-Type": "application/json"}'
                    />
                  </div>

                  <!-- Body -->
                  <div v-if="['POST', 'PUT', 'PATCH'].includes(selectedNode.config.method)">
                    <label class="block text-xs font-medium text-gray-700 mb-2">
                      Body (JSON)
                    </label>
                    <textarea
                      v-model="selectedNode.config.body"
                      rows="4"
                      class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
                      placeholder='{"key": "value"}'
                    />
                  </div>
                </div>
              </div>

              <!-- Function Configuration -->
              <div v-if="selectedNode.type === 'function'">
                <h4 class="text-xs font-semibold text-gray-900 mb-3">Function Settings</h4>
                
                <div class="space-y-4">
                  <!-- Code -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-2">
                      JavaScript Code
                    </label>
                    <textarea
                      v-model="selectedNode.config.code"
                      rows="10"
                      class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
                      placeholder="// Write your code here&#10;return { result: 'value' };"
                    />
                  </div>
                </div>
              </div>

              <!-- Transform Configuration -->
              <div v-if="selectedNode.type === 'transform'">
                <h4 class="text-xs font-semibold text-gray-900 mb-3">Transform Settings</h4>
                
                <div class="space-y-4">
                  <!-- Transform Type -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-2">
                      Transform Type
                    </label>
                    <select
                      v-model="selectedNode.config.transformType"
                      class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="map">Map</option>
                      <option value="filter">Filter</option>
                      <option value="reduce">Reduce</option>
                      <option value="custom">Custom</option>
                    </select>
                  </div>

                  <!-- Expression -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-2">
                      Expression
                    </label>
                    <textarea
                      v-model="selectedNode.config.expression"
                      rows="4"
                      class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
                      placeholder="item => item.value > 10"
                    />
                  </div>
                </div>
              </div>

              <!-- Credential Selection -->
              <div v-if="nodeRequiresCredential(selectedNode.type)">
                <label class="block text-xs font-medium text-gray-700 mb-2">
                  Credential
                </label>
                <select
                  v-model="selectedNode.config.credentialId"
                  class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">No credential</option>
                  <option v-for="cred in availableCredentials" :key="cred.name" :value="cred.name">
                    {{ cred.credential_name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Panel Footer -->
          <div class="p-4 border-t border-gray-200 space-y-2">
            <button
              @click="testNode"
              :disabled="testing"
              class="w-full px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ testing ? 'Testing...' : 'Test Node' }}
            </button>
            <button
              @click="deleteSelectedNode"
              class="w-full px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors"
            >
              Delete Node
            </button>
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
  name: 'WorkflowEditor',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // Workflow properties
    const workflowId = ref(route.params.id)
    const isNewWorkflow = computed(() => workflowId.value === 'new')
    const workflowName = ref('')
    const description = ref('')
    const active = ref(false)
    const saving = ref(false)
    const activeTab = ref('editor')
    
    // Canvas
    const canvasNodes = ref([])
    const connections = ref([])
    const zoomLevel = ref(100)
    const selectedNodeId = ref(null)
    
    // Node dragging
    const draggingNodeId = ref(null)
    const dragOffset = ref({ x: 0, y: 0 })
    
    // Connection dragging
    const draggingConnection = ref(false)
    const connectionStart = ref(null)
    const connectionEnd = ref({ x: 0, y: 0 })
    
    // Connection selection
    const selectedConnection = ref(null)
    
    // Node refs for position calculation
    const nodeRefs = ref({})
    
    // Node types
    const availableNodeTypes = ref([
      { type: 'http', name: 'HTTP Request', description: 'Make HTTP requests' },
      { type: 'function', name: 'Function', description: 'Execute custom code' },
      { type: 'transform', name: 'Transform', description: 'Transform data' },
    ])

    // Configuration panel
    const testing = ref(false)
    const availableCredentials = ref([])
    const showRightSidebar = ref(true)
    const showTriggers = ref(false)
    const triggerSearch = ref('')
    
    // Computed property for selected node
    const selectedNode = computed(() => {
      if (!selectedNodeId.value) return null
      return canvasNodes.value.find(n => n.id === selectedNodeId.value)
    })

    // Check if workflow has a trigger node
    const hasTriggerNode = computed(() => {
      return canvasNodes.value.some(n => n.isTrigger === true)
    })

    // Trigger types
    const triggerTypes = ref([
      {
        type: 'manual',
        name: 'Trigger manually',
        description: 'Runs the flow on clicking a button in n8n. Good for getting started quickly',
        isTrigger: true
      },
      {
        type: 'webhook',
        name: 'On webhook call',
        description: 'Runs the flow on receiving an HTTP request',
        isTrigger: true
      },
      {
        type: 'schedule',
        name: 'On a schedule',
        description: 'Runs the flow every day, hour, or custom interval',
        isTrigger: true
      },
      {
        type: 'app_event',
        name: 'On app event',
        description: 'Runs the flow when something happens in an app like Telegram, Notion or Airtable',
        isTrigger: true
      },
      {
        type: 'form_submission',
        name: 'On form submission',
        description: 'Generate webforms in n8n and pass their responses to the workflow',
        isTrigger: true
      },
      {
        type: 'workflow_call',
        name: 'When executed by another workflow',
        description: 'Runs the flow when called by the Execute Workflow node from a different workflow',
        isTrigger: true
      },
      {
        type: 'chat_message',
        name: 'On chat message',
        description: 'Runs the flow when a user sends a chat message. For use with AI nodes',
        isTrigger: true
      }
    ])

    // Filtered triggers based on search
    const filteredTriggers = computed(() => {
      if (!triggerSearch.value) return triggerTypes.value
      
      const query = triggerSearch.value.toLowerCase()
      return triggerTypes.value.filter(t => 
        t.name.toLowerCase().includes(query) ||
        t.description.toLowerCase().includes(query)
      )
    })

    const navigateBack = () => {
      router.push('/')
    }

    const autoSave = () => {
      // TODO: Implement auto-save
      console.log('Auto-saving...')
    }

    const addFirstNode = () => {
      // Show trigger selector if no trigger exists
      if (!hasTriggerNode.value) {
        showTriggers.value = true
        showRightSidebar.value = true
      } else if (availableNodeTypes.value.length > 0) {
        addNode(availableNodeTypes.value[0])
      }
    }

    const addNode = (nodeType) => {
      const newNode = {
        id: Date.now().toString(),
        name: nodeType.name,
        type: nodeType.type,
        x: Math.random() * 400 + 200,
        y: Math.random() * 300 + 100,
        config: getDefaultConfig(nodeType.type),
        isTrigger: nodeType.isTrigger || false
      }
      canvasNodes.value.push(newNode)
    }

    const addTriggerNode = (trigger) => {
      const newNode = {
        id: Date.now().toString(),
        name: trigger.name,
        type: trigger.type,
        x: 300,
        y: 200,
        config: getTriggerDefaultConfig(trigger.type),
        isTrigger: true
      }
      canvasNodes.value.push(newNode)
      showTriggers.value = false
    }

    const getDefaultConfig = (nodeType) => {
      switch (nodeType) {
        case 'http':
          return {
            method: 'GET',
            url: '',
            headers: '{}',
            body: '{}',
            credentialId: ''
          }
        case 'function':
          return {
            code: '// Write your code here\nreturn { result: "value" };'
          }
        case 'transform':
          return {
            transformType: 'map',
            expression: 'item => item'
          }
        default:
          return {}
      }
    }

    const getTriggerDefaultConfig = (triggerType) => {
      switch (triggerType) {
        case 'manual':
          return {}
        case 'webhook':
          return {
            path: '/webhook',
            method: 'POST',
            responseMode: 'onReceived'
          }
        case 'schedule':
          return {
            interval: 'hours',
            value: 1
          }
        case 'app_event':
          return {
            app: '',
            event: ''
          }
        case 'form_submission':
          return {
            formId: ''
          }
        case 'workflow_call':
          return {}
        case 'chat_message':
          return {
            channel: ''
          }
        default:
          return {}
      }
    }

    const removeNode = (nodeId) => {
      // Remove node
      canvasNodes.value = canvasNodes.value.filter(n => n.id !== nodeId)
      // Remove associated connections
      connections.value = connections.value.filter(c => c.from !== nodeId && c.to !== nodeId)
      // Clear selection if this node was selected
      if (selectedNodeId.value === nodeId) {
        selectedNodeId.value = null
      }
    }

    const selectNode = (nodeId, event) => {
      if (event && event.stopPropagation) {
        event.stopPropagation() // Prevent canvas click from firing
      }
      selectedNodeId.value = nodeId
    }

    const onCanvasClick = () => {
      // Deselect node and connection when clicking on canvas
      selectedNodeId.value = null
      selectedConnection.value = null
    }

    const setNodeRef = (nodeId, el) => {
      if (el) {
        nodeRefs.value[nodeId] = el
      }
    }

    // Node dragging functions
    const startDragging = (event, nodeId) => {
      if (event.button !== 0) return // Only left click
      
      event.stopPropagation() // Prevent canvas click
      
      draggingNodeId.value = nodeId
      const node = canvasNodes.value.find(n => n.id === nodeId)
      if (node) {
        dragOffset.value = {
          x: event.clientX - node.x,
          y: event.clientY - node.y
        }
      }
      
      document.addEventListener('mousemove', onNodeDrag)
      document.addEventListener('mouseup', stopDragging)
    }

    const onNodeDrag = (event) => {
      if (!draggingNodeId.value) return
      
      const node = canvasNodes.value.find(n => n.id === draggingNodeId.value)
      if (node) {
        node.x = event.clientX - dragOffset.value.x
        node.y = event.clientY - dragOffset.value.y
      }
    }

    const stopDragging = () => {
      draggingNodeId.value = null
      document.removeEventListener('mousemove', onNodeDrag)
      document.removeEventListener('mouseup', stopDragging)
    }

    // Connection functions
    const startConnection = (event, nodeId) => {
      event.stopPropagation()
      draggingConnection.value = true
      connectionStart.value = nodeId
      connectionEnd.value = { x: event.clientX, y: event.clientY }
      
      document.addEventListener('mousemove', onConnectionDrag)
      document.addEventListener('mouseup', cancelConnection)
    }

    const onConnectionDrag = (event) => {
      connectionEnd.value = { x: event.clientX, y: event.clientY }
    }

    const endConnection = (targetNodeId) => {
      if (draggingConnection.value && connectionStart.value) {
        // Check if connection is valid
        if (connectionStart.value !== targetNodeId) {
          // Check if connection already exists
          const exists = connections.value.some(
            c => c.from === connectionStart.value && c.to === targetNodeId
          )
          
          if (!exists) {
            connections.value.push({
              from: connectionStart.value,
              to: targetNodeId
            })
          }
        }
      }
      
      cancelConnection()
    }

    const cancelConnection = () => {
      draggingConnection.value = false
      connectionStart.value = null
      document.removeEventListener('mousemove', onConnectionDrag)
      document.removeEventListener('mouseup', cancelConnection)
    }

    const canHaveInput = (node) => {
      // All nodes can have input except trigger nodes (to be implemented)
      return true
    }

    const isValidConnectionTarget = (nodeId) => {
      return draggingConnection.value && connectionStart.value !== nodeId
    }

    const getNodeCenter = (nodeId) => {
      const node = canvasNodes.value.find(n => n.id === nodeId)
      if (!node) return { x: 0, y: 0 }
      
      // Node dimensions
      const nodeWidth = 200
      const nodeHeight = 80 // Approximate height
      
      return {
        x: node.x + nodeWidth / 2,
        y: node.y + nodeHeight / 2
      }
    }

    const getConnectionPath = (connection) => {
      const fromNode = canvasNodes.value.find(n => n.id === connection.from)
      const toNode = canvasNodes.value.find(n => n.id === connection.to)
      
      if (!fromNode || !toNode) return ''
      
      // Calculate connection points
      const nodeWidth = 200
      const nodeHeight = 80
      
      const startX = fromNode.x + nodeWidth + 8 // Right side + padding
      const startY = fromNode.y + nodeHeight / 2
      const endX = toNode.x - 8 // Left side - padding
      const endY = toNode.y + nodeHeight / 2
      
      // Create Bezier curve
      const controlPointOffset = Math.abs(endX - startX) / 2
      const cp1x = startX + controlPointOffset
      const cp1y = startY
      const cp2x = endX - controlPointOffset
      const cp2y = endY
      
      return `M ${startX} ${startY} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${endX} ${endY}`
    }

    const getTempConnectionPath = () => {
      if (!connectionStart.value) return ''
      
      const fromNode = canvasNodes.value.find(n => n.id === connectionStart.value)
      if (!fromNode) return ''
      
      const nodeWidth = 200
      const nodeHeight = 80
      
      const startX = fromNode.x + nodeWidth + 8
      const startY = fromNode.y + nodeHeight / 2
      const endX = connectionEnd.value.x
      const endY = connectionEnd.value.y
      
      const controlPointOffset = Math.abs(endX - startX) / 2
      const cp1x = startX + controlPointOffset
      const cp1y = startY
      const cp2x = endX - controlPointOffset
      const cp2y = endY
      
      return `M ${startX} ${startY} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${endX} ${endY}`
    }

    // Connection selection and deletion
    const selectConnection = (connection) => {
      selectedConnection.value = connection
      selectedNodeId.value = null // Deselect any selected node
    }

    const deleteSelectedConnection = () => {
      if (!selectedConnection.value) return
      
      connections.value = connections.value.filter(c => 
        !(c.from === selectedConnection.value.from && c.to === selectedConnection.value.to)
      )
      selectedConnection.value = null
    }

    const saveWorkflow = async () => {
      if (!workflowName.value) {
        alert('Please enter a workflow name')
        return
      }

      try {
        saving.value = true
        const workflowData = {
          workflow_name: workflowName.value,
          description: description.value,
          active: active.value,
          nodes: JSON.stringify(canvasNodes.value),
          connections: JSON.stringify(connections.value)
        }

        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.workflow.save_workflow',
          args: { data: workflowData }
        })

        if (response.message) {
          alert('Workflow saved successfully')
          
          if (isNewWorkflow.value) {
            router.push({
              name: 'WorkflowEditor',
              params: { id: response.message.name }
            })
          }
        }
      } catch (error) {
        console.error('Error saving workflow:', error)
        alert('Failed to save workflow')
      } finally {
        saving.value = false
      }
    }

    const zoomIn = () => {
      zoomLevel.value = Math.min(200, zoomLevel.value + 10)
    }

    const zoomOut = () => {
      zoomLevel.value = Math.max(50, zoomLevel.value - 10)
    }

    const resetZoom = () => {
      zoomLevel.value = 100
    }

    const fitToScreen = () => {
      zoomLevel.value = 100
    }

    // Configuration panel functions
    const closeConfigPanel = () => {
      selectedNodeId.value = null
    }

    const nodeRequiresCredential = (nodeType) => {
      // HTTP nodes can use credentials for authentication
      return nodeType === 'http'
    }

    const testNode = async () => {
      if (!selectedNode.value) return
      
      try {
        testing.value = true
        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.node_types.test_node',
          args: {
            node_type: selectedNode.value.type,
            config: selectedNode.value.config
          }
        })
        
        if (response.message) {
          if (response.message.success) {
            alert('Node test successful!\n\nResult:\n' + JSON.stringify(response.message.result, null, 2))
          } else {
            alert('Node test failed:\n' + (response.message.error || 'Unknown error'))
          }
        }
      } catch (error) {
        console.error('Error testing node:', error)
        alert('Error testing node: ' + error.message)
      } finally {
        testing.value = false
      }
    }

    const deleteSelectedNode = () => {
      if (!selectedNodeId.value) return
      
      if (confirm('Are you sure you want to delete this node?')) {
        removeNode(selectedNodeId.value)
      }
    }

    const fetchCredentials = async () => {
      try {
        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.credential.get_credential_list'
        })
        availableCredentials.value = response.message || []
      } catch (error) {
        console.error('Error fetching credentials:', error)
      }
    }

    const fetchWorkflow = async () => {
      if (isNewWorkflow.value) {
        workflowName.value = 'My workflow'
        return
      }

      try {
        const response = await window.frappe.call({
          method: 'spry.flow_automation.api.workflow.get_workflow',
          args: { name: workflowId.value }
        })

        if (response.message) {
          const workflow = response.message
          workflowName.value = workflow.workflow_name
          description.value = workflow.description || ''
          active.value = workflow.active || false
          
          try {
            const nodes = typeof workflow.nodes === 'string'
              ? JSON.parse(workflow.nodes)
              : workflow.nodes || []
            canvasNodes.value = Array.isArray(nodes) ? nodes : []
            
            const conns = typeof workflow.connections === 'string'
              ? JSON.parse(workflow.connections)
              : workflow.connections || []
            connections.value = Array.isArray(conns) ? conns : []
          } catch (e) {
            console.error('Error parsing workflow data:', e)
            canvasNodes.value = []
            connections.value = []
          }
        }
      } catch (error) {
        console.error('Error fetching workflow:', error)
      }
    }

    // Keyboard shortcuts
    const handleKeyDown = (event) => {
      // Delete key - delete selected connection or node
      if (event.key === 'Delete' || event.key === 'Backspace') {
        if (selectedConnection.value) {
          event.preventDefault()
          deleteSelectedConnection()
        } else if (selectedNodeId.value) {
          event.preventDefault()
          if (confirm('Are you sure you want to delete this node?')) {
            removeNode(selectedNodeId.value)
          }
        }
      }
      // Escape key - deselect
      else if (event.key === 'Escape') {
        selectedNodeId.value = null
        selectedConnection.value = null
      }
    }

    onMounted(() => {
      fetchWorkflow()
      fetchCredentials()
      
      // Add keyboard event listener
      document.addEventListener('keydown', handleKeyDown)
    })

    // Cleanup on unmount
    const onUnmounted = () => {
      document.removeEventListener('keydown', handleKeyDown)
    }

    return {
      workflowName,
      description,
      active,
      saving,
      activeTab,
      canvasNodes,
      connections,
      zoomLevel,
      selectedNodeId,
      selectedNode,
      selectedConnection,
      draggingConnection,
      testing,
      showRightSidebar,
      showTriggers,
      triggerSearch,
      hasTriggerNode,
      filteredTriggers,
      availableNodeTypes,
      availableCredentials,
      navigateBack,
      autoSave,
      addFirstNode,
      addNode,
      addTriggerNode,
      removeNode,
      selectNode,
      selectConnection,
      deleteSelectedConnection,
      onCanvasClick,
      setNodeRef,
      startDragging,
      startConnection,
      endConnection,
      canHaveInput,
      isValidConnectionTarget,
      getConnectionPath,
      getTempConnectionPath,
      closeConfigPanel,
      nodeRequiresCredential,
      testNode,
      deleteSelectedNode,
      saveWorkflow,
      zoomIn,
      zoomOut,
      resetZoom,
      fitToScreen
    }
  }
}
</script>

<style scoped>
.connection-path {
  transition: stroke 0.2s ease;
}

.connection-path:hover {
  stroke: #2563EB;
  stroke-width: 3;
  cursor: pointer;
}
</style>
