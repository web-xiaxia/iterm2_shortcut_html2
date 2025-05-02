<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonEditorRefreshProps, ButtonEditorVariableProps, ButtonProps} from "@/types/AppConfig.ts";
import {type AppButtonTypeVariableText, GetAppVariableRef} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";
import AppEditorVariable from "./AppEditorVariable.vue";
import AppEditorVariableRefresh from "./AppEditorVariableRefresh.vue";

const props = defineProps<ButtonProps<AppButtonTypeVariableText>>();
const variableInfo = GetAppVariableRef(props.button.buttonInfo, props.executeContext.executeVariable.variable)
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}))
const editorVariableProp = computed<ButtonEditorVariableProps>(() => ({
  buttonProps: props,
}))
const editorRefreshProp = computed<ButtonEditorRefreshProps>(() => ({
  buttonProps: props,
}))
const buttonStyle = computed<CSSProperties>(() => {
  return {
    color: props.button.color,
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
  <div @click="handleClick" :style="buttonStyle" class="handle-click">
    {{ variableInfo.value }}
    <label v-if="!variableInfo.value.value || variableInfo.value.value?.length == 0">无值</label>
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑变量文本"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
    <AppEditorVariable v-bind="editorVariableProp"/>
    <AppEditorVariableRefresh v-bind="editorRefreshProp"/>
  </Modal>
</template>

<style scoped>

</style>