<template>
  <el-container class="app-layout">
    <el-header class="app-header">
      <div class="header-inner">
        <h1 class="title" @click="router.push('/')">方言词汇库</h1>
        <div class="nav-actions">
          <el-button
            :icon="Star"
            :type="isDailyPage ? 'warning' : 'default'"
            @click="router.push('/daily')"
          >
            每日一词
          </el-button>
          <el-button
            :icon="DataLine"
            :type="isStatsPage ? 'success' : 'default'"
            @click="router.push('/stats')"
          >
            数据统计
          </el-button>
          <el-button type="primary" :icon="Plus" @click="router.push('/words/new')">
            新增词条
          </el-button>
        </div>
      </div>
    </el-header>
    <el-main class="app-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Star, DataLine, Plus } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isDailyPage = computed(() => route.name === 'daily-word')
const isStatsPage = computed(() => route.name === 'stats')
</script>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #f5f7fa;
}

.app-layout {
  min-height: 100vh;
}

.app-header {
  background: #fff;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
}

.header-inner {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-actions {
  display: flex;
  gap: 8px;
}

.title {
  margin: 0;
  font-size: 20px;
  cursor: pointer;
  color: #303133;
}

.app-main {
  max-width: 1100px;
  margin: 0 auto;
  width: 100%;
}
</style>
