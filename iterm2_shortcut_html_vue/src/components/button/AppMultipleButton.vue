<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonEditorVariableProps, ButtonProps} from "@/types/AppConfig.ts";
import {type AppButtonTypeMultipleButton, GetAppVariableRef} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";
import {AppButtonTypeButtonTypeList, AppButtonTypeButtonTypeMap} from "../AppButtonTypeButtonTypeConfig.ts";
import CommonSelect from "../common/CommonSelect.vue";
import AppEditorVariable from "./AppEditorVariable.vue";

const props = defineProps<ButtonProps<AppButtonTypeMultipleButton>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}))
const editorVariableProp = computed<ButtonEditorVariableProps>(() => ({
  buttonProps: props,
}))

const variableInfo = GetAppVariableRef(props.button.buttonInfo, props.executeContext.executeVariable.variable)

const buttonStyle = computed<CSSProperties>(() => {
  return {
    color: props.button.color,
    borderColor: props.button.color,
    width: props.button.buttonInfo.width > 0 ? props.button.buttonInfo.width + "em" : undefined,
  }
});

const buttonTypeList = AppButtonTypeButtonTypeList;
const buttonTypeTitleMap = AppButtonTypeButtonTypeMap;


const getOptionsByType = computed<string[]>(() => {
  const refreshType = props.button.buttonInfo.type
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return []
  return config.getOptions(props.executeContext.executeVariable)
})
const getInputTypeByType = computed<"input" | "textarea" | "variable">(() => {
  const refreshType = props.button.buttonInfo.type
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return "input"
  return config.inputType
})
const getInputTitleByType = computed<string>(() => {
  const refreshType = props.button.buttonInfo.type
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return "内容"
  return config.title
})

const showModal = ref(false);

function handleClickSettings() {
  if (props.appSessionStatus.appMode === 'settings') {
    showModal.value = true;
    return
  }
}

function handleClick(v: string) {
  if (props.appSessionStatus.editWidth) {
    return
  }
  variableInfo.value.value.value = v
  const buttonType = buttonTypeTitleMap.get(props.button.buttonInfo.type);
  if (buttonType) {
    let sendValue = props.button.buttonInfo.value
    if (buttonType.inputType != 'variable') {
      sendValue = sendValue.replaceAll("{{value}}", v)
    }
    buttonType.send(props.executeContext, sendValue)
  }
}

</script>

<template>
  <div @click="handleClickSettings" class="handle-click">
    <button v-for="v in variableInfo.variable.value.options" :class="{'edit-width-model':props.appSessionStatus.editWidth}"
            @mouseenter="handleMouseenterEditWidth($event,props)"
            @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
            :style="buttonStyle"
            @click="handleClick(v)"
    >
      {{ v }}
    </button>
    <label v-if="variableInfo.variable.value.options.length==0">无值</label>
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑动态按钮"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
    <AppEditorVariable v-bind="editorVariableProp"/>
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">按钮类型</div>
        <div class="form-input">
          <select v-model="props.button.buttonInfo.type">
            <option v-for="buttonType in  buttonTypeList" :value="buttonType.key">
              {{ buttonType.name }}
            </option>
          </select>
        </div>
      </div>
      <div style="display: flex; align-items: center;" v-pre>
        文本类型内容{{value}}替换为当前选中内容
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">{{ getInputTitleByType }}</div>
        <div class="form-input" style="">
          <input v-if="getInputTypeByType == 'input'" v-model="props.button.buttonInfo.value">
          <CommonSelect
              v-else-if="getInputTypeByType == 'variable'"
              :modelValue="props.button.buttonInfo.value"
              :options="getOptionsByType"
              :hideAdd="true"
              :hideRemove="true"
              width="14.8em"
              height="2.2em"
              @update:modelValue="(newVal:string)=>props.button.buttonInfo.value=newVal"
          />
          <textarea style="width: 37.3em" v-else v-model="props.button.buttonInfo.value" rows="7"></textarea>
        </div>
      </div>
    </div>

  </Modal>
</template>

<style scoped>
</style>