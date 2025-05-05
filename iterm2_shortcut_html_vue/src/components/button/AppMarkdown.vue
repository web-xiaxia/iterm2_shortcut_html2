<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonProps} from "@/types/AppConfig.ts";
import Markdown from "../common/CommonMarkdown.vue";
import type {AppButtonTypeMarkdown} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";

const props = defineProps<ButtonProps<AppButtonTypeMarkdown>>();
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
  <div style="display: block" :style="buttonStyle"
       @click="handleClick" class="handle-click">
    <Markdown :content="props.button.buttonInfo.markdown||''"/>
    <label v-if="!props.button.buttonInfo.markdown || props.button.buttonInfo.markdown.length == 0">无值</label>
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑Markdown"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
    <div class="form-row">
      <div class="form-group" style="width: 42.3em;">
        <div class="form-label">Markdown</div>
        <div class="form-input">
          <textarea autocapitalize="off" style="width: 100%" v-model="props.button.buttonInfo.markdown" rows="5"></textarea>
        </div>
      </div>
    </div>
  </Modal>
</template>

<style scoped>
</style>