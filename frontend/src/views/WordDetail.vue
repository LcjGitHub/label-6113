<template>
  <el-card shadow="never">
    <template #header>
      <div class="card-header">
        <span>{{ isCreate ? '新增词条' : '词条详情 / 编辑' }}</span>
        <el-button :icon="Back" @click="router.push('/')">返回列表</el-button>
      </div>
    </template>

    <el-form
      ref="formRef"
      v-loading="loading"
      :model="form"
      :rules="rules"
      label-width="90px"
      style="max-width: 640px"
    >
      <el-form-item label="方言词" prop="dialect_word">
        <el-input v-model="form.dialect_word" placeholder="请输入方言词" />
      </el-form-item>
      <el-form-item label="普通话" prop="mandarin">
        <el-input v-model="form.mandarin" placeholder="请输入对应普通话" />
      </el-form-item>
      <el-form-item label="地区" prop="region">
        <el-input v-model="form.region" placeholder="如：四川、广东" />
      </el-form-item>
      <el-form-item label="例句" prop="example">
        <el-input
          v-model="form.example"
          type="textarea"
          :rows="3"
          placeholder="请输入例句"
        />
      </el-form-item>
      <el-form-item label="来源" prop="source">
        <el-input v-model="form.source" placeholder="请输入来源" />
      </el-form-item>
      <el-form-item label="备注" prop="remark">
        <el-input
          v-model="form.remark"
          type="textarea"
          :rows="3"
          placeholder="请输入备注说明"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="saving" @click="handleSubmit">
          {{ isCreate ? '创建' : '保存' }}
        </el-button>
        <el-button v-if="!isCreate" type="danger" :loading="deleting" @click="handleDelete">
          删除
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Back } from '@element-plus/icons-vue'
import { createWord, deleteWord, fetchWord, updateWord } from '@/api/words'
import type { WordForm } from '@/types/word'

const props = defineProps<{
  id?: string
}>()

const route = useRoute()
const router = useRouter()

const formRef = ref<FormInstance>()
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)

const form = reactive<WordForm>({
  dialect_word: '',
  mandarin: '',
  region: '',
  example: '',
  source: '',
  remark: '',
})

const rules: FormRules<WordForm> = {
  dialect_word: [{ required: true, message: '请输入方言词', trigger: 'blur' }],
  mandarin: [{ required: true, message: '请输入普通话', trigger: 'blur' }],
  region: [{ required: true, message: '请输入地区', trigger: 'blur' }],
}

const isCreate = computed(() => route.name === 'word-create')

async function loadWord() {
  if (isCreate.value || !props.id) {
    return
  }

  loading.value = true
  try {
    const word = await fetchWord(Number(props.id))
    Object.assign(form, {
      dialect_word: word.dialect_word,
      mandarin: word.mandarin,
      region: word.region,
      example: word.example,
      source: word.source,
      remark: word.remark,
    })
  } catch {
    ElMessage.error('加载词条失败')
    router.push('/')
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) {
    return
  }

  saving.value = true
  try {
    if (isCreate.value) {
      const created = await createWord(form)
      ElMessage.success('创建成功')
      router.replace(`/words/${created.id}`)
    } else {
      await updateWord(Number(props.id), form)
      ElMessage.success('保存成功')
    }
  } catch {
    ElMessage.error(isCreate.value ? '创建失败' : '保存失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!props.id) {
    return
  }

  try {
    await ElMessageBox.confirm('确定删除该词条吗？', '提示', { type: 'warning' })
    deleting.value = true
    await deleteWord(Number(props.id))
    ElMessage.success('删除成功')
    router.push('/')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  } finally {
    deleting.value = false
  }
}

onMounted(loadWord)
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
