import { createRouter, createWebHistory } from 'vue-router'
import WordList from '@/views/WordList.vue'
import WordDetail from '@/views/WordDetail.vue'
import Stats from '@/views/Stats.vue'
import DailyWord from '@/views/DailyWord.vue'
import BrowserHistory from '@/views/BrowserHistory.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'word-list',
      component: WordList,
    },
    {
      path: '/daily',
      name: 'daily-word',
      component: DailyWord,
    },
    {
      path: '/stats',
      name: 'stats',
      component: Stats,
    },
    {
      path: '/history',
      name: 'browser-history',
      component: BrowserHistory,
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
