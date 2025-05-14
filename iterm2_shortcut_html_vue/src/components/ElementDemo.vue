<template>
  <div class="element-demo">
    <el-card class="demo-card">
      <template #header>
        <div class="card-header">
          <h3>Element Plus 黑色主题示例</h3>
          <el-switch
            v-model="isDark"
            inline-prompt
            active-text="暗色"
            inactive-text="亮色"
            @change="toggleDarkMode"
          />
        </div>
      </template>
      <div class="card-content">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-button type="primary">主要按钮</el-button>
            <el-button type="success">成功按钮</el-button>
            <el-button type="warning">警告按钮</el-button>
            <el-button type="danger">危险按钮</el-button>
            <el-button type="info">信息按钮</el-button>
          </el-col>
          <el-col :span="12">
            <el-input v-model="input" placeholder="请输入内容"></el-input>
            <el-select v-model="value" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-col>
        </el-row>
        
        <el-divider />
        
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="date" label="日期" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="address" label="地址" />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 模拟数据
const isDark = ref(true)
const input = ref('')
const value = ref('')
const options = [
  { value: 'option1', label: '选项1' },
  { value: 'option2', label: '选项2' },
  { value: 'option3', label: '选项3' },
]
const tableData = [
  { date: '2023-01-01', name: '张三', address: '北京市朝阳区' },
  { date: '2023-01-02', name: '李四', address: '上海市浦东新区' },
  { date: '2023-01-03', name: '王五', address: '广州市天河区' },
]

// 切换暗黑模式
const toggleDarkMode = (val: boolean) => {
  // 获取html元素
  const html = document.documentElement
  // 切换暗黑模式类名
  if (val) {
    html.classList.add('dark')
    document.body.setAttribute('class', 'el-theme-dark')
  } else {
    html.classList.remove('dark')
    document.body.removeAttribute('class')
  }
}

// 初始化暗黑模式
if (isDark.value) {
  document.documentElement.classList.add('dark')
  document.body.setAttribute('class', 'el-theme-dark')
}
</script>

<style scoped>
.element-demo {
  max-width: 800px;
  margin: 20px auto;
}

.demo-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  margin-top: 20px;
}

.el-row {
  margin-bottom: 20px;
}

.el-button {
  margin-right: 10px;
  margin-bottom: 10px;
}

.el-input, .el-select {
  margin-bottom: 15px;
  width: 100%;
}
</style> 