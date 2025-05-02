<script setup lang="ts">
const props = defineProps<{
  visible: boolean;
  title?: string;
}>();

const emit = defineEmits(['update:visible']);

function closeModal() {
  emit('update:visible', false);
}

</script>

<template>
  <div class="modal">
    <div v-if="props.visible" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ props.title || '编辑' }}</h3>
          <button @click="closeModal" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 0;
  pointer-events: auto;
}

.modal-content {
  position: absolute;
  top: 2rem;
  left: 5rem;
  right: 5rem;
  bottom: 2rem;
  background-color: #222;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  color: #eee;
  pointer-events: auto;
  display: flex;
  flex-direction: column;
}

/* 防止模态框背景透明部分透传鼠标事件 */
body:has(.modal-overlay) {
  pointer-events: none;
}

.modal-overlay,
.modal-overlay * {
  pointer-events: auto;
}

@media (max-width: 768px) {
  .modal-content {
    left: 3rem;
    right: 3rem;
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .modal-content {
    left: 1rem;
    right: 1rem;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 8px;
  border-bottom: 1px solid #444;
  width: 100%;
  box-sizing: border-box;
}

.modal-header h3 {
  margin: 0;
  font-size: 0.9rem;
}

.close-btn {
  width: 24px;
  height: 24px;
  border-radius: 50% !important;
  font-size: 18px;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  border: none;
  transition: background-color 0.2s, transform 0.2s;
}

.close-btn:hover {
  background-color: #444 !important;
  transform: scale(1.1);
}

.modal-body {
  padding: 6px 8px;
  overflow-y: auto;
  gap: 6px;
  width: 100%;
  box-sizing: border-box;
  overflow-x: auto;
  flex: 1;
}

.modal-body :deep(*) {
  max-width: 100%;
  box-sizing: border-box;
}

.modal-body :deep(img),
.modal-body :deep(video),
.modal-body :deep(table),
.modal-body :deep(pre),
.modal-body :deep(iframe) {
  max-width: 100%;
  width: auto;
  height: auto;
}

.modal-body :deep(.form-row) {

  gap: 8px;
  width: 100%;
}

/* 表单元素样式 */
.modal-body :deep(input),
.modal-body :deep(textarea),
.modal-body :deep(select) {
  color: #eee;
  border-radius: 3px;
  padding: 5px 8px;
  width: 13rem;
  font-size: 0.85rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.modal-body :deep(input:focus),
.modal-body :deep(textarea:focus),
.modal-body :deep(label) {
  color: #ccc;
  font-size: 0.85rem;
}

.modal-body :deep(input[type="checkbox"]),
.modal-body :deep(input[type="radio"]) {
  width: auto;
  margin-right: 8px;
}

.modal-body :deep(.checkbox-label),
.modal-body :deep(.radio-label) {
  cursor: pointer;
}

/* 全局按钮颜色重置，确保颜色不丢失 */
button {
  background-color: #333 !important;
  color: #eee !important;
}

button.primary {
  background-color: #2a5885 !important;
  color: white !important;
}

</style> 