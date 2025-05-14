<script setup lang="ts">

import type {AppConfig} from "@/types/AppConfig.ts";

const props = defineProps<{
  appConfig: AppConfig
}>();

</script>

<template>
  <div class="form">
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">shell pre</div>
        <div class="form-input" style="flex: 1">
          <textarea v-model="props.appConfig.exec_config.shell" style="width: 37.4em" rows="6"></textarea>
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