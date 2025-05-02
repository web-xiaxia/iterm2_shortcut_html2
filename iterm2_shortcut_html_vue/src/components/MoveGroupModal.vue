<script setup lang="ts">
import { ref} from 'vue'
import CommonModal from './common/CommonModal.vue'
import {AppConfig} from "@/types/AppConfig.ts";

const props = defineProps<{
  appConfig: AppConfig
  currentTabIndex: number
}>()

const showMoveTabModal = ref(false)
const currentMoveGroupIndex = ref(-1)
const targetTabIndex = ref(0)

const handleMoveGroupToOtherTab = () => {
  if (currentMoveGroupIndex.value !== -1 && targetTabIndex.value !== props.currentTabIndex) {
    const currentTab = props.currentTabIndex
    const group = props.appConfig.tabs[currentTab].buttonGroups[currentMoveGroupIndex.value]
    props.appConfig.tabs[targetTabIndex.value].buttonGroups.push({...group})
    props.appConfig.tabs[currentTab].buttonGroups.splice(currentMoveGroupIndex.value, 1)
    showMoveTabModal.value = false
  }
}

defineExpose({
  show: () => showMoveTabModal.value = true,
  setGroupIndex: (index: number) => currentMoveGroupIndex.value = index
})
</script>

<template>
  <CommonModal
    v-model:visible="showMoveTabModal"
    title="移动按钮组到其他tab"
  >
    <div class="form-row">
      <div class="form-group half">
        <div class="form-label">目标tab</div>
        <div class="form-input">
          <select v-model="targetTabIndex">
            <option 
              :value="index"
              v-for="(tab, index) in appConfig.tabs"
              :key="index"
            >
              {{ tab.title }}
            </option>
          </select>
        </div>
        <div class="form-input">
          <button class="button-primary" @click="handleMoveGroupToOtherTab">
            移动
          </button>
        </div>
      </div>
    </div>
  </CommonModal>
</template>

<style scoped>
.form-row {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

.form-row label {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-row select {
  padding: 8px;
  border-radius: 4px;
  background-color: #333;
  color: #fff;
  border: 1px solid #666;
}

.button-primary {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button-primary:hover {
  background-color: #45a049;
}
</style>