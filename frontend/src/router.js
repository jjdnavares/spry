import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'FlowAutomation',
    component: () => import('@/pages/flow_automation/Index.vue'),
    children: [
      {
        path: '',
        name: 'WorkflowList',
        component: () => import('@/pages/flow_automation/WorkflowList.vue'),
      },
      {
        path: 'workflow/:id',
        name: 'WorkflowEditor',
        component: () => import('@/pages/flow_automation/WorkflowEditor.vue'),
      },
      {
        path: 'workflow/:id/executions',
        name: 'WorkflowExecutions',
        component: () => import('@/pages/flow_automation/WorkflowExecutions.vue'),
      },
      {
        path: 'execution/:executionId',
        name: 'ExecutionDetail',
        component: () => import('@/pages/flow_automation/ExecutionDetail.vue'),
      },
      {
        path: 'credentials',
        name: 'CredentialList',
        component: () => import('@/pages/flow_automation/CredentialList.vue'),
      },
      {
        path: 'credential/:id',
        name: 'CredentialEditor',
        component: () => import('@/pages/flow_automation/CredentialEditor.vue'),
      }
    ]
  },
]

let router = createRouter({
  history: createWebHistory('/flow-automation'),
  routes,
})

export default router
