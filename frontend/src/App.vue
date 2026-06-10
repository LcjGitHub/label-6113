<template>
  <el-container class="app-layout">
    <el-header class="app-header">
      <div class="header-inner">
        <h1 class="title" @click="router.push('/')">方言词汇库</h1>
        <el-button type="primary" :icon="Plus" @click="router.push('/words/new')">
          新增词条
        </el-button>
      </div>
    </el-header>
    <el-main class="app-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
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
