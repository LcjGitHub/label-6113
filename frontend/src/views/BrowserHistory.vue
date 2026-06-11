<template>
  <el-card shadow="never">
    <template #header>
      <div class="card-header">
        <span>浏览历史</span>
        <div class="header-actions">
          <el-button :icon="Refresh" @click="refreshTime">刷新时间</el-button>
          <el-button
            v-if="historyStore.history.length > 0"
            type="danger"
            :icon="Delete"
            @click="handleClearAll"
          >
            清空历史
          </el-button>
        </div>
      </div>
    </template>

    <el-empty v-if="historyStore.history.length === 0" description="暂无浏览记录" />

    <el-table
      v-else
      :data="historyStore.history"
      stripe
      style="width: 100%; cursor: pointer"
      @row-click="handleRowClick"
    >
      <el-table-column type="index" label="序号" width="70" />
      <el-table-column prop="id" label="词条编号" width="120" />
      <el-table-column prop="dialect_word" label="方言词" width="160" />
      <el-table-column label="访问时间" min-width="200">
        <template #default="{ row }">
          {{ formatTime(row.visited_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click.stop="goDetail(row.id)">查看详情</el-button>
          <el-button type="danger" link @click.stop="handleRemove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { Delete, Refresh } from '@element-plus/icons-vue'
import { useBrowserHistoryStore } from '@/stores/browserHistory'

const router = useRouter()
const historyStore = useBrowserHistoryStore()

const _tick = ref(0)

function refreshTime() {
  _tick.value++
}

function formatTime(ts: number) {
  void _tick.value
  const date = new Date(ts)
  const pad = (n: number) => n.toString().padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(
    date.getHours()
  )}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}

function goDetail(id: number) {
  router.push(`/words/${id}`)
}

function handleRowClick(row: { id: number }) {
  goDetail(row.id)
}

async function handleRemove(id: number) {
  try {
    await ElMessageBox.confirm('确定删除该条浏览记录吗？', '提示', { type: 'warning' })
    historyStore.removeHistory(id)
  } catch (error) {
    if (error !== 'cancel') {
      // ignore
    }
  }
}

async function handleClearAll() {
  try {
    await ElMessageBox.confirm('确定清空所有浏览历史吗？此操作不可恢复。', '提示', {
      type: 'warning',
    })
    historyStore.clearHistory()
  } catch (error) {
    if (error !== 'cancel') {
      // ignore
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-actions {
  display: flex;
  gap: 8px;
}
</style>
