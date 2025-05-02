<script setup lang="ts">
import type {AppSessionStatus} from "../types/AppConfig.ts";
import {ref, watch} from "vue";

const props = defineProps<{
  appSessionStatus: AppSessionStatus,
}>()
const widthEditTitle = ref<string>("鼠标移动到灰色背景区域")
watch(props.appSessionStatus, (newVal: AppSessionStatus) => {
  if (newVal.editWidthNow) {
    const nowWidth = newVal.editWidthNow.width.value || 0
    if (nowWidth <= 0) {
      widthEditTitle.value = `按Q/W键进行调节：当前未设置`
      return;
    }
    widthEditTitle.value = `按Q/W键进行调节：${nowWidth.toFixed(1)}em, 按R键重置`
    return
  }
  widthEditTitle.value = "鼠标移动到灰色背景区域"
}, {deep: true});
</script>

<template>
  <div class="drag-width-tip-box-main">
    <div class="drag-width-tip-box">{{ widthEditTitle }}</div>
  </div>
</template>

<style scoped>
.drag-width-tip-box-main {
  display: flex;
  position: fixed;
  top: 0;
  width: 100vw;
  z-index: 66;
  pointer-events: none;
  justify-content: center;
}

.drag-width-tip-box {
  padding: 6px;
  color: white;
  width: 40%;
  font-size: 12px;
  border-radius: 0 0 10px 10px;
  background-color: rgba(107, 196, 108, 0.76);
  text-align: center;
}
</style>