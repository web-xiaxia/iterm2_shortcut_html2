<script setup lang="ts">
import {computed, ref, watch, watchEffect} from 'vue';
import type {AppConfig, AppExecuteContext, AppSessionStatus, AppStatus} from "../types/AppConfig";
import Modal from './common/CommonModal.vue';
import type {AppButtonInfoTypeRefreshInfo, AppButtonInfoTypeVariableInfo, AppButtonTypeButton} from "../types/AppButton";

// 引入拆分的组件
import SettingsVariable from './settings/SettingsVariable.vue';
import SettingsVariableEvent from './settings/SettingsVariableEvent.vue';
import SettingsCodeConfig from './settings/SettingsCodeConfig.vue';
import SettingsTrigger from './settings/SettingsTrigger.vue';
import SettingsSystemConfig from "@/components/settings/SettingsSystemConfig.vue";
import SettingsExecConfig from "@/components/settings/SettingsExecConfig.vue";

const props = defineProps<{
  appConfig: AppConfig,
  executeContext: AppExecuteContext,
  appStatus: AppStatus,
  appSessionStatus: AppSessionStatus,
}>()

// 变量使用情况跟踪
const usedVariableSet = computed<Set<string>>(() => {
  const ret = new Set<string>()
  for (const tab of props.appConfig.tabs) {
    for (const group of tab.buttonGroups) {
      for (const button of group.buttons) {
        const typeVariable = button.buttonInfo as AppButtonInfoTypeVariableInfo
        if (typeVariable && typeVariable.variableName) {
          ret.add(typeVariable.variableName)
        }
      }
    }
  }
  return ret
})

function filterUsedByType(type: string): Set<string> {
  const ret = new Set<string>()
  for (const tab of props.appConfig.tabs) {
    for (const group of tab.buttonGroups) {
      for (const button of group.buttons) {
        if (button.type == "button") {
          const typeButton = button.buttonInfo as AppButtonTypeButton
          if (typeButton.type == type) {
            ret.add(typeButton.value)
          }
        } else {
          const typeVariable = button.buttonInfo as AppButtonInfoTypeRefreshInfo
          if (typeVariable.refreshType == type) {
            ret.add(typeVariable.refreshValue)
          }
        }
      }
    }
  }
  return ret
}

// 其他配置使用情况跟踪
const usedShellSet = computed<Set<string>>(() => {
  return filterUsedByType("shell_variable")
})

const usedPySet = computed<Set<string>>(() => {
  return filterUsedByType("py_variable")
})

const usedJsSet = computed<Set<string>>(() => {
  return filterUsedByType("js_variable")
})

const usedEventSet = computed<Set<string>>(() => {
  return new Set<string>()
})

const editSettings = computed<boolean>({
  get: () => {
    return !!props.appSessionStatus.editSettings
  },
  set: (newVel) => {
    props.appSessionStatus.editSettings = newVel
  }
})

// 固定的标签数组
const settingTabs = ref(['变量', '变量监听', 'js', 'py', 'shell', '事件', '触发', '运行配置', '系统配置']);
// 当前选中的标签索引
const currentTabIndex = ref(0);

// 切换标签
const switchTab = (index: number) => {
  currentTabIndex.value = index;
}

// 控制模态框显示
const showSettingsModal = ref(false);

// 监听appSessionStatus.editSettings变化，同步到showSettingsModal
watchEffect(() => {
  showSettingsModal.value = props.appSessionStatus.editSettings === true;
});

// 监听showSettingsModal变化，同步到appSessionStatus.editSettings
watch(showSettingsModal, (newValue) => {
  props.appSessionStatus.editSettings = newValue;
});

</script>

<template>
  <Modal
      v-model:visible="editSettings"
      title="设置"
  >
    <div class="settings-tabs">
      <div class="tabs-header">
        <div class="tabs-item-box">
          <div
              v-for="(tab, index) in settingTabs"
              :key="index"
              class="tab-item"
              :class="{ active: currentTabIndex === index }"
              @click="switchTab(index)">
            {{ tab }}
          </div>
        </div>
        <div class="tab-box-border"></div>
      </div>
      <div class="tabs-content">
        <!-- 变量标签页 -->
        <div v-if="currentTabIndex === 0" class="tab-pane">
          <SettingsVariable :appConfig="appConfig" :usedVariableSet="usedVariableSet"/>
        </div>

        <!-- 变量监听标签页 -->
        <div v-else-if="currentTabIndex === 1" class="tab-pane">
          <SettingsVariableEvent :appConfig="appConfig"/>
        </div>

        <!-- JavaScript配置标签页 -->
        <div v-else-if="currentTabIndex === 2" class="tab-pane">
          <SettingsCodeConfig
              :appConfig="appConfig"
              :executeContext="executeContext"
              configType="js"
              :usedSet="usedJsSet"
              title="JavaScript"
          />
        </div>

        <!-- Python配置标签页 -->
        <div v-else-if="currentTabIndex === 3" class="tab-pane">
          <SettingsCodeConfig
              :appConfig="appConfig"
              :executeContext="executeContext"
              configType="py"
              :usedSet="usedPySet"
              title="Python"
          />
        </div>

        <!-- Shell配置标签页 -->
        <div v-else-if="currentTabIndex === 4" class="tab-pane">
          <SettingsCodeConfig
              :appConfig="appConfig"
              :executeContext="executeContext"
              configType="shell"
              :usedSet="usedShellSet"
              title="Shell"
          />
        </div>

        <!-- 事件配置标签页 -->
        <div v-else-if="currentTabIndex === 5" class="tab-pane">
          <SettingsCodeConfig
              :appConfig="appConfig"
              :executeContext="executeContext"
              configType="event"
              :usedSet="usedEventSet"
              title="事件"
          />
        </div>

        <!-- 触发器配置标签页 -->
        <div v-else-if="currentTabIndex === 6" class="tab-pane">
          <SettingsTrigger :appConfig="appConfig"/>
        </div>

        <!-- 运行配置 -->
        <div v-else-if="currentTabIndex === 7" class="tab-pane">
          <SettingsExecConfig :appConfig="appConfig"/>
        </div>
        <!-- 系统配置 -->
        <div v-else-if="currentTabIndex === 8" class="tab-pane">
          <SettingsSystemConfig/>
        </div>

      </div>
    </div>
  </Modal>
</template>

<style scoped>
.modal-header h3 {
  margin: 0;
  font-size: 0.9rem;
}

.settings-tabs {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.tabs-header {
  display: flex;
  background-color: rgb(28, 25, 25);
  white-space: nowrap;
  position: relative;
  border-radius: 0.3em 0.3em 0 0;
}

.tabs-header .tab-box-border {
  border-bottom: 1px solid rgb(143, 143, 143);
  width: 100%;
  position: absolute;
  bottom: 0;
  z-index: 10;
}

.tabs-item-box {
  padding: 0.3em 0 0;
  display: flex;
  overflow-x: auto;
  scrollbar-width: none;
  scrollbar-color: transparent transparent;
  margin: 0 2em;
  position: relative;
}

.tab-item {
  padding: 2px 16px;
  cursor: pointer;
  border-radius: 5px 5px 0 0;
  margin: 0 2px;
  transition: background-color 0.2s;
  border: 1px solid transparent;
}

.tab-item:hover {
  background-color: rgb(65, 70, 74);
}

.tab-item.active {
  border: 1px solid rgb(143, 143, 143);
  border-bottom: 1px solid rgb(38, 37, 37);
  background-color: rgb(38, 37, 37);
  position: sticky;
  left: 0;
  right: 0;
  z-index: 21;
}

.tabs-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background-color: rgb(38, 37, 37);
  border: 1px solid rgb(143, 143, 143);
  border-top: 0;
  border-radius: 0 0 0.3em 0.3em;
}

.tab-pane {
  height: 100%;
}

.tab-pane h3 {
  margin-top: 0;
  color: #eee;
}

/* 共享样式，放在这里确保所有子组件都能用到 */
:deep(.config-container) {
  color: #eee;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: auto;
}

:deep(.config-list) {
  flex: 1;
}

:deep(.config-item) {
  display: flex;
  margin-bottom: 8px;
  padding: 8px;
  background-color: rgba(60, 60, 60, 0.5);
  border-radius: 4px;
  align-items: center;
}

:deep(.config-key) {
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 0 0 15em;
  white-space: nowrap;
}

:deep(.config-value) {
  margin: 0 10px;
  width: 25em;
}

:deep(.config-value input) {
  width: 100%;
  background-color: #333;
  border: 1px solid #555;
  color: #eee;
  padding: 4px 8px;
  border-radius: 3px;
}

:deep(.config-actions) {
  flex: 0 0 auto;
}

:deep(.add-config-form) {
  background-color: rgba(60, 60, 60, 0.3);
  padding: 12px;
  border-radius: 4px;
}

:deep(.add-config-form h4) {
  margin-top: 0;
  margin-bottom: 10px;
}

:deep(.config-input) {
  background-color: #333;
  border: 1px solid #555;
  color: #eee;
  padding: 6px 10px;
  border-radius: 3px;
}

:deep(.add-btn) {
  background-color: #2c5282;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 3px;
  cursor: pointer;
}

:deep(.add-btn:hover) {
  background-color: #3873b3;
}

/* 筛选样式 */
:deep(.filter-container) {
  display: flex;
  align-items: center;
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: rgba(60, 60, 60, 1);
  padding: 10px;
  border-radius: 4px;
  position: sticky;
  top: 0;
}

:deep(.filter-label) {
  margin-right: 10px;
  font-weight: bold;
}

:deep(.filter-options) {
  display: flex;
  gap: 20px;
}

:deep(.filter-option) {
  display: flex;
  align-items: center;
  cursor: pointer;
}

:deep(.filter-option input) {
  margin-right: 5px;
}

:deep(.delete-btn) {
  background-color: #732626;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 3px;
  cursor: pointer;
}

:deep(.delete-btn:hover) {
  background-color: #a03333;
}

:deep(.delete-btn[disabled]) {
  background-color: #ccc;
}

:deep(.delete-btn[disabled]:hover) {
  background-color: #ccc;
}

:deep(.empty-message) {
  text-align: center;
  padding: 20px;
  color: #999;
}

:deep(.variables-container) {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

:deep(.event-value-container) {
  margin-top: 10px;
  border-top: 1px dashed #555;
  padding-top: 10px;
}

:deep(.form-label) {
  font-weight: bold;
  margin-bottom: 5px;
  color: #bbb;
}

:deep(.textarea.config-input) {
  width: 100%;
  resize: vertical;
  background-color: #333;
  border: 1px solid #555;
  color: #eee;
  padding: 4px 8px;
  border-radius: 3px;
}

:deep(.variable-tag) {
  display: inline-flex;
  align-items: center;
  background-color: #2c5282;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  margin-right: 5px;
  margin-bottom: 5px;
}

:deep(.remove-variable-btn) {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  margin-left: 4px;
  padding: 0 4px;
}

:deep(.remove-variable-btn:hover) {
  color: #ff9999;
}

:deep(.monitor-item) {
  margin-bottom: 15px;
  padding: 12px;
  background-color: rgba(60, 60, 60, 0.5);
  border-radius: 4px;
  border-left: 3px solid #2c5282;
}

:deep(.monitor-item.editing) {
  border-left: 3px solid #a08c25;
  background-color: rgba(70, 70, 60, 0.5);
}

:deep(.monitor-header) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

:deep(.monitor-title) {
  font-weight: bold;
  font-size: 1.1em;
}

:deep(.event-type) {
  background-color: #2c5282;
  padding: 3px 8px;
  border-radius: 3px;
}

:deep(.monitor-actions) {
  display: flex;
  gap: 5px;
}

:deep(.edit-btn) {
  background-color: #4a6c8b;
  color: white;
  border: none;
  padding: 3px 8px;
  border-radius: 3px;
  cursor: pointer;
}

:deep(.edit-btn:hover) {
  background-color: #5b84a9;
}

:deep(.monitor-body) {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

:deep(.monitor-section) {
  margin-bottom: 8px;
}

:deep(.section-title) {
  font-weight: bold;
  margin-bottom: 5px;
  color: #bbb;
}

:deep(.event-value-display) {
  background-color: rgba(40, 40, 40, 0.5);
  padding: 8px;
  border-radius: 3px;
  font-family: monospace;
  white-space: pre-wrap;
  max-height: 150px;
  overflow-y: auto;
}

:deep(.variables-list) {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 8px;
}

:deep(.input-with-button) {
  display: flex;
  gap: 5px;
}

:deep(.small-btn) {
  background-color: #4a6c8b;
  color: white;
  border: none;
  padding: 3px 8px;
  border-radius: 3px;
  cursor: pointer;
}

:deep(.small-btn:hover) {
  background-color: #5b84a9;
}

:deep(.save-btn) {
  background-color: #2c5282;
  color: white;
  border: none;
  padding: 5px 12px;
  border-radius: 3px;
  cursor: pointer;
  margin-right: 5px;
}

:deep(.save-btn:hover) {
  background-color: #3873b3;
}

:deep(.cancel-btn) {
  background-color: #666;
  color: white;
  border: none;
  padding: 5px 12px;
  border-radius: 3px;
  cursor: pointer;
}

:deep(.cancel-btn:hover) {
  background-color: #888;
}

:deep(.monitor-edit-form) {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

:deep(.form-actions) {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

:deep(.form-row) {
  display: flex;
  gap: 10px;
  align-items: center;
}

:deep(.form-group) {
  margin-bottom: 10px;
}
</style>