<template>
  <el-card shadow="never" class="daily-card">
    <template #header>
      <div class="card-header">
        <div class="title-group">
          <span class="header-title">每日一词</span>
          <el-tag v-if="currentRegion" type="success" size="small" effect="light">
            地区: {{ currentRegion }}
          </el-tag>
          <el-tag v-else type="info" size="small" effect="light">
            全库随机
          </el-tag>
        </div>
        <el-button type="primary" :icon="RefreshRight" :loading="loading" @click="loadRandomWord">
          换一条
        </el-button>
      </div>
    </template>

    <div v-loading="loading" class="word-content">
      <template v-if="word">
        <div class="region-tag">
          <el-tag type="primary" size="large" effect="light">
            <Location />
            <span class="region-text">{{ word.region }}</span>
          </el-tag>
        </div>

        <div class="dialect-word">{{ word.dialect_word }}</div>

        <div class="divider">
          <el-divider>普通话释义</el-divider>
        </div>

        <div class="mandarin-word">{{ word.mandarin }}</div>

        <div v-if="word.pinyin" class="pinyin-word">{{ word.pinyin }}</div>

        <div class="example-section">
          <div class="example-label">
            <ChatLineRound />
            <span>例句</span>
          </div>
          <div v-if="word.example" class="example-text">「{{ word.example }}」</div>
          <div v-else class="example-empty">暂无例句</div>
        </div>

        <div class="word-id">
          <el-tag type="info" size="small">#{{ word.id }}</el-tag>
        </div>
      </template>

      <el-empty v-else-if="!loading && isEmpty" description="暂无词条数据" />
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { RefreshRight, Location, ChatLineRound } from '@element-plus/icons-vue'
import { fetchRandomWord } from '@/api/words'
import { useRegionStore } from '@/stores/region'
import type { DialectWord } from '@/types/word'

const regionStore = useRegionStore()

const loading = ref(false)
const word = ref<DialectWord | null>(null)
const isEmpty = ref(false)

const currentRegion = computed(() => regionStore.selectedRegion)

async function loadRandomWord() {
  loading.value = true
  isEmpty.value = false
  try {
    const region = currentRegion.value || undefined
    word.value = await fetchRandomWord(region)
  } catch (e: any) {
    const status = e?.response?.status
    if (status === 404) {
      word.value = null
      isEmpty.value = true
    } else {
      word.value = null
      isEmpty.value = true
      ElMessage.error('获取随机词条失败')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRandomWord()
})
</script>

<style scoped>
.daily-card {
  margin-top: 24px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.word-content {
  padding: 16px 10px;
  min-height: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.region-tag {
  margin-bottom: 16px;
}

.region-tag :deep(.el-tag) {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  padding: 0 16px;
  height: 32px;
  line-height: 30px;
  border-radius: 16px;
}

.region-text {
  font-weight: 500;
}

.dialect-word {
  font-size: 48px;
  font-weight: 700;
  color: #409eff;
  text-align: center;
  line-height: 1.2;
  letter-spacing: 4px;
  margin-bottom: 12px;
  text-shadow: 2px 2px 8px rgba(64, 158, 255, 0.15);
}

.divider {
  width: 80%;
  margin: 4px 0;
}

.divider :deep(.el-divider__text) {
  font-size: 14px;
  color: #909399;
  font-weight: 500;
}

.mandarin-word {
  font-size: 30px;
  font-weight: 500;
  color: #303133;
  text-align: center;
  line-height: 1.4;
  margin-bottom: 10px;
}

.pinyin-word {
  font-size: 20px;
  color: #909399;
  text-align: center;
  line-height: 1.4;
  margin-bottom: 16px;
  letter-spacing: 2px;
}

.example-section {
  width: 100%;
  max-width: 600px;
  background: #f5f7fa;
  border-radius: 12px;
  padding: 18px 24px;
  margin-bottom: 16px;
}

.example-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #67c23a;
  font-weight: 600;
  margin-bottom: 10px;
}

.example-text {
  font-size: 18px;
  color: #606266;
  line-height: 1.8;
  font-style: italic;
}

.example-empty {
  font-size: 16px;
  color: #c0c4cc;
  line-height: 1.8;
  font-style: italic;
}

.word-id {
  margin-top: auto;
}
</style>
