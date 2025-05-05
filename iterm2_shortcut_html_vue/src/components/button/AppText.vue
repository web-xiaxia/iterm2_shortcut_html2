<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonProps} from "@/types/AppConfig.ts";
import type {AppButtonTypeText} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";

const props = defineProps<ButtonProps<AppButtonTypeText>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
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
    {{ props.button.buttonInfo.text }}
    <label v-if="!props.button.buttonInfo.text || props.button.buttonInfo.text.length == 0">无值</label>
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑文本"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">文本内容</div>
        <div class="form-input">
          <input v-model="props.button.buttonInfo.text"
                 autocapitalize="off"
                 autocomplete="off"
                 spellcheck="false"
                 type="text"
          />
        </div>
      </div>
    </div>
  </Modal>
</template>

<style scoped>

</style>