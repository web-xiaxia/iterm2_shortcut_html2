<script setup lang="ts">

import {ref} from "vue";
import type {AppVariableTool} from "@/types/AppButton.ts";

const props = defineProps<{
  variableInfo: AppVariableTool
  variableName: string
}>();
const {variableInfo} = props;
const newOption = ref('');

function addOption() {
  if (newOption.value.trim() && !variableInfo.variable.value.options.includes(newOption.value)) {
    variableInfo.variable.value.options.push(newOption.value);
    newOption.value = '';
  }
}

function updateOptionValue(index: number, value: string) {
  if (value.trim()) {
    variableInfo.variable.value.options[index] = value;
  }
}

function removeOption(index: number) {
  variableInfo.variable.value.options.splice(index, 1);
}

function moveOption(index: number, direction: number) {
  const newIndex = index + direction;
  if (newIndex >= 0 && newIndex < variableInfo.variable.value.options.length) {
    const temp = variableInfo.variable.value.options[index];
    variableInfo.variable.value.options[index] = variableInfo.variable.value.options[newIndex];
    variableInfo.variable.value.options[newIndex] = temp;
  }
}
</script>

<template>
  <div class="options-section" v-if="variableName && variableName.length>0">
    <h3 class="options-title">选项管理</h3>

    <div class="option-add-container">
      <div class="option-input-wrapper">
        <input
            v-model="newOption"
            type="text"
            autocapitalize="off"
            autocomplete="off"
            spellcheck="false"
            placeholder="输入新选项"
            @keyup.enter="addOption"
            class="option-add-input"
        />
      </div>
      <div class="option-button-wrapper">
        <button class="option-add-btn" @click="addOption">添加</button>
      </div>
    </div>

    <div class="options-list">
      <div v-if="variableInfo.variable.value.options.length === 0" class="empty-options">
        暂无选项，请添加
      </div>

      <div
          v-for="(option, index) in variableInfo.variable.value.options"
          :key="index"
          class="option-item"
      >
        <div class="option-number">{{ index + 1 }}</div>
        <input
            type="text"
            autocapitalize="off"
            autocomplete="off"
            spellcheck="false"
            class="option-input"
            :value="option"
            @input="(e:Event) => updateOptionValue(index, (e.target as HTMLInputElement).value)"
        />
        <div class="option-actions">
          <button
              class="option-btn option-btn-up"
              @click="moveOption(index, -1)"
              :disabled="index === 0"
              title="上移"
          >↑
          </button>
          <button
              class="option-btn option-btn-down"
              @click="moveOption(index, 1)"
              :disabled="index === variableInfo.variable.value.options.length - 1"
              title="下移"
          >↓
          </button>
          <button
              class="option-btn option-btn-delete"
              @click="removeOption(index)"
              title="删除"
          >×
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

/* 选项管理的新样式 */
.options-section {
  border: 1px solid #444;
  border-radius: 4px;
  padding: 12px;
  background-color: rgba(0, 0, 0, 0.1);
}

.options-title {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: bold;
}

.option-add-container {
  display: flex;
  margin-bottom: 12px;
  align-items: center;
}

.option-input-wrapper {
  margin-right: 10px;
}

.option-add-input {
  width: 100%;
  padding: 8px 10px;
  border-radius: 4px;
  color: #fff;
  box-sizing: border-box;
}

.option-button-wrapper {
  flex-shrink: 0;
}

.option-add-btn {
  background-color: #2c5282;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
  font-weight: 500;
}

.option-add-btn:hover {
  background-color: #3182ce;
}

.options-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #555;
  border-radius: 4px;
  background-color: rgba(0, 0, 0, 0.2);
}

.empty-options {
  padding: 15px;
  text-align: center;
  color: #999;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #444;
}

.option-item:last-child {
  border-bottom: none;
}

.option-number {
  min-width: 24px;
  text-align: center;
  color: #999;
  margin-right: 8px;
}

.option-input {
  padding: 5px 8px;
  color: #fff;
}

.option-actions {
  display: flex;
  margin-left: 8px;
}

.option-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  padding: 0;
  font-size: 12px;
  margin: 0 2px;
  border-radius: 3px;
  border: 1px solid #555;
  background-color: #333;
  color: #fff;
  cursor: pointer;
}

.option-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.option-btn:hover:not(:disabled) {
  background-color: #444;
}

.option-btn-up,
.option-btn-down {
  background-color: #4a5568;
}

.option-btn-delete {
  background-color: #c53030;
}
</style>