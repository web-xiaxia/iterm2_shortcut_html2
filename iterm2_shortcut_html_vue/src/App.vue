<script setup lang="ts">
import {computed, type CSSProperties, ref, watch} from 'vue'
import TabButtonGroup from "./components/TabButtonGroup.vue";
import {AppConfig, AppExecuteVariable, AppGroup, AppSessionStatus, AppStatus, AppVariableHistoryStore} from "./types/AppConfig";
import {getAppConfig, getAppStatus, getAppVariableHistoryStore, setAppConfig, setAppStatus, setAppVariableHistoryStore} from "./config/AppConfig";
import {handleEditWidth} from "./types/Common";
import AppWidthEdit from "./components/AppWidthEdit.vue";
import AppToolbelt from "./components/AppToolbelt.vue";
import Tab from "./components/Tab.vue";
import AppSettingsEdit from "./components/AppSettingsEdit.vue";
import {newAppExecuteContext} from "@/types/ExecuteContext.ts";
import FullScreenInputModal from "./components/FullScreenInputModal.vue"
import KeyModifiersDisplay from "./components/KeyModifiersDisplay.vue"
import MoveGroupModal from "./components/MoveGroupModal.vue"
import {appVariableHistoryFunc, appVariablesChange, appVariablesRefreshFunc} from '@/AppVariablesRefresh'
import {debounce} from "lodash";

// 配置信息
const appConfig = ref<AppConfig>(getAppConfig())
const debounceSetAppConfig = debounce((newVal: AppConfig) => {
  setAppConfig(newVal);
}, 900)
watch(appConfig, (newVal: AppConfig) => {
  debounceSetAppConfig(newVal);
}, {deep: true});

// 状态
const appStatus = ref<AppStatus>(getAppStatus())
watch(appStatus, (newVal: AppStatus) => {
  setAppStatus(newVal);
}, {deep: true});

// 历史记录
const appVariableHistoryStore = ref<AppVariableHistoryStore>(getAppVariableHistoryStore())
watch(appVariableHistoryStore, (newVal: AppVariableHistoryStore) => {
  setAppVariableHistoryStore(newVal);
}, {deep: true});

// 实时状态
const appSessionStatusRef = ref<AppSessionStatus>(<AppSessionStatus>{
  appMode: "show",
  editWidth: false,
  showFullScreenInputModal: false,
  fullScreenInputValue: "",
});
const appSessionStatus = computed<AppSessionStatus>((): AppSessionStatus => {
  return appSessionStatusRef.value as AppSessionStatus;
})

// 运行信息
const appExecuteVariable = computed<AppExecuteVariable>(() => appConfig.value)
const appExecuteContext = newAppExecuteContext(appSessionStatus, appExecuteVariable)


// 变量刷新
const appVariablesRefresh = appVariablesRefreshFunc(appConfig, appExecuteContext)
const appVariableHistory = appVariableHistoryFunc(appExecuteContext, appVariableHistoryStore)
appVariablesChange(appConfig)(function (newVal: string[]) {
  appVariablesRefresh(newVal);
  appVariableHistory(newVal);
})

// 样式
const appModeClass = computed<CSSProperties>(() => {
  return {
    'app-settings': appSessionStatus.value.appMode == 'settings',
    'app-settings-edit-width': appSessionStatus.value.editWidth,
  }
});

// 展示分组
const showButtonGroups = computed<AppGroup[]>(() => {
  let nowIndex = appStatus.value.index
  if (nowIndex < 1) nowIndex = 0;
  if (nowIndex >= appConfig.value.tabs.length) nowIndex = appConfig.value.tabs.length - 1;

  const nowTab = appConfig.value.tabs[nowIndex]
  if (!nowTab.hide) {
    return nowTab.buttonGroups
  }
  for (let i = 0; i < appConfig.value.tabs.length; i++) {
    const tab = appConfig.value.tabs[i]
    if (!tab.hide) {
      appStatus.value.index = i
      return tab.buttonGroups
    }
  }
  return []
})


// 处理将按钮组移动到其他tab的初始事件
const moveGroupModalRef = ref()
const handleMoveGroup = (groupIndex: number) => {
  moveGroupModalRef.value.setGroupIndex(groupIndex)
  moveGroupModalRef.value.show()
}

// 监听 editWidth 变化
const editWidthHandleKeyDown = (event: KeyboardEvent) => {
  handleEditWidth(event.key, appSessionStatus.value)
}
watch(() => appSessionStatus.value.editWidth, (newVal) => {
  if (newVal) {
    document.addEventListener('keydown', editWidthHandleKeyDown);
  } else {
    document.removeEventListener('keydown', editWidthHandleKeyDown);
  }
});

</script>

<template>
  <AppSettingsEdit
      :appConfig="appConfig as any"
      :appStatus="appStatus"
      :appSessionStatus="appSessionStatus"
  />
  <div :class="appModeClass">
    <AppWidthEdit :appSessionStatus="appSessionStatus" v-if="appSessionStatus.editWidth"/>
    <Tab :tabs="appConfig.tabs" :appStatus="appStatus" :appSessionStatus="appSessionStatus"/>
    <div style="font-size: 14px;max-width: 100vw;">
      <TabButtonGroup
          v-if="appConfig.tabs.filter((v)=>!v.hide).length>0"
          :buttonGroups="showButtonGroups"
          :appStatus="appStatus"
          :appSessionStatus="appSessionStatus"
          :executeContext="appExecuteContext"
          :variableHistory="appVariableHistoryStore"
          @moveGroupToOtherTab="handleMoveGroup"
      />
    </div>

    <!-- 工具栏组件 -->
    <AppToolbelt
        :appConfig="appConfig"
        :appStatus="appStatus"
        :appSessionStatus="appSessionStatus"
        :executeContext="appExecuteContext"
        :variableHistory="appVariableHistoryStore"
    />

    <!-- 移动分组 -->
    <MoveGroupModal
        ref="moveGroupModalRef"
        :app-config="appConfig"
        :current-tab-index="appStatus.index"
    />

    <!-- 新增全屏输入模态框 -->
    <FullScreenInputModal
        :appStatus="appStatus"
        :appSessionStatus="appSessionStatus"
        :executeContext="appExecuteContext"
    />

    <!-- 修饰键状态显示组件 -->
    <KeyModifiersDisplay
        :executeContext="appExecuteContext"
    />
  </div>
</template>

<style scoped>
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
</style>
