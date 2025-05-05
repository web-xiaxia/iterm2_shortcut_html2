<script setup lang="ts">

import {type AppButtonInfoTypeWidth, GetColorList} from "@/types/AppButton.ts";
import type {ButtonEditorCommonProps} from "@/types/AppConfig.ts";
import {computed, type CSSProperties} from "vue";

const props = defineProps<ButtonEditorCommonProps>();
const colorSelectStyle = computed<CSSProperties>(() => {
  return {
    color: props.buttonProps.button.color,
    borderColor: props.buttonProps.button.color,
  }
});
</script>

<template>
  <div class="form-row">
    <div class="form-group half">
      <div class="form-label">变量联动</div>
      <div class="form-input">
        <input v-model="props.buttonProps.button.linkage" autocapitalize="off" type="text"/>
      </div>
    </div>
    <div class="form-group half">
      <div class="form-label">联动类型</div>
      <div class="form-input">
        <select v-model="props.buttonProps.button.linkage_type">
          <option value="value_true">有值时显示</option>
          <option value="value_false">无值时显示</option>
        </select>
      </div>
    </div>
  </div>
  <div class="form-row" v-if="!props.buttonProps.editConfig.notMargin">
    <div class="form-group half">
      <div class="form-label">前间距</div>
      <div class="form-input">
        <input v-model="props.buttonProps.button.beforeMargin" type="number"/>
      </div>
    </div>
    <div class="form-group half">
      <div class="form-label">后间距</div>
      <div class="form-input">
        <input v-model="props.buttonProps.button.afterMargin" type="number"/>
      </div>
    </div>
  </div>
  <div class="form-row">
    <div class="form-group half" v-if="!props.buttonProps.editConfig.disableColor">
      <div class="form-label">颜色</div>
      <div class="form-input">
        <select :style="colorSelectStyle" v-model="props.buttonProps.button.color">
          <option :value="v" v-for="v in GetColorList()" :key="v">{{ v }}</option>
        </select>
      </div>
    </div>
    <div class="form-group half" v-if="props.buttonProps.editConfig.width">
      <div class="form-label">{{ props.buttonProps.editConfig.widthTitle || '宽度' }}</div>
      <div class="form-input">
        <input v-model="(props.buttonProps.button.buttonInfo as AppButtonInfoTypeWidth).width" step="0.1" type="number"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>