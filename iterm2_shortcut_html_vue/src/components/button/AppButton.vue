<script setup lang="ts">
import {ButtonEditorButtonTypeProps, ButtonEditorCommonProps, ButtonProps} from "@/types/AppConfig.ts";
import {type AppButtonTypeButton} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";
import {AppButtonTypeButtonTypeList, AppButtonTypeButtonTypeMap} from "../AppButtonTypeButtonTypeConfig.ts";
import CommonSelect from "../common/CommonSelect.vue";
import AppEditorButtonType from "@/components/button/AppEditorButtonType.vue";

const props = defineProps<ButtonProps<AppButtonTypeButton>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}))
const editorButtonTypeProp = computed<ButtonEditorButtonTypeProps>(() => ({
  buttonProps: props,
}))

const buttonStyle = computed<CSSProperties>(() => {
  return {
    color: props.button.color,
    borderColor: props.button.color,
    width: props.button.buttonInfo.width > 0 ? props.button.buttonInfo.width + "em" : undefined,
  }
});


const buttonTypeTitleMap = AppButtonTypeButtonTypeMap;

const showModal = ref(false);

function handleClick() {
  if (props.appSessionStatus.editWidth) {
    return
  }
  if (props.appSessionStatus.appMode === 'settings') {
    showModal.value = true;
    return
  }
  const buttonType = buttonTypeTitleMap.get(props.button.buttonInfo.type);
  if (buttonType) {
    buttonType.send(props.executeContext,props.button.buttonInfo.value)
  }
}

</script>

<template>
  <button :class="{'edit-width-model':props.appSessionStatus.editWidth}"
          @mouseenter="handleMouseenterEditWidth($event,props)"
          @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
          :style="buttonStyle"
          @click="handleClick"
          class="handle-click"
  >
    {{ props.button.buttonInfo.title }}
  </button>

  <Modal
      v-model:visible="showModal"
      title="编辑按钮"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">标题</div>
        <div class="form-input">
          <input v-model="props.button.buttonInfo.title" autocapitalize="off" type="text"/>
        </div>
      </div>
    </div>
    <AppEditorButtonType v-bind="editorButtonTypeProp"/>
  </Modal>
</template>

<style scoped>
</style>