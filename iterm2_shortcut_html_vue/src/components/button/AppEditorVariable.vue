<script setup lang="ts">
import type {ButtonEditorVariableProps} from "@/types/AppConfig.ts";
import {computed} from "vue";
import CommonSelect from "../common/CommonSelect.vue";

const props = defineProps<ButtonEditorVariableProps>();

const appVariableSelectOptions = computed<string[]>(() => {
  return Object.keys(props.buttonProps.executeContext.executeVariable.variable)
})

</script>

<template>
  <div class="form-row">
    <div class="form-group">
      <div class="form-label">变量名</div>
      <div class="form-input" style="display: flex">
        <!--        <input v-model="props.buttonProps.button.buttonInfo.variableName" type="text"/>-->
        <CommonSelect
            :modelValue="props.buttonProps.button.buttonInfo.variableName"
            :options="appVariableSelectOptions"
            :hideAdd="true"
            :hideRemove="true"
            width="14.8em"
            height="2.2em"
            @update:modelValue="(newVal:string)=>props.buttonProps.button.buttonInfo.variableName=newVal"
        />
      </div>
    </div>
    <div class="form-group" v-if="props.buttonProps.editConfig.historyVariableValue">
      <div class="form-label">历史记录</div>
      <div class="form-input" style="display: flex">
        <select v-model="props.buttonProps.button.buttonInfo.historyVariableValue">
          <option>不记录</option>
          <option>记录</option>
        </select>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>