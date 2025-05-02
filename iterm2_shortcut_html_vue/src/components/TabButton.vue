<script setup lang="ts">

import {AppExecuteContext, AppSessionStatus, AppStatus, AppVariableHistoryStore} from "../types/AppConfig";
import {type AppButtonInfo, type AppButtonInfoType, type AppButtonInfoTypeRefreshInfo, AppButtonInfoTypeVariableInfo, type AppButtonInfoTypeWidthEdit, GetAppVariableRefWithGetFunc} from "../types/AppButton";
import {componentMap} from "./AppButtonComponent.ts";
import {handleMouseenterEditWidthWithTypeWidthEdit, handleMouseoutEditWidth} from "../types/Common.ts";
import {computed, type CSSProperties} from "vue";
import {AppButtonVariableRefreshConfigMap} from "./AppButtonVariableRefreshConfig.ts";

const props = defineProps<{
  buttons: AppButtonInfo<AppButtonInfoType>[],
  buttonIndex: number,
  appStatus: AppStatus,
  appSessionStatus: AppSessionStatus,
  executeContext: AppExecuteContext,
  variableHistory: AppVariableHistoryStore,
}>()

const emit = defineEmits<{
  handleDelete: [],
}>();

const componentInfo = computed(() => {
  return componentMap[buttonInfo.value.type]
})

const buttonInfo = computed(() => {
  return props.buttons[props.buttonIndex];
})
const variableInfo = GetAppVariableRefWithGetFunc(() => buttonInfo.value.linkage, props.executeContext.executeVariable.variable)

const linkageHide = computed<boolean>((): boolean => {
  if (props.appSessionStatus.appMode != 'show') {
    return false
  }
  if (!buttonInfo.value.linkage) {
    return false
  }
  const hide = !variableInfo.value.value.value || variableInfo.value.value.value === "false"
  if (buttonInfo.value.linkage_type == 'value_false') {
    return !hide
  }
  return hide
})


const afterMarginTypeWidthEdit = <AppButtonInfoTypeWidthEdit>{
  width: {
    get value(): number {
      return buttonInfo.value.afterMargin
    },
    set value(newVal: number) {
      buttonInfo.value.afterMargin = newVal
    }
  },
  getMinWidth(): number {
    return 0
  }
}

const refreshConfigMap = AppButtonVariableRefreshConfigMap

const showRefreshFunc = (refreshShow: string): boolean => {
  const typeVariableInfo = buttonInfo.value.buttonInfo as AppButtonInfoTypeRefreshInfo
  if (!typeVariableInfo.refreshType || typeVariableInfo.refreshType.length == 0) {
    return false
  }
  if (!typeVariableInfo.refreshShow) {
    return false
  }
  if (typeVariableInfo.refreshShow != refreshShow) {
    return false
  }
  if (typeVariableInfo.refreshShow == "focus") {
    if (props.appSessionStatus.appMode != 'show') {
      return false
    }
  }
  return true;
}
const showRefreshFocus = computed<boolean>((): boolean => {
  return showRefreshFunc("focus")
})
const showRefreshFixed = computed<boolean>((): boolean => {
  return showRefreshFunc("fixed")
})

const handleRefresh = () => {
  const typeVariableInfo = buttonInfo.value.buttonInfo as AppButtonInfoTypeRefreshInfo
  if (!typeVariableInfo.refreshType || typeVariableInfo.refreshType.length == 0) {
    return false
  }
  refreshConfigMap.get(typeVariableInfo.refreshType)?.refresh(props.executeContext, typeVariableInfo.refreshValue)
}
const beforeMarginTypeWidthEdit = <AppButtonInfoTypeWidthEdit>{
  width: {
    get value(): number {
      return buttonInfo.value.beforeMargin
    },
    set value(newVal: number) {
      buttonInfo.value.beforeMargin = newVal
    }
  },
  getMinWidth(): number {
    return 0
  }
}

const showTipsFixed = computed<boolean>(() => {
  const variableInfo = buttonInfo.value.buttonInfo as AppButtonInfoTypeVariableInfo
  return !(!variableInfo || !variableInfo.historyVariableValue);
})

const tipsList = computed<string[]>(() => {
  if (!showTipsFixed.value) {
    return []
  }
  const variableInfo = buttonInfo.value.buttonInfo as AppButtonInfoTypeVariableInfo
  const historyInfo = props.variableHistory[variableInfo.variableName]
  if (!historyInfo || !historyInfo.values || historyInfo.values.length == 0) {
    return []
  }
  if (historyInfo.values.length < 5) {
    return historyInfo.values
  }
  const ret = <string[]>[]
  for (let i = 0; i < 5; i++) {
    ret.push(historyInfo.values[i])
  }
  return ret
})
const handleTips=(v:string)=>{
  const buttonVariableInfo = buttonInfo.value.buttonInfo as AppButtonInfoTypeVariableInfo
  if (!buttonVariableInfo.variableName || buttonVariableInfo.variableName.length == 0) {
    return
  }
  const variableInfo=props.executeContext.executeVariable.variable[buttonVariableInfo.variableName]
  if (!variableInfo) {
    props.executeContext.executeVariable.variable[buttonVariableInfo.variableName]={
      values:[v],
      options:[]
    }
  }else {
    variableInfo.values=[v]
  }
}

</script>

<template>
  <div class="button-box" :style="{display:linkageHide?'none':undefined}">
    <span v-if="buttonInfo.beforeMargin"
          class="button-box-margin"
          :style="{width: buttonInfo.beforeMargin + 'em'}"
          :class="{'edit-width-model':props.appSessionStatus.editWidth}"
          @mouseenter="handleMouseenterEditWidthWithTypeWidthEdit($event,props.appSessionStatus, beforeMarginTypeWidthEdit)"
          @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
    ></span>
    <div class="button-box-button">
      <component :is="componentInfo.handler" v-bind="{
        button: buttonInfo,
        appStatus: props.appStatus,
        appSessionStatus: props.appSessionStatus,
        executeContext: props.executeContext,
        editConfig: componentInfo.editConfig,
      }"/>
      <div class="button-box-tools-fixed">
        <div class="button-box-tools-button-box" v-if="showRefreshFixed">
          <button class="button-box-tools-button" @click="handleRefresh">↻</button>
        </div>
        <div class="button-box-tools-button-box button-box-tools-tips-box" v-if="showTipsFixed">
          <button class="button-box-tools-button button-box-tools-button-tips-icon">📄</button>
          <div class="button-box-tools-tips-show-box">
            <button v-for="item in tipsList" class="button-type-text button-box-tools-tips-item" @click="handleTips(item)">{{ item }}</button>
            <div v-if="tipsList.length==0">无</div>
          </div>
        </div>
      </div>
      <div class="button-box-tools-focus">
        <div class="button-box-tools-button-box" v-if="showRefreshFocus">
          <button class="button-box-tools-button" @click="handleRefresh">↻</button>
        </div>
      </div>
      <div class="button-box-settings-box" v-if="props.appSessionStatus.appMode=='settings'">
        <button class="button-type-text handle-button-delete" @click="emit('handleDelete')">x</button>
      </div>
    </div>
    <span v-if="buttonInfo.afterMargin"
          class="button-box-margin"
          :style="{width: buttonInfo.afterMargin + 'em'}"
          :class="{'edit-width-model':props.appSessionStatus.editWidth}"
          @mouseenter="handleMouseenterEditWidthWithTypeWidthEdit($event,props.appSessionStatus, afterMarginTypeWidthEdit)"
          @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
    ></span>
  </div>
</template>

<style scoped>
.button-box {
  display: flex;
  align-items: center;
  margin: 0 0.3em 0 0;
}

.app-settings:not(.app-settings-edit-width) .button-box:hover {
  outline: 3px dashed #45aabec2;
  outline-offset: 0px;
}

.button-box-button {
  position: relative;
  flex: 1;
  display: flex;
}

.button-box-margin {
  height: 0.5em;
  display: inline-block;
}

.button-box-settings-box {
  flex: 1;
  display: none;
  position: absolute;
  z-index: 88;
  top: 0;
  background: #242424;
  border: 1px dashed rgb(131, 131, 131);
  border-radius: 3px;
  font-size: 8px;
  margin: 0 !important;
  padding: 0 !important;
}

.button-box:hover .button-box-settings-box {
  display: flex;
}

.app-settings-edit-width .button-box:hover .button-box-settings-box {
  display: none;
}

.button-box-settings-box .button-type-text {
  padding: 0 !important;
  margin: 0 !important;
  width: 10px !important;
  min-width: 10px !important;
  line-height: 10px !important;
}

.button-box-tools-fixed {
  display: flex;
  flex-direction: column;
}

.button-box-tools-focus {
  position: absolute;
  bottom: 100%;
  display: none;
  z-index: 20;
  padding: 0.5em 2em 0 1px;
}

.button-box-tools-button-box {
  display: flex;
}

.button-box-tools-focus .button-box-tools-button-box {
  margin-bottom: 1px;
  border-radius: 3px 3px 0 0;
}

.button-box-button:hover .button-box-tools-focus {
  display: flex;
}

.button-box-tools-button {
  border: 0;
  padding: 0 !important;
  margin: 0 !important;
  width: 1em !important;
  min-width: auto !important;
  height: 1em !important;
  font-size: inherit !important;
  line-height: 1.0 !important;
}

.button-box-tools-tips-box {
  position: relative;
}
.button-box-tools-button-tips-icon{
  font-size: 0.6em !important;
  padding: 0 0.3em !important;
  width: 1.3em !important;
}
.button-box-tools-button-tips-icon:hover{
  background-color: transparent;
}
.button-box-tools-tips-show-box {
  display: none;
  position: absolute;
  padding: 4px 4px;
  background: #242424d6;
  border: 1px solid #b3b3b3cf;
  top: 0.6em;
  right: -2em;
  z-index: 1000;
  border-radius: 3px;
  flex-direction: column;
  min-width: 90px;
  max-width: 180px;
}

.button-box-tools-tips-box:hover .button-box-tools-tips-show-box {
  display: flex;
}
.button-box-tools-tips-item{
  text-align: left;
  text-wrap: nowrap;
  overflow: hidden; /* 隐藏溢出的内容 */
  text-overflow: ellipsis; /* 超出部分显示为省略号 */
}

/* 确保按钮里的内容也继承字体大小，但排除模态框 */
.button-box :deep(*:not([class*="modal"]):not([class*="Modal"])) {
  font-size: inherit;
}

/* 自适应输入框和按钮大小，但排除模态框内的元素 */
.button-box :deep(input:not([class*="modal"] *):not([class*="Modal"] *)),
.button-box :deep(select:not([class*="modal"] *):not([class*="Modal"] *)),
.button-box :deep(button:not([class*="modal"] *):not([class*="Modal"] *)),
.button-box :deep(textarea:not([class*="modal"] *):not([class*="Modal"] *)) {
  height: auto;
  padding: 0.4em 0.6em;
  line-height: 1.2;
  border-radius: 0.3em;
  box-sizing: border-box;
}

.button-box :deep(button:not([class*="modal"] *):not([class*="Modal"] *)) {
  line-height: 1.0;
}

/* 单选框和复选框保持合理大小，但排除模态框内的元素 */
.button-box :deep(input[type="checkbox"]:not([class*="modal"] *):not([class*="Modal"] *)),
.button-box :deep(input[type="radio"]:not([class*="modal"] *):not([class*="Modal"] *)) {
  width: 1em;
  height: 1em;
  vertical-align: middle;
}

.button-box :deep(label:not([class*="modal"] *):not([class*="Modal"] *)) {
  margin: 0 0.3em 0 0;
}

/* 下拉菜单和多选框的自适应，但排除模态框内的元素 */
.button-box :deep(select:not([class*="modal"] *):not([class*="Modal"] *)) {
  padding-right: 1.5em;
}

/* 标签和文本元素的间距适配，但排除模态框内的元素 */
.button-box :deep(label:not([class*="modal"] *):not([class*="Modal"] *)),
.button-box :deep(span:not([class*="modal"] *):not([class*="Modal"] *)),
.button-box :deep(div:not([class*="modal"]):not([class*="Modal"])) {
  line-height: 2;
}

/* 按钮宽度自适应内容，但排除模态框内的元素 */
.button-box :deep(button:not([class*="modal"] *):not([class*="Modal"] *)) {
  min-width: 2.5em;
  white-space: nowrap;
}
</style>
