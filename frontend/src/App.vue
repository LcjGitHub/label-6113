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
          <el-button
            :icon="Clock"
            :type="isHistoryPage ? 'info' : 'default'"
            @click="router.push('/history')"
          >
            浏览历史
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
    <el-footer class="app-footer">
      <div class="footer-inner">
        <div class="status-item">
          <span class="status-dot" :class="isOnline ? 'dot-online' : 'dot-offline'"></span>
          <span class="status-text">{{ isOnline ? '服务在线' : '服务离线' }}</span>
        </div>
        <div v-if="healthInfo" class="status-detail">
          <span class="detail-item">词条总数: {{ healthInfo.total_words }}</span>
          <span class="detail-item">检查时间: {{ formatTime(healthInfo.current_time) }}</span>
        </div>
        <div v-if="healthInfo?.error" class="status-error">
          {{ healthInfo.error }}
        </div>
      </div>
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Clock, Star, DataLine, Plus } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchHealthCheck, type HealthCheckResponse } from '@/api/health'

const router = useRouter()
const route = useRoute()

const isDailyPage = computed(() => route.name === 'daily-word')
const isStatsPage = computed(() => route.name === 'stats')
const isHistoryPage = computed(() => route.name === 'browser-history')

const healthInfo = ref<HealthCheckResponse | null>(null)
const isOnline = computed(() => healthInfo.value?.status === 'online')

function formatTime(isoString: string): string {
  try {
    const date = new Date(isoString)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  } catch {
    return isoString
  }
}

async function loadHealthStatus() {
  healthInfo.value = await fetchHealthCheck()
}

onMounted(() => {
  loadHealthStatus()
})
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

.app-footer {
  background: #fff;
  border-top: 1px solid #ebeef5;
  height: auto;
  padding: 12px 0;
}

.footer-inner {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 13px;
  color: #606266;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.dot-online {
  background-color: #67c23a;
  box-shadow: 0 0 6px rgba(103, 194, 58, 0.5);
}

.dot-offline {
  background-color: #f56c6c;
  box-shadow: 0 0 6px rgba(245, 108, 108, 0.5);
}

.status-text {
  font-weight: 500;
}

.status-detail {
  display: flex;
  gap: 16px;
}

.detail-item {
  color: #909399;
}

.status-error {
  width: 100%;
  color: #f56c6c;
  font-size: 12px;
}
</style>
