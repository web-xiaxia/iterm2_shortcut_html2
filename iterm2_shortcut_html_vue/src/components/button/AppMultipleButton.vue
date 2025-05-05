<script setup lang="ts">
import {ButtonEditorButtonTypeProps, ButtonEditorCommonProps, ButtonEditorVariableProps, ButtonProps} from "@/types/AppConfig.ts";
import {type AppButtonTypeMultipleButton, GetAppVariableRef} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";
import {AppButtonTypeButtonTypeList, AppButtonTypeButtonTypeMap} from "../AppButtonTypeButtonTypeConfig.ts";
import CommonSelect from "../common/CommonSelect.vue";
import AppEditorVariable from "./AppEditorVariable.vue";
import AppEditorVariableRefresh from "@/components/button/AppEditorVariableRefresh.vue";
import type {ButtonEditorRefreshProps} from "@/types/AppConfig.ts";
import AppEditorButtonType from "@/components/button/AppEditorButtonType.vue";

const props = defineProps<ButtonProps<AppButtonTypeMultipleButton>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}))
const editorVariableProp = computed<ButtonEditorVariableProps>(() => ({
  buttonProps: props,
}))
const editorRefreshProp = computed<ButtonEditorRefreshProps>(() => ({
  buttonProps: props,
}))
const editorButtonTypeProp = computed<ButtonEditorButtonTypeProps>(() => ({
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

const buttonTypeTitleMap = AppButtonTypeButtonTypeMap;

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
    <AppEditorVariableRefresh v-bind="editorRefreshProp"/>
    <AppEditorButtonType v-bind="editorButtonTypeProp">
      <template #type-remarks>
        <div style="display: flex; align-items: center;" v-pre>
          文本类型内容{{value}}替换为当前选中内容
        </div>
      </template>
    </AppEditorButtonType>

  </Modal>
</template>

<style scoped>
</style>