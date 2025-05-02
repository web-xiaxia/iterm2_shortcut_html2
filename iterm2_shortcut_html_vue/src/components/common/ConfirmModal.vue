<script setup lang="ts">
const props = defineProps<{
  visible: boolean;
  title?: string;
  message?: string;
  confirmText?: string;
  cancelText?: string;
}>();

const emit = defineEmits(['update:visible', 'confirm', 'cancel']);

function closeModal() {
  emit('update:visible', false);
}

function handleConfirm() {
  emit('confirm');
  closeModal();
}

function handleCancel() {
  emit('cancel');
  closeModal();
}
</script>

<template>
  <div class="modal">
    <div v-if="props.visible" class="confirm-modal-overlay" @click.self="closeModal">
      <div class="confirm-modal-content">
        <div class="confirm-modal-header">
          <h3>{{ props.title || '确认' }}</h3>
          <button @click="closeModal" class="close-btn">×</button>
        </div>
        <div class="confirm-modal-body">
          <p class="confirm-message">{{ props.message || '确定要执行此操作吗？' }}</p>
          <div class="confirm-buttons">
            <button class="cancel-btn" @click="handleCancel">{{ props.cancelText || '取消' }}</button>
            <button class="confirm-btn" @click="handleConfirm">{{ props.confirmText || '确定' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.confirm-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.confirm-modal-content {
  background-color: #222;
  border-radius: 4px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  color: #eee;
}

.confirm-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid #444;
}

.confirm-modal-header h3 {
  margin: 0;
  font-size: 16px;
}

.close-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 18px;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  border: none;
  background-color: transparent;
  color: #eee;
  transition: background-color 0.2s, transform 0.2s;
}

.close-btn:hover {
  background-color: #444;
  transform: scale(1.1);
}

.confirm-modal-body {
  padding: 15px;
}

.confirm-message {
  margin-bottom: 20px;
  text-align: center;
}

.confirm-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.cancel-btn, .confirm-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.cancel-btn {
  background-color: #555 !important;
  color: #eee !important;
}

.confirm-btn {
  background-color: #d32f2f !important;
  color: white !important;
}

.confirm-btn:hover {
  background-color: #b71c1c !important;
}

.cancel-btn:hover {
  background-color: #666 !important;
}
</style> 