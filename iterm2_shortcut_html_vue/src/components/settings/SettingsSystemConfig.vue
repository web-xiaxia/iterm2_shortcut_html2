<script setup lang="ts">

import {onMounted, ref, watch} from "vue";
import {getInitSettingsSystemConfig, getSystemConfig, saveSystemConfig, type SettingsSystemConfig} from "@/api/config.ts";
import {debounce} from "lodash";


const systemConfig = ref<SettingsSystemConfig>(getInitSettingsSystemConfig());
onMounted(() => {
  systemConfig.value = getSystemConfig()
})
const debounceSaveSystemConfig=debounce(saveSystemConfig,900)
watch(systemConfig, (newVal) => {
  if (newVal) {
    debounceSaveSystemConfig(newVal)
  }
},{deep:true})
</script>

<template>
  <div class="form">
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">宽度</div>
        <div class="form-input">
          <input type="number" v-model="systemConfig.window_width">
        </div>
      </div>
      <div class="form-group">
        <div class="form-label">高度</div>
        <div class="form-input">
          <input type="number" v-model="systemConfig.window_height">
        </div>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">shell pre</div>
        <div class="form-input" style="flex: 1">
          <textarea v-model="systemConfig.shell" style="width: 37.4em" rows="6"></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.form-group{
  flex-direction: row;
}
.form{
  display: flex;
  flex-direction: column;
}
</style>