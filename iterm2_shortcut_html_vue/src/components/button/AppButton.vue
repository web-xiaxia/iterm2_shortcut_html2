<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonProps} from "@/types/AppConfig.ts";
import {type AppButtonTypeButton} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";
import {AppButtonTypeButtonTypeList, AppButtonTypeButtonTypeMap} from "../AppButtonTypeButtonTypeConfig.ts";
import CommonSelect from "../common/CommonSelect.vue";

const props = defineProps<ButtonProps<AppButtonTypeButton>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}))

const buttonStyle = computed<CSSProperties>(() => {
  return {
    color: props.button.color,
    borderColor: props.button.color,
    width: props.button.buttonInfo.width > 0 ? props.button.buttonInfo.width + "em" : undefined,
  }
});

const buttonTypeList = AppButtonTypeButtonTypeList;
const buttonTypeTitleMap = AppButtonTypeButtonTypeMap;


const getOptionsByType = computed<string[]>(() => {
  const refreshType = props.button.buttonInfo.type
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return []
  return config.getOptions(props.executeContext.executeVariable)
})
const getInputTypeByType = computed< "input" | "textarea" | "variable">(() => {
  const refreshType = props.button.buttonInfo.type
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return 'input'
  return config.inputType
})
const getInputTitleByType = computed<string>(() => {
  const refreshType = props.button.buttonInfo.type
  const config = buttonTypeTitleMap.get(refreshType)
  if (!config) return "内容"
  return config.title
})

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
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">按钮类型</div>
        <div class="form-input">
          <select v-model="props.button.buttonInfo.type">
            <option v-for="buttonType in  buttonTypeList" :value="buttonType.key">
              {{ buttonType.name }}
            </option>
          </select>
        </div>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">{{ getInputTitleByType }}</div>
        <div class="form-input" style="">
          <input v-if="getInputTypeByType=='input'" v-model="props.button.buttonInfo.value">
          <CommonSelect
              v-else-if="getInputTypeByType=='variable'"
              :modelValue="props.button.buttonInfo.value"
              :options="getOptionsByType"
              :hideAdd="true"
              :hideRemove="true"
              width="14.8em"
              height="2.2em"
              @update:modelValue="(newVal:string)=>props.button.buttonInfo.value=newVal"
          />
          <textarea style="width: 37.3em" v-else v-model="props.button.buttonInfo.value" rows="7"></textarea>
        </div>
      </div>
    </div>
  </Modal>
</template>

<style scoped>
</style>