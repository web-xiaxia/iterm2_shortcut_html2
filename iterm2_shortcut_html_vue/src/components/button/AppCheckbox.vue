<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonEditorRefreshProps, ButtonEditorVariableProps, ButtonProps} from "@/types/AppConfig.ts";
import {type AppButtonTypeCheckbox, GetAppVariableRef} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import EditorOptions from "./AppEditorOptions.vue";
import AppEditorCommon from "./AppEditorCommon.vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";
import AppEditorVariable from "./AppEditorVariable.vue";
import AppEditorVariableRefresh from "./AppEditorVariableRefresh.vue";

const props = defineProps<ButtonProps<AppButtonTypeCheckbox>>();
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

const buttonStyle = computed<CSSProperties>(() => {
  return {
    color: props.button.color,
  }
});

const labelStyle = computed<CSSProperties>(() => {
  return {
    maxWidth: props.button.buttonInfo.width > 0 ? props.button.buttonInfo.width + "em" : undefined,
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

function handleLabelClick(e: MouseEvent) {
  if (props.appSessionStatus.editWidth) {
    e.preventDefault()
    return;
  }
}

</script>

<template>
  <div @click="handleClick" :style="buttonStyle" class="button-box handle-click">
    <label class="button-label" v-for="v in variableInfo.variable.value.options" :key="v"
           @click="handleLabelClick"
           :style="labelStyle"
           :class="{'edit-width-model':props.appSessionStatus.editWidth}"
           @mouseenter="handleMouseenterEditWidth($event,props)"
           @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
    >
      <div style="display: flex;align-items: center">
        <input type="checkbox" :value="v" v-model="variableInfo.variable.value.values">
        {{ v }}
      </div>
    </label>
    <label v-if="!variableInfo.variable.value.options || variableInfo.variable.value.options.length == 0">无值</label>
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑复选框"
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
.button-box {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.button-label {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>