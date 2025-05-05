<script setup lang="ts">
import {ref} from 'vue';
import type {AppConfig} from "@/types/AppConfig.ts";

const props = defineProps<{
  appConfig: AppConfig,
  usedVariableSet: Set<string>
}>();

// 变量相关功能
const newVarKey = ref('');
const newVarValue = ref('');

// 变量筛选类型
type FilterType = 'all' | 'used' | 'unused';
const variableFilter = ref<FilterType>('all');

// 修改变量值
const updateVariable = (key: string, value: string) => {
  if (props.appConfig.variable) {
    if (!props.appConfig.variable[key]) {
      props.appConfig.variable[key] = {
        values: [],
        options: []
      };
    }
    props.appConfig.variable[key].values = [value];
  }
};

// 删除变量
const deleteVariable = (key: string) => {
  if (props.appConfig.variable) {
    delete props.appConfig.variable[key];
  }
};

// 添加新变量
const addNewVariable = () => {
  if (newVarKey.value.trim() && newVarValue.value.trim()) {
    if (!props.appConfig.variable) {
      props.appConfig.variable = {};
    }
    props.appConfig.variable[newVarKey.value] = {
      values: [newVarValue.value],
      options: []
    };
    newVarKey.value = '';
    newVarValue.value = '';
  }
};

// 处理变量值改变的事件
const handleVariableChange = (key: string, event: Event) => {
  const target = event.target as HTMLInputElement;
  updateVariable(key, target.value);
};
</script>

<template>
  <div class="config-container">
    <div class="add-config-form">
      <div class="form-row">
        <div>添加新变量</div>
        <input
            type="text"
            autocapitalize="off"
            autocomplete="off"
            spellcheck="false"
            v-model="newVarKey"
            placeholder="变量名称"
            class="config-input"
        />
        <input
            type="text"
            autocapitalize="off"
            autocomplete="off"
            spellcheck="false"
            v-model="newVarValue"
            placeholder="变量值"
            class="config-input"
        />
        <button @click="addNewVariable" class="add-btn">添加</button>
      </div>
    </div>
    <!-- 变量列表 -->
    <div class="config-list">
      <!-- 筛选变量 -->
      <div class="filter-container">
        <div class="filter-label">筛选：</div>
        <div class="filter-options">
          <label class="filter-option">
            <input type="radio" v-model="variableFilter" value="all"/>
            <span>全部</span>
          </label>
          <label class="filter-option">
            <input type="radio" v-model="variableFilter" value="used"/>
            <span>使用中</span>
          </label>
          <label class="filter-option">
            <input type="radio" v-model="variableFilter" value="unused"/>
            <span>未使用</span>
          </label>
        </div>
      </div>
      <div v-for="[key, variable] in Object.entries(props.appConfig.variable || {})" :key="key" 
          v-show="variableFilter === 'all' || 
                (variableFilter === 'used' && props.usedVariableSet.has(key)) || 
                (variableFilter === 'unused' && !props.usedVariableSet.has(key))"
          class="config-item">
        <div class="config-key">{{ key }}</div>
        <div class="config-value">
          <input
              type="text"
              autocapitalize="off"
              autocomplete="off"
              spellcheck="false"
              :value="variable.values && variable.values.length > 0 ? variable.values[variable.values.length - 1] : ''"
              @change="(e) => handleVariableChange(key, e)"
          />
        </div>
        <div class="config-actions">
          <button @click="deleteVariable(key)" :disabled="props.usedVariableSet.has(key)" class="delete-btn">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 这些样式会被主组件里的样式覆盖，保留作为参考 */
</style> 