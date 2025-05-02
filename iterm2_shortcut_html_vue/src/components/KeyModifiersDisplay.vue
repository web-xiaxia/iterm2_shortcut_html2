<script setup lang="ts">
import {onMounted, onUnmounted, computed} from 'vue'
import {AppExecuteContext} from "@/types/AppConfig.ts";

const props = defineProps<{
  executeContext: AppExecuteContext
}>()

const activeKeys = computed(() => {
  return [
    {key: props.executeContext.keyboard.command, name: 'command'},
    {key: props.executeContext.keyboard.control, name: 'control'},
    {key: props.executeContext.keyboard.shift, name: 'shift'},
    {key: props.executeContext.keyboard.option, name: 'option'},
  ].filter(k => k.key).map(k => k.name)
})

const displayText = computed(() => {
  return activeKeys.value.join(' + ')
})

const handleKey = (e: KeyboardEvent) => {
  props.executeContext.keyboard.command = e.metaKey
  props.executeContext.keyboard.shift = e.shiftKey
  props.executeContext.keyboard.option = e.altKey
  props.executeContext.keyboard.control = e.ctrlKey
  props.executeContext.keyboard.code = e.code
  props.executeContext.keyboard.key = e.key
}

onMounted(() => {
  window.addEventListener('keydown', handleKey)
  window.addEventListener('keyup', handleKey)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKey)
  window.removeEventListener('keyup', handleKey)
})
</script>

<template>
  <div class="key-status" v-if="activeKeys.length > 0">
    {{ displayText }}
  </div>
</template>

<style scoped>
.key-status {
  position: fixed;
  bottom: 0;
  left: 0;
  padding: 1px 4px;
  margin: 0 0 4px 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  color: #666;
  font-family: monospace;
  font-size: 10px;
  opacity: 0.9;
  transition: all 0.2s;
  z-index: 999;
}

</style>