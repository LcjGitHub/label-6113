import { createRouter, createWebHistory } from 'vue-router'
import WordList from '@/views/WordList.vue'
import WordDetail from '@/views/WordDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'word-list',
      component: WordList,
    },
    {
      path: '/words/new',
      name: 'word-create',
      component: WordDetail,
    },
    {
      path: '/words/:id',
      name: 'word-detail',
      component: WordDetail,
      props: true,
    },
  ],
})

export default router
