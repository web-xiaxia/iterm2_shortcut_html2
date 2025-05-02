<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonProps} from "@/types/AppConfig.ts";
import type {AppButtonTypeLine} from "@/types/AppButton.ts";
import {computed, type CSSProperties, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";

const props = defineProps<ButtonProps<AppButtonTypeLine>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}));

const buttonStyle = computed<CSSProperties>(() => {
  return {
    height: props.button.buttonInfo.width + 'em',
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
  <div class="button-box handle-click"
       :style="buttonStyle"
       :class="{
         'settings-model':props.appSessionStatus.appMode == 'settings',
         'edit-width-model':props.appSessionStatus.editWidth,
       }"
       @mouseenter="handleMouseenterEditWidth($event, props)"
       @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
       @click="handleClick"
  >
    <span v-if="props.appSessionStatus.appMode == 'settings'" class="button-box-edit-span"></span>
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑换行"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
  </Modal>
</template>

<style scoped>
.button-box {
  box-sizing: border-box;
  margin: 0 !important;
  width: 100%;
}

.settings-model {
  background-color: #6164642b;
}

.button-box-edit-span {
  position: absolute;
  right: 0;
  margin: 0 !important;
  border: 1px dashed white;
  font-size: 8px;
  cursor: pointer;
  width: 8px;
  height: 8px;
  display: inline-block;
}
</style>