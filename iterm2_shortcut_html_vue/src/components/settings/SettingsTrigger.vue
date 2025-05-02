<script setup lang="ts">
import type {AppConfig} from "@/types/AppConfig.ts";

const props = defineProps<{
  appConfig: AppConfig
}>();
</script>

<template>
  <div class="config-container">
    <h3>触发器设置</h3>
    <p>在这里管理触发器配置</p>
  </div>
</template> 