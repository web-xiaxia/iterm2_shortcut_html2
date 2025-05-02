<script setup lang="ts">
import {onMounted, onUnmounted, ref, useTemplateRef, watch} from 'vue'
import {AppExecuteContext, AppSessionStatus, AppStatus} from "@/types/AppConfig.ts";

const props = defineProps<{
  appStatus: AppStatus,
  appSessionStatus: AppSessionStatus,
  executeContext: AppExecuteContext
}>()

// 新增ESC监听逻辑
// 新增双击Shift检测逻辑
const lastShiftTime = ref(0)

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    props.appSessionStatus.showFullScreenInputModal = false
  }
  if (e.key === 'Shift') {
    const now = Date.now()
    if (now - lastShiftTime.value < 300) {
      props.appSessionStatus.showFullScreenInputModal = true
      lastShiftTime.value = 0
    } else {
      lastShiftTime.value = now
    }
  }
  if (props.appSessionStatus.showFullScreenInputModal) {
    if (props.appSessionStatus.fullScreenInputValue) {
      if (e.key === 'Enter') {
        if (!props.appStatus.fullScreenInputTypeTextarea|| e.metaKey) {
          props.executeContext.execute.sendText(props.appSessionStatus.fullScreenInputValue)
          props.appSessionStatus.fullScreenInputValue = ""
        }
      }
    }
  }
}

// 新增背景点击逻辑
const handleBackgroundClick = () => {
  props.appSessionStatus.showFullScreenInputModal = false
}

const fullScreenInput = useTemplateRef("fullScreenInput")
const fullScreenTextarea = useTemplateRef("fullScreenTextarea")
watch(() => props.appSessionStatus.showFullScreenInputModal, (value) => {
  if (value) {
    setTimeout(() => {
      if (props.appStatus.fullScreenInputTypeTextarea) {
        fullScreenTextarea.value?.focus()
      } else {
        fullScreenInput.value?.focus()
      }
    }, 100)
  }
})
onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div v-if="props.appSessionStatus.showFullScreenInputModal" class="fullscreen-modal" @click="handleBackgroundClick">
    <div class="modal-content">
      <div class="modal-body-padding"></div>
      <div class="modal-body" @click.stop="">
        <div>
          <button class="button-type-text" @click="props.appStatus.fullScreenInputTypeTextarea=!props.appStatus.fullScreenInputTypeTextarea">{{ props.appStatus.fullScreenInputTypeTextarea ? '切换单行':'切换多行' }}</button>
        </div>
        <textarea
            v-if="props.appStatus.fullScreenInputTypeTextarea"
            ref="fullScreenTextarea"
            v-model="props.appSessionStatus.fullScreenInputValue"
            class="center-input"
            placeholder="请输入内容"
            rows="8"
        ></textarea>
        <input v-else ref="fullScreenInput"
               v-model="props.appSessionStatus.fullScreenInputValue"
               class="center-input"
               placeholder="请输入内容"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.fullscreen-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  z-index: 999;
}

.modal-content {
  border-radius: 8px;
  width: 80%;
  max-width: 800px;

}

.modal-body-padding {
  height: 20vh;
  max-height: 90px;
}

.center-input {
  width: 100%;
  padding: 6px 6px;
  border-radius: 4px;
  background-color: rgb(38, 37, 37);
  border: 1px dashed white;
}
</style>