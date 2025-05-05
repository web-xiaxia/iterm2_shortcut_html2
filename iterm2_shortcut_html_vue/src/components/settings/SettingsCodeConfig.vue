<script setup lang="ts">
import {ref} from 'vue';
import type {AppConfig} from "@/types/AppConfig.ts";
import type {AppKvStrStore} from "@/types/AppButton.ts";

const props = defineProps<{
  appConfig: AppConfig,
  configType: 'js' | 'py' | 'shell' | 'event',
  usedSet: Set<string>,
  title: string,
}>();

// 新增字段的key和value
const newConfigKey = ref('');
const newConfigValue = ref('');

// 配置筛选类型
type FilterType = 'all' | 'used' | 'unused';
const configFilter = ref<FilterType>('all');

// 获取排序和过滤后的配置列表
const getFilteredConfig = () => {
  if (!props.appConfig[props.configType]) return [];

  // 获取条目并排序
  const entries = Object.entries(props.appConfig[props.configType] as AppKvStrStore);
  const sortedEntries = entries.sort((a, b) => a[0].localeCompare(b[0]));

  // 根据筛选条件过滤
  if (configFilter.value === 'all') {
    return sortedEntries;
  } else if (configFilter.value === 'used') {
    return sortedEntries.filter(([key]) => props.usedSet.has(key));
  } else {
    return sortedEntries.filter(([key]) => !props.usedSet.has(key));
  }
};

// 修改配置值
const updateConfig = (key: string, value: string) => {
  if (props.appConfig[props.configType]) {
    (props.appConfig[props.configType] as AppKvStrStore)[key] = value;
  }
};

// 删除配置
const deleteConfig = (key: string) => {
  if (props.appConfig[props.configType]) {
    delete (props.appConfig[props.configType] as AppKvStrStore)[key];
  }
};

// 添加新配置
const addNewConfig = () => {
  if (newConfigKey.value.trim() && newConfigValue.value.trim()) {
    if (!props.appConfig[props.configType]) {
      props.appConfig[props.configType] = {};
    }
    (props.appConfig[props.configType] as AppKvStrStore)[newConfigKey.value] = newConfigValue.value;
    newConfigKey.value = '';
    newConfigValue.value = '';
  }
};

// 处理配置值改变的事件
const handleConfigChange = (key: string, event: Event) => {
  const target = event.target as HTMLTextAreaElement;
  updateConfig(key, target.value);
};
</script>

<template>
  <div class="config-container">
    <h3>{{ title }}配置</h3>

    <!-- 添加新配置 -->
    <div class="add-config-form">
      <h4>添加新配置</h4>
      <div class="form-row">
        <input
            type="text"
            autocapitalize="off"
            v-model="newConfigKey"
            placeholder="配置名称"
            class="config-input"
        />
        <textarea
            autocapitalize="off"
            v-model="newConfigValue"
            placeholder="配置值"
            class="config-input"
            rows="2"
        ></textarea>
        <button @click="addNewConfig" class="add-btn">添加</button>
      </div>
    </div>

    <!-- 筛选配置 -->
    <div class="filter-container">
      <div class="filter-label">筛选：</div>
      <div class="filter-options">
        <label class="filter-option">
          <input type="radio" v-model="configFilter" value="all"/>
          <span>全部</span>
        </label>
        <label class="filter-option">
          <input type="radio" v-model="configFilter" value="used"/>
          <span>使用中</span>
        </label>
        <label class="filter-option">
          <input type="radio" v-model="configFilter" value="unused"/>
          <span>未使用</span>
        </label>
      </div>
    </div>

    <!-- 配置列表 -->
    <div class="config-list">
      <div v-for="[key, value] in getFilteredConfig()" :key="key" class="config-item">
        <div class="config-key">{{ key }}</div>
        <div class="config-value">
          <textarea
              autocapitalize="off"
              :value="value"
              @change="(e) => handleConfigChange(key, e)"
              rows="2"
          ></textarea>
        </div>
        <div class="config-actions">
          <button @click="deleteConfig(key)" :disabled="props.usedSet.has(key)" class="delete-btn">删除</button>
        </div>
      </div>
    </div>
  </div>
</template> 