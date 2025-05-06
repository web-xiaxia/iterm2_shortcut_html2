<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonEditorRefreshProps, ButtonEditorVariableProps, ButtonProps} from "@/types/AppConfig.ts";
import {type AppButtonTypeInput, GetAppVariableRef} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";
import AppEditorVariable from "./AppEditorVariable.vue";
import AppEditorVariableRefresh from "./AppEditorVariableRefresh.vue";

const props = defineProps<ButtonProps<AppButtonTypeInput>>();
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
const variableInfoNumberValue = computed({
  get: () => {
    if (!variableInfoValue.value) {
      return ""
    }
    return parseFloat(variableInfoValue.value)
  },
  set: (val: number) => {
    variableInfoValue.value = "" + val
  }
})
const buttonStyle = computed<CSSProperties>(() => {
  return {
    borderColor: props.button.color,
    color: props.button.color,
    width: props.button.buttonInfo.width > 0 ? props.button.buttonInfo.width + "em" : undefined,
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
  <div class="input-box handle-click" @click="handleClick">
    <input v-if="props.button.buttonInfo.showType =='number'"
        :class="{'edit-width-model':props.appSessionStatus.editWidth}"
           @mouseenter="handleMouseenterEditWidth($event,props)"
           @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
           :readonly="props.appSessionStatus.editWidth"
           :style="buttonStyle"
           type="number"
           autocapitalize="off"
           autocomplete="off"
           spellcheck="false"
           v-model="variableInfoNumberValue"
    />
    <input v-else
           :class="{'edit-width-model':props.appSessionStatus.editWidth}"
           @mouseenter="handleMouseenterEditWidth($event,props)"
           @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
           :readonly="props.appSessionStatus.editWidth"
           :style="buttonStyle"
           type="text"
           autocapitalize="off"
           autocomplete="off"
           spellcheck="false"
           v-model="variableInfoValue"
    />
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑输入框"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">类型</div>
        <div class="form-input" style="display: flex">
          <select v-model="props.button.buttonInfo.showType">
            <option value="">文本</option>
            <option value="number">数字</option>
          </select>
        </div>
      </div>
    </div>
    <AppEditorVariable v-bind="editorVariableProp"/>
    <AppEditorVariableRefresh v-bind="editorRefreshProp"/>
  </Modal>
</template>

<style scoped>
.input-box {
  align-items: center;
  display: flex;
}
</style>