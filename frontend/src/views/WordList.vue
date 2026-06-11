<template>
  <el-card shadow="never">
    <template #header>
      <div class="card-header">
        <span>词汇列表</span>
        <div class="filters">
          <el-input
            v-model="keyword"
            placeholder="输入关键词搜索"
            clearable
            style="width: 220px"
            @keyup.enter="handleSearch"
            @clear="handleClear"
          />
          <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
          <el-select
            v-model="regionStore.selectedRegion"
            placeholder="按地区筛选"
            clearable
            style="width: 180px"
            @change="handleRegionChange"
          >
            <el-option
              v-for="region in regions"
              :key="region"
              :label="region"
              :value="region"
            />
          </el-select>
          <el-button :icon="Refresh" @click="loadWords">刷新</el-button>
        </div>
      </div>
    </template>

    <el-table
      v-loading="loading"
      :data="words"
      stripe
      style="width: 100%"
      @row-click="handleRowClick"
    >
      <el-table-column prop="dialect_word" label="方言词" width="120" />
      <el-table-column prop="mandarin" label="普通话" width="120" />
      <el-table-column prop="region" label="地区" width="100" />
      <el-table-column prop="example" label="例句" show-overflow-tooltip />
      <el-table-column prop="source" label="来源" width="160" show-overflow-tooltip />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click.stop="goDetail(row.id)">编辑</el-button>
          <el-button type="danger" link @click.stop="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Search } from '@element-plus/icons-vue'
import { deleteWord, fetchRegions, fetchWords, searchWords } from '@/api/words'
import { useRegionStore } from '@/stores/region'
import type { DialectWord, WordQueryParams } from '@/types/word'

const router = useRouter()
const regionStore = useRegionStore()

const loading = ref(false)
const words = ref<DialectWord[]>([])
const regions = ref<string[]>([])
const keyword = ref('')

async function loadWords() {
  loading.value = true
  try {
    const region = regionStore.selectedRegion || undefined
    if (keyword.value.trim()) {
      const params: WordQueryParams = { keyword: keyword.value.trim() }
      if (region) params.region = region
      words.value = await searchWords(params)
    } else {
      words.value = await fetchWords(region)
    }
  } catch {
    ElMessage.error('加载词汇列表失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  loadWords()
}

function handleClear() {
  keyword.value = ''
  loadWords()
}

function handleRegionChange() {
  loadWords()
}

async function loadRegions() {
  try {
    regions.value = await fetchRegions()
  } catch {
    ElMessage.error('加载地区列表失败')
  }
}

function goDetail(id: number) {
  router.push(`/words/${id}`)
}

function handleRowClick(row: DialectWord) {
  goDetail(row.id)
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定删除该词条吗？', '提示', { type: 'warning' })
    await deleteWord(id)
    ElMessage.success('删除成功')
    await loadWords()
    await loadRegions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(async () => {
  await Promise.all([loadWords(), loadRegions()])
})
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.filters {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-table__row) {
  cursor: pointer;
}
</style>
