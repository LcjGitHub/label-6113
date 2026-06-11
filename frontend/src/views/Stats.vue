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

    <div class="chart-section">
      <div class="chart-title">地区词条数量分布</div>
      <div v-loading="loading" class="chart-container">
        <div v-if="!loading && stats.length === 0" class="empty-chart">
          <el-empty description="暂无数据" />
        </div>
        <div v-else ref="chartRef" class="chart"></div>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { fetchRegionStats } from '@/api/stats'
import type { RegionStat } from '@/types/word'

const loading = ref(false)
const total = ref(0)
const stats = ref<RegionStat[]>([])
const chartRef = ref<HTMLDivElement | null>(null)
let chartInstance: echarts.ECharts | null = null

function initChart() {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

function updateChart() {
  if (!chartInstance) return
  const regions = stats.value.map(item => item.region)
  const counts = stats.value.map(item => item.count)
  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: regions,
      axisLabel: {
        rotate: 0,
        interval: 0
      }
    },
    yAxis: {
      type: 'value',
      minInterval: 1
    },
    series: [
      {
        name: '词条数量',
        type: 'bar',
        data: counts,
        barMaxWidth: 60,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#409EFF' },
            { offset: 1, color: '#67C23A' }
          ]),
          borderRadius: [4, 4, 0, 0]
        },
        label: {
          show: true,
          position: 'top'
        }
      }
    ]
  }
  chartInstance.setOption(option)
}

function handleResize() {
  chartInstance?.resize()
}

async function loadStats() {
  loading.value = true
  try {
    const data = await fetchRegionStats()
    total.value = data.total
    stats.value = data.regions
    await nextTick()
    updateChart()
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

watch(stats, () => {
  if (!loading.value && chartInstance) {
    updateChart()
  }
})

onMounted(() => {
  loadStats()
  nextTick(() => {
    initChart()
    window.addEventListener('resize', handleResize)
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
  chartInstance = null
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

.chart-section {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 400px;
}

.chart {
  width: 100%;
  height: 100%;
}

.empty-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
</style>
