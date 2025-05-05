<script setup lang="ts">
import type {ButtonEditorRefreshProps} from "@/types/AppConfig.ts";
import {AppButtonVariableRefreshConfigList, AppButtonVariableRefreshConfigMap} from "../AppButtonVariableRefreshConfig";
import {computed, ref} from "vue";
import CommonSelect from "../common/CommonSelect.vue";
import type {AppButtonInfoTypeRefreshInfo} from "@/types/AppButton.ts";

const props = defineProps<ButtonEditorRefreshProps>();
const buttonTypeList = AppButtonVariableRefreshConfigList
const buttonTypeTitleMap = AppButtonVariableRefreshConfigMap

const refreshTypeSelected = computed<boolean>((): boolean => {
  return !!props.buttonProps.button.buttonInfo.refreshType && props.buttonProps.button.buttonInfo.refreshType.length > 0
})
const getOptionsByRefreshType = computed<string[]>(() => {
  const refreshType = props.buttonProps.button.buttonInfo.refreshType
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return []
  return config.getOptions(props.buttonProps.executeContext.executeVariable)
})
const getInputTypeByRefreshType = computed<"input" | "textarea" | "variable">(() => {
  const refreshType = props.buttonProps.button.buttonInfo.refreshType
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return 'input'
  return config.inputType
})
const getInputTitleByRefreshType = computed<string>(() => {
  const refreshType = props.buttonProps.button.buttonInfo.refreshType
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return "内容"
  return config.title
})
const allVariables = computed<string[]>(() => {
  if (!props.buttonProps.executeContext.executeVariable.variable) return [];
  return Object.keys(props.buttonProps.executeContext.executeVariable.variable);
});

const newVariable = ref('')

const addVariable = () => {
  if (!props.buttonProps.button.buttonInfo.refreshOfVariables) {
    props.buttonProps.button.buttonInfo.refreshOfVariables = []
  }
  if (newVariable.value && !props.buttonProps.button.buttonInfo.refreshOfVariables.includes(newVariable.value)) {
    props.buttonProps.button.buttonInfo.refreshOfVariables.push(newVariable.value)
    newVariable.value = ''
  }
}

const removeVariable = (index: number) => {
  props.buttonProps.button.buttonInfo.refreshOfVariables.splice(index, 1)
}


const refreshConfigMap = AppButtonVariableRefreshConfigMap

const handleRefresh = () => {
  const typeVariableInfo = props.buttonProps.button.buttonInfo as AppButtonInfoTypeRefreshInfo
  if (!typeVariableInfo.refreshType || typeVariableInfo.refreshType.length == 0) {
    return false
  }
  refreshConfigMap.get(typeVariableInfo.refreshType)?.refresh(props.buttonProps.executeContext, typeVariableInfo.refreshValue)
}
</script>

<template>
  <div class="form-row">
    <div class="form-group">
      <div class="form-label">变量刷新</div>
      <div class="form-input">
        <select v-model="props.buttonProps.button.buttonInfo.refreshType">
          <option value="">不刷新</option>
          <option v-for="buttonType in  buttonTypeList" :value="buttonType.key">
            {{ buttonType.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="form-group" v-if="refreshTypeSelected">
      <div class="form-label">刷新按钮</div>
      <div class="form-input">
        <select v-model="props.buttonProps.button.buttonInfo.refreshShow">
          <option value="">不展示</option>
          <option value="fixed">固定</option>
          <option value="focus">焦点</option>
        </select>
      </div>
    </div>
  </div>
  <div class="form-row" v-if="refreshTypeSelected">
    <div class="form-group">
      <div class="form-label">{{ getInputTitleByRefreshType }}</div>
      <div class="form-input" style="display: flex;flex-direction: column">
        <button @click="handleRefresh" style="width: 10em;">run</button>
        <input type="text"
               autocapitalize="off"
               autocomplete="off"
               spellcheck="false"
               v-if="getInputTypeByRefreshType == 'input'"
               v-model="props.buttonProps.button.buttonInfo.refreshValue"
        />
        <CommonSelect
            v-else-if="getInputTypeByRefreshType == 'variable'"
            :modelValue="props.buttonProps.button.buttonInfo.refreshValue"
            :options="getOptionsByRefreshType"
            :hideAdd="true"
            :hideRemove="true"
            width="14.8em"
            height="2.2em"
            @update:modelValue="(newVal:string)=>props.buttonProps.button.buttonInfo.refreshValue=newVal"
        />
        <textarea v-else
                  autocapitalize="off"
                  autocomplete="off"
                  spellcheck="false"
                  style="width: 37.3em"
                  v-model="props.buttonProps.button.buttonInfo.refreshValue"
                  rows="7"
        ></textarea>
      </div>
    </div>
  </div>
  <div class="form-row" v-if="refreshTypeSelected">
    <div class="form-group" style="align-items: flex-start">
      <div class="form-label">监听变量</div>
      <div class="form-input">
        <div style="display: flex; gap: 8px;">
          <CommonSelect
              v-model="newVariable"
              :options="allVariables"
              :hideRemove="true"
              width="14.8em"
              height="2.2em"
              @add-option="(newVal:string)=>newVariable=newVal"
          />
          <button @click="addVariable">添加</button>
        </div>
        <div style="margin-top: 8px;">
          <div v-for="(variable, index) in props.buttonProps.button.buttonInfo.refreshOfVariables" :key="variable" style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span>{{ variable }}</span>
            <button @click="removeVariable(index)">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>