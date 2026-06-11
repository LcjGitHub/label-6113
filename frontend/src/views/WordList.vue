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
              v-for="item in regions"
              :key="item.region"
              :label="`${item.region}(${item.count})`"
              :value="item.region"
            />
          </el-select>
          <el-select
            v-model="selectedTag"
            placeholder="按标签筛选"
            clearable
            style="width: 160px"
            @change="handleTagChange"
          >
            <el-option
              v-for="tag in allTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
          <el-select
            v-model="sortField"
            placeholder="排序字段"
            style="width: 130px"
            @change="handleSortChange"
          >
            <el-option label="编号" value="id" />
            <el-option label="方言词" value="dialect_word" />
            <el-option label="地区" value="region" />
          </el-select>
          <el-button :icon="sortDirection === 'asc' ? SortUp : SortDown" @click="toggleSortDirection">
            {{ sortDirection === 'asc' ? '升序' : '降序' }}
          </el-button>
          <el-button :icon="Refresh" @click="loadWords">刷新</el-button>
          <el-button type="success" :icon="Download" @click="handleExport">导出</el-button>
          <el-button type="primary" :icon="Upload" @click="openImportDialog">导入</el-button>
          <el-button
            type="danger"
            :icon="Delete"
            :disabled="selectedIds.length === 0"
            @click="handleBatchDelete"
          >
            批量删除 ({{ selectedIds.length }})
          </el-button>
        </div>
      </div>
    </template>

    <el-table
      ref="tableRef"
      v-loading="loading"
      :data="words"
      stripe
      style="width: 100%; cursor: pointer"
      @selection-change="handleSelectionChange"
      @row-click="handleRowClick"
    >
      <el-table-column type="selection" width="50" />
      <el-table-column prop="dialect_word" label="方言词" width="110" />
      <el-table-column prop="mandarin" label="普通话" width="110" />
      <el-table-column prop="pinyin" label="拼音" width="140" show-overflow-tooltip />
      <el-table-column prop="region" label="地区" width="90" />
      <el-table-column prop="example" label="例句" show-overflow-tooltip />
      <el-table-column prop="source" label="来源" width="140" show-overflow-tooltip />
      <el-table-column label="标签" width="180">
        <template #default="{ row }">
          <template v-if="row.tags">
            <el-tag
              v-for="t in row.tags.split(',').map((s: string) => s.trim()).filter(Boolean)"
              :key="t"
              size="small"
              style="margin: 2px"
            >
              {{ t }}
            </el-tag>
          </template>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" width="160" show-overflow-tooltip />
      <el-table-column label="操作" width="140" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click.stop="goDetail(row.id)">编辑</el-button>
          <el-button type="danger" link @click.stop="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="importDialogVisible" title="批量导入词条" width="600px" @closed="handleImportDialogClosed">
      <el-alert
        type="info"
        :closable="false"
        style="margin-bottom: 16px"
      >
        <template #title>
          <span>请粘贴或输入 JSON 格式的词条数组，每个词条对象包含 dialect_word（方言词）、mandarin（普通话）、region（地区）三个必填字段，可选字段包括 pinyin（拼音）、example（例句）、source（来源）、remark（备注）。</span>
        </template>
      </el-alert>
      <el-input
        v-model="importJsonText"
        type="textarea"
        :rows="14"
        placeholder='例如：&#10;[&#10;  {&#10;    "dialect_word": "啥子",&#10;    "mandarin": "什么",&#10;    "region": "四川",&#10;    "pinyin": "shà zi",&#10;    "example": "你在搞啥子？",&#10;    "source": "日常用语",&#10;    "remark": "常用疑问词"&#10;  }&#10;]'
      />
      <div style="margin-top: 8px">
        <el-button @click="handleSelectFile">选择 JSON 文件</el-button>
        <input
          ref="fileInputRef"
          type="file"
          accept=".json,application/json"
          style="display: none"
          @change="handleFileChange"
        />
      </div>
      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="importing" @click="handleImportConfirm">确认导入</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Download, Refresh, Search, SortDown, SortUp, Upload } from '@element-plus/icons-vue'
import { batchDeleteWords, batchImportWords, deleteWord, exportWords, fetchRegions, fetchTags, fetchWords } from '@/api/words'
import { useRegionStore } from '@/stores/region'
import type { DialectWord, Region, WordForm } from '@/types/word'

const router = useRouter()
const regionStore = useRegionStore()

const tableRef = ref<any>()
const loading = ref(false)
const words = ref<DialectWord[]>([])
const regions = ref<Region[]>([])
const keyword = ref('')
const selectedTag = ref('')
const allTags = ref<string[]>([])
const selectedIds = ref<number[]>([])
const sortField = ref('id')
const sortDirection = ref<'asc' | 'desc'>('asc')

const importDialogVisible = ref(false)
const importJsonText = ref('')
const importing = ref(false)
const fileInputRef = ref<HTMLInputElement | null>(null)

async function loadWords() {
  loading.value = true
  try {
    const region = regionStore.selectedRegion || undefined
    const kw = keyword.value.trim() || undefined
    const tag = selectedTag.value || undefined
    const sf = sortField.value || undefined
    const sd = sortDirection.value || undefined
    words.value = await fetchWords(region, kw, tag, sf, sd)
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

function handleTagChange() {
  loadWords()
}

function handleSortChange() {
  loadWords()
}

function toggleSortDirection() {
  sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  loadWords()
}

async function loadTags() {
  try {
    allTags.value = await fetchTags()
  } catch {
    // silent
  }
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

function clearSelection() {
  tableRef.value?.clearSelection()
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

function handleSelectionChange(selection: DialectWord[]) {
  selectedIds.value = selection.map((item) => item.id)
}

function handleRowClick(row: DialectWord, column: any) {
  if (column.type === 'selection' || column.label === '操作') return
  goDetail(row.id)
}

async function handleBatchDelete() {
  try {
    await ElMessageBox.confirm(
      `确定删除选中的 ${selectedIds.value.length} 条词条吗？`,
      '提示',
      { type: 'warning' }
    )
    const result = await batchDeleteWords(selectedIds.value)
    ElMessage.success(`成功删除 ${result.deleted_count} 条词条`)
    clearSelection()
    await loadWords()
    await loadRegions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
      clearSelection()
    }
  }
}

async function handleExport() {
  try {
    const region = regionStore.selectedRegion || undefined
    const kw = keyword.value.trim() || undefined
    await exportWords(region, kw)
    ElMessage.success('导出成功')
  } catch {
    ElMessage.error('导出失败')
  }
}

function openImportDialog() {
  importJsonText.value = ''
  importDialogVisible.value = true
}

function handleImportDialogClosed() {
  importJsonText.value = ''
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}

function handleSelectFile() {
  fileInputRef.value?.click()
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    const content = e.target?.result as string
    importJsonText.value = content
  }
  reader.onerror = () => {
    ElMessage.error('读取文件失败')
  }
  reader.readAsText(file)
}

async function handleImportConfirm() {
  const text = importJsonText.value.trim()
  if (!text) {
    ElMessage.warning('请输入或粘贴 JSON 数据')
    return
  }

  let items: WordForm[]
  try {
    const parsed = JSON.parse(text)
    if (!Array.isArray(parsed)) {
      ElMessage.error('JSON 数据必须是数组格式')
      return
    }
    items = parsed as WordForm[]
  } catch {
    ElMessage.error('JSON 格式不正确，请检查语法')
    return
  }

  if (items.length === 0) {
    ElMessage.warning('没有可导入的词条数据')
    return
  }

  importing.value = true
  try {
    const result = await batchImportWords(items)
    let message = `导入完成：成功 ${result.success_count} 条，失败 ${result.fail_count} 条`
    if (result.fail_count > 0) {
      const detailList = result.failed_items
        .slice(0, 5)
        .map((item) => `第 ${item.index + 1} 条: ${item.error}`)
        .join('\n')
      const extra = result.failed_items.length > 5 ? `\n...还有 ${result.failed_items.length - 5} 条错误` : ''
      message += `\n\n失败详情：\n${detailList}${extra}`
      ElMessageBox.alert(message, '导入结果', { type: 'warning', dangerouslyUseHTMLString: false })
    } else {
      ElMessage.success(message)
    }
    importDialogVisible.value = false
    await loadWords()
    await loadRegions()
  } catch (error: any) {
    const msg = error?.response?.data?.error || '导入失败'
    ElMessage.error(msg)
  } finally {
    importing.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadWords(), loadRegions(), loadTags()])
})

watch(
  () => regionStore.selectedRegion,
  () => {
    loadWords()
  }
)
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


</style>
