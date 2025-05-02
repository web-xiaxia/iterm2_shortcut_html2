<script setup lang="ts">
import {ref, computed, onMounted, onUnmounted} from 'vue';
import type {AppConfig, AppSessionStatus, AppStatus, AppExecuteContext, AppVariableHistoryStore} from "../types/AppConfig";
import TabButtonGroup from './TabButtonGroup.vue';
import CommonModal from './common/CommonModal.vue';

const props = defineProps<{
  appConfig: AppConfig,
  appStatus: AppStatus,
  appSessionStatus: AppSessionStatus,
  executeContext: AppExecuteContext,
  variableHistory: AppVariableHistoryStore,
}>();

if (!props.appConfig.toolbelt) {
  props.appConfig.toolbelt = {
    height: 200,
  }
}

// 计算样式
const toolbeltStyle = computed(() => {
  return {
    height: !props.appStatus.hideToolbelt ? `${props.appConfig.toolbelt.height}px` : '0',
    transition: isDragging.value ? 'none' : 'height 0.3s ease-out'
  };
});

// 获取当前应该显示的tab
const activeToolbeltTab = computed(() => {
  if (props.appConfig.tabs.length == 0) {
    return null
  }
  for (const tab of props.appConfig.tabs) {
    if (tab.model == 'toolbelt') {
      return tab
    }
  }
  return null;
});


// 被选中的tab (0表示空白选项)
const selectedTabIndex = computed<number>({
  get: () => {
    if (props.appConfig.tabs.length == 0) {
      return 0
    }
    for (let i = 0; i < props.appConfig.tabs.length; i++) {
      const tab = props.appConfig.tabs[i];
      if (tab.model == 'toolbelt') {
        return i + 1
      }
    }
    return 0;
  },
  set: (newVal: number) => {
    const selectIndex = newVal - 1
    let newIndex = -1
    for (let i = 0; i < props.appConfig.tabs.length; i++) {
      const tab = props.appConfig.tabs[i];
      if (tab.model == 'toolbelt') {
        tab.model = undefined
        tab.hide = false
      }
      if (i === selectIndex) {
        tab.model = 'toolbelt'
        tab.hide = true
      }
      if (newIndex === -1 && !tab.hide && i !== selectIndex) {
        newIndex = i
      }
    }
    if (props.appStatus.index == selectIndex) {
      props.appStatus.index = newIndex
    }
  }
})

// 控制设置模态框
const showSettings = ref(false);

// 切换可见性
const toggleVisibility = () => {
  props.appStatus.hideToolbelt = !props.appStatus.hideToolbelt;
};

// 拖拽相关状态和方法
const isDragging = ref(false);
const startY = ref(0);
const startHeight = ref(0);

const handleMouseDown = (e: MouseEvent) => {
  if (props.appStatus.hideToolbelt) return;

  isDragging.value = true;
  startY.value = e.clientY;
  startHeight.value = props.appConfig.toolbelt.height;

  // 添加鼠标样式
  document.body.style.cursor = 'ns-resize';
  document.body.style.userSelect = 'none';
};

const handleMouseMove = (e: MouseEvent) => {
  if (!isDragging.value) return;

  // 计算新高度 (向上拖动时减少高度)
  const deltaY = startY.value - e.clientY;
  let newHeight = startHeight.value + deltaY;

  // 限制最小和最大高度
  newHeight = Math.max(100, Math.min(newHeight, window.innerHeight * 0.8));

  // 更新工具栏高度
  props.appConfig.toolbelt.height = newHeight;
};

const handleMouseUp = () => {
  if (!isDragging.value) return;

  isDragging.value = false;

  // 恢复鼠标样式
  document.body.style.cursor = '';
  document.body.style.userSelect = '';
};

// 添加和移除全局事件监听器
onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
});

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
});
</script>

<template>
  <div class="toolbelt-container">
    <!-- 工具栏主体 -->
    <div class="toolbelt-content" :style="toolbeltStyle">
      <!-- 拖拽边框 -->
      <div
          class="resize-handle"
          @mousedown="handleMouseDown"
          v-show="!props.appStatus.hideToolbelt"
      ></div>

      <!-- 移除原来的头部，改为浮动按钮 -->
      <div class="floating-actions">
        <button class="toolbelt-button" v-if="props.appSessionStatus.appMode == 'settings'" @click="showSettings = true">⚙</button>
        <button
            class="toolbelt-button"
            @click="toggleVisibility"
            @contextmenu.prevent="showSettings = true"
            :title="!props.appStatus.hideToolbelt ? '折叠工具栏 (右键点击设置)' : '展开工具栏 (右键点击设置)'"
        >
          {{ !props.appStatus.hideToolbelt ? '▼' : '▲' }}
        </button>
      </div>

      <div class="toolbelt-body" v-if="activeToolbeltTab && !props.appStatus.hideToolbelt">
        <div class="toolbelt-body-content">
          <TabButtonGroup
              v-if="activeToolbeltTab.buttonGroups"
              :buttonGroups="activeToolbeltTab.buttonGroups"
              :appStatus="appStatus"
              :appSessionStatus="appSessionStatus"
              :executeContext="props.executeContext"
              :variableHistory="props.variableHistory"
          />
        </div>
      </div>
    </div>

    <!-- 设置模态框 -->
    <CommonModal
        v-model:visible="showSettings"
        title="工具栏设置"
    >
      <div class="settings-form">
        <div class="form-group">
          <label>显示的Tab:</label>
          <select v-model="selectedTabIndex">
            <option :value="0">无内容</option>
            <option
                v-for="(tab, index) in props.appConfig.tabs"
                :key="index + 1"
                :value="index + 1"
            >
              {{ tab.title }}
            </option>
          </select>
          <span class="toolbelt-hint">选中的tab将在工具栏显示，并在主界面隐藏</span>
        </div>

        <div class="form-group">
          <label>高度设置 (px):</label>
          <input
              type="number"
              v-model.number="props.appConfig.toolbelt.height"
              min="100"
              max="500"
          />
        </div>
      </div>
    </CommonModal>
  </div>
</template>

<style scoped>
.toolbelt-container {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  max-height: 80vh;
  z-index: 100;
  background-color: rgb(28, 25, 25);
  border-top: 1px solid rgb(143, 143, 143);
}

/* 拖拽边框样式 */
.resize-handle {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 6px;
  cursor: ns-resize;
  z-index: 101;
  background-color: transparent;
  transition: background-color 0.2s;
}

.resize-handle:hover {
  background-color: rgba(100, 100, 100, 0.3);
}

.resize-handle:active {
  background-color: rgba(100, 100, 100, 0.5);
}

/* 添加浮动按钮样式 */
.floating-actions {
  position: absolute;
  top: 2px;
  right: 16px;
  display: flex;
  gap: 8px;
  z-index: 102;
  transform: translateY(-100%);
}

.toolbelt-button {
  background-color: rgb(28, 25, 25);
  border: 0.13em solid rgb(143, 143, 143);
  border-bottom: 0.1em solid rgb(28, 25, 25);
  color: #fff;
  cursor: pointer;
  font-size: 12px;
  /* line-height: 16px; */
  padding: 6px 12px 2px 12px;
  border-radius: 22px 22px 0 0;
  min-width: 30px;
  transition: background-color 0.2s;
  vertical-align: bottom;
}

.toolbelt-button:hover {
  background-color: #444;
}

.toolbelt-body {
  padding: 4px 10px;
  /*overflow-y: auto;*/
  height: 100%;
  transition: transform .5s cubic-bezier(.23, 1, .32, 1), box-shadow .3s cubic-bezier(.23, 1, .32, 1);
  background-color: rgb(28, 25, 25);
  display: flex;
  justify-content: center;
}

.toolbelt-body-content {
  width: fit-content;
  min-width: 50vw;
}

/* 移除不再需要的展开按钮样式 */

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: bold;
  color: #fff;
}

.form-group select,
.form-group input {
  padding: 8px;
  background-color: #333;
  color: #fff;
  border: 1px solid #666;
  border-radius: 4px;
}

.toolbelt-hint {
  font-size: 12px;
  color: #aaa;
  margin-top: 4px;
}
</style>