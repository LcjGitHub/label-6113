<template>
  <el-card shadow="never">
    <template #header>
      <div class="card-header">
        <span>地区统计</span>
        <div class="total-badge">
          <span>全库总条数：</span>
          <el-tag type="primary" size="large">{{ total }}</el-tag>
          <el-button :icon="Refresh" @click="handleRefresh">刷新</el-button>
        </div>
      </div>
    </template>

    <el-table
      v-loading="loading"
      :data="stats"
      stripe
      style="width: 100%"
      empty-text="暂无统计数据"
    >
      <el-table-column type="index" label="序号" width="80" align="center" />
      <el-table-column prop="region" label="地区" />
      <el-table-column prop="count" label="词条数量" sortable>
        <template #default="{ row }">
          <el-tag :type="getTagType(row.count)">{{ row.count }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { fetchRegionStats } from '@/api/stats'
import type { RegionStat } from '@/types/word'

const loading = ref(false)
const total = ref(0)
const stats = ref<RegionStat[]>([])

async function loadStats() {
  loading.value = true
  try {
    const data = await fetchRegionStats()
    total.value = data.total
    stats.value = data.regions
  } catch {
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

function handleRefresh() {
  loadStats()
}

function getTagType(count: number): 'success' | 'warning' | 'info' | 'primary' {
  if (count >= 50) return 'success'
  if (count >= 20) return 'warning'
  return 'info'
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.total-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.total-badge :deep(.el-tag) {
  font-size: 16px;
  padding: 0 16px;
  height: 32px;
  line-height: 30px;
}
</style>
