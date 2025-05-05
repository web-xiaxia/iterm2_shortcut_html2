<script setup lang="ts">

import CommonSelect from "@/components/common/CommonSelect.vue";
import {computed} from "vue";
import {AppButtonTypeButtonTypeList, AppButtonTypeButtonTypeMap} from "@/components/AppButtonTypeButtonTypeConfig.ts";
import {ButtonEditorButtonTypeProps} from "@/types/AppConfig.ts";
import type {AppButtonInfoTypeRefreshInfo} from "@/types/AppButton.ts";

const props = defineProps<ButtonEditorButtonTypeProps>();

const buttonTypeList = AppButtonTypeButtonTypeList;
const buttonTypeTitleMap = AppButtonTypeButtonTypeMap;

const getOptionsByType = computed<string[]>(() => {
  const refreshType = props.buttonProps.button.buttonInfo.type
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return []
  return config.getOptions(props.buttonProps.executeContext.executeVariable)
})
const getInputTypeByType = computed< "input" | "textarea" | "variable">(() => {
  const refreshType = props.buttonProps.button.buttonInfo.type
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return 'input'
  return config.inputType
})
const getInputTitleByType = computed<string>(() => {
  const refreshType = props.buttonProps.button.buttonInfo.type
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return "内容"
  return config.title
})

const handleRefresh = () => {
  const buttonInfo = props.buttonProps.button.buttonInfo
  buttonTypeTitleMap.get(buttonInfo.type)?.send(props.buttonProps.executeContext, buttonInfo.value)
}
</script>

<template>
  <div class="form-row">
    <div class="form-group">
      <div class="form-label">按钮类型</div>
      <div class="form-input">
        <select v-model="props.buttonProps.button.buttonInfo.type">
          <option v-for="buttonType in  buttonTypeList" :value="buttonType.key">
            {{ buttonType.name }}
          </option>
        </select>
      </div>
    </div>
    <slot name="type-remarks"></slot>
  </div>
  <div class="form-row">
    <div class="form-group">
      <div class="form-label">{{ getInputTitleByType }}</div>
      <div class="form-input" style="display: flex;flex-direction: column">
        <button @click="handleRefresh" style="width: 10em;">run</button>
        <input v-if="getInputTypeByType=='input'" v-model="props.buttonProps.button.buttonInfo.value">
        <CommonSelect
            v-else-if="getInputTypeByType=='variable'"
            :modelValue="props.buttonProps.button.buttonInfo.value"
            :options="getOptionsByType"
            :hideAdd="true"
            :hideRemove="true"
            width="14.8em"
            height="2.2em"
            @update:modelValue="(newVal:string)=>props.buttonProps.button.buttonInfo.value=newVal"
        />
        <textarea autocapitalize="off" style="width: 37.3em" v-else v-model="props.buttonProps.button.buttonInfo.value" rows="7"></textarea>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>