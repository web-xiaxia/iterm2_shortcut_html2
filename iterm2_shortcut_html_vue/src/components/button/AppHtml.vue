<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonProps} from "@/types/AppConfig.ts";
import type {AppButtonTypeHtml} from "@/types/AppButton.ts";
import Modal from '../common/CommonModal.vue';
import {computed, ref} from "vue";
import AppEditorCommon from "./AppEditorCommon.vue";

const props = defineProps<ButtonProps<AppButtonTypeHtml>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}))

const showModal = ref<boolean>(false);

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
  <div style="display: block"
       @click="handleClick"
       class="handle-click"
  >
    <div v-html="props.button.buttonInfo.html"></div>
    <label v-if="!props.button.buttonInfo.html || props.button.buttonInfo.html.length == 0">无值</label>
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑Html"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>

    <div class="form-row">
      <div class="form-group" style="width: 42.3em;">
        <div class="form-label">Html内容</div>
        <div class="form-input">
          <textarea autocapitalize="off"
                    autocomplete="off"
                    spellcheck="false"
                    style="width: 100%"
                    v-model="props.button.buttonInfo.html"
                    rows="5"
          ></textarea>
        </div>
      </div>
    </div>
  </Modal>
</template>

<style scoped>
</style>