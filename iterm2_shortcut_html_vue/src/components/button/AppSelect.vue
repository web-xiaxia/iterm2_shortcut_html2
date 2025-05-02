<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonEditorRefreshProps, ButtonEditorVariableProps, ButtonProps} from "@/types/AppConfig.ts";
import Select from "../common/CommonSelect.vue";
import {type AppButtonTypeSelect, GetAppVariableRef} from "@/types/AppButton.ts";
import Modal from '../common/CommonModal.vue';
import EditorOptions from "./AppEditorOptions.vue";
import AppEditorCommon from "./AppEditorCommon.vue";
import {computed, type CSSProperties, ref} from "vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";
import AppEditorVariable from "./AppEditorVariable.vue";
import AppEditorVariableRefresh from "./AppEditorVariableRefresh.vue";

const props = defineProps<ButtonProps<AppButtonTypeSelect>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}))
const editorVariableProp = computed<ButtonEditorVariableProps>(() => ({
  buttonProps: props,
}))
const editorRefreshProp = computed<ButtonEditorRefreshProps>(() => ({
  buttonProps: props,
}))
const variableInfo = GetAppVariableRef(props.button.buttonInfo, props.executeContext.executeVariable.variable)
const variableInfoValue = variableInfo.value.value
const selectClass = computed<CSSProperties>(() => {
  return {
    'edit-width-model': props.appSessionStatus.editWidth,
  }
});

const showModal = ref(false);

function handleClick() {
  if (props.appSessionStatus.editWidth) {
    return
  }
  if (props.appSessionStatus.appMode === 'settings') {
    showModal.value = true;
  }
}


</script>

<template>
  <div @click="handleClick" class="handle-click">
    <Select :options="variableInfo.variable.value.options"
            :modelValue="variableInfoValue"
            :disabled="props.appSessionStatus.appMode === 'settings'"
            :color="props.button.color"
            :width="props.button.buttonInfo.width > 0 ? props.button.buttonInfo.width +'em': undefined"
            :bindClass="selectClass"
            @mouseenter="handleMouseenterEditWidth($event,props)"
            @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
            @addOption="(add:string) => variableInfo.variable.value.options.push(add)"
            @removeOption="(delValue:string) => variableInfo.variable.value.options = variableInfo.variable.value.options.filter((v) => v !== delValue)"
            @update:modelValue="(v) => variableInfoValue = v"
    />
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑下拉选择框"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
    <AppEditorVariable v-bind="editorVariableProp"/>
    <EditorOptions
        :variableInfo="variableInfo"
        :variableName="props.button.buttonInfo.variableName"
    />
    <AppEditorVariableRefresh v-bind="editorRefreshProp"/>
  </Modal>
</template>

<style scoped>

</style>