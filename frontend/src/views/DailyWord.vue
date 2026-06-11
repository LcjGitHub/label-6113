<template>
  <el-card shadow="never" class="daily-card">
    <template #header>
      <div class="card-header">
        <span class="header-title">每日一词</span>
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

        <div v-if="word.example" class="example-section">
          <div class="example-label">
            <ChatLineRound />
            <span>例句</span>
          </div>
          <div class="example-text">「{{ word.example }}」</div>
        </div>

        <div class="word-id">
          <el-tag type="info" size="small">#{{ word.id }}</el-tag>
        </div>
      </template>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { RefreshRight, Location, ChatLineRound } from '@element-plus/icons-vue'
import { fetchRandomWord } from '@/api/words'
import type { DialectWord } from '@/types/word'

const loading = ref(false)
const word = ref<DialectWord | null>(null)

async function loadRandomWord() {
  loading.value = true
  try {
    word.value = await fetchRandomWord()
  } catch {
    ElMessage.error('获取随机词条失败')
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

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.word-content {
  padding: 20px 10px;
  min-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.region-tag {
  margin-bottom: 32px;
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
  font-size: 72px;
  font-weight: 700;
  color: #409eff;
  text-align: center;
  line-height: 1.2;
  letter-spacing: 4px;
  margin-bottom: 24px;
  text-shadow: 2px 2px 8px rgba(64, 158, 255, 0.15);
}

.divider {
  width: 80%;
  margin: 8px 0;
}

.divider :deep(.el-divider__text) {
  font-size: 14px;
  color: #909399;
  font-weight: 500;
}

.mandarin-word {
  font-size: 36px;
  font-weight: 500;
  color: #303133;
  text-align: center;
  line-height: 1.4;
  margin-bottom: 40px;
}

.example-section {
  width: 100%;
  max-width: 600px;
  background: #f5f7fa;
  border-radius: 12px;
  padding: 24px 28px;
  margin-bottom: 32px;
}

.example-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #67c23a;
  font-weight: 600;
  margin-bottom: 12px;
}

.example-text {
  font-size: 20px;
  color: #606266;
  line-height: 1.8;
  font-style: italic;
}

.word-id {
  margin-top: auto;
}
</style>
