<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonProps} from "@/types/AppConfig.ts";
import type {AppButtonTypeBlank} from "@/types/AppButton.ts";
import {computed, type CSSProperties, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";

const props = defineProps<ButtonProps<AppButtonTypeBlank>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}));

const buttonStyle = computed<CSSProperties>(() => {
  return {
    width: props.button.buttonInfo.width + 'em',
    borderTop: props.appSessionStatus.appMode == 'settings' ? '1px dashed rgb(99 148 189)' : undefined,
    borderBottom: props.appSessionStatus.appMode == 'settings' ? '1px dashed rgb(99 148 189)' : undefined,
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
  <div :class="{'edit-width-model':props.appSessionStatus.editWidth}"
       @mouseenter="handleMouseenterEditWidth($event, props)"
       @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
       :style="buttonStyle"
       @click="handleClick"
       class="button-box handle-click"
  >
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑间隔"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
  </Modal>
</template>

<style scoped>
.button-box {
  height: 0.5em;
  display: inline-block;
}
</style>