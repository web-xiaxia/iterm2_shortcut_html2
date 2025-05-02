<script setup lang="ts">
import {ref} from 'vue';
import type {AppSessionStatus, AppStatus, AppTab} from "../types/AppConfig";
import Modal from './common/CommonModal.vue';
import ConfirmModal from "./common/ConfirmModal.vue";


const props = defineProps<{
  tabs: AppTab[],
  appStatus: AppStatus,
  appSessionStatus: AppSessionStatus,
}>()

// 编辑模态框状态
const showEditModal = ref(false);
const currentEditingIndex = ref(-1);
// 打开编辑模态框
const openEditModal = (index: number) => {
  currentEditingIndex.value = index;
  showEditModal.value = true;
}

// 新增标签模态框状态
const showAddModal = ref(false);
const newTabTitle = ref('');

// 打开新增标签模态框
const openAddModal = () => {
  newTabTitle.value = '';
  showAddModal.value = true;
}

// 确认新增标签
const confirmAddTab = () => {
  if (newTabTitle.value.trim()) {
    props.tabs.push({
      title: newTabTitle.value.trim(),
      buttonGroups: []
    });
    showAddModal.value = false;
  }
}

// 删除标签
const currentDeleteIndex = ref<number>(-1)
const showDeleteConfirm = ref(false)
const handleDeleteTab = (index: number) => {
  currentDeleteIndex.value = index
  showDeleteConfirm.value = true
}

const confirmDeleteTab = () => {
  if (currentDeleteIndex.value !== -1) {
    props.tabs.splice(currentDeleteIndex.value, 1)
    currentDeleteIndex.value = -1
    props.appStatus.index = 0;
    showDeleteConfirm.value = false
  }
}

// 控制按钮显示状态
const showControlsIndex = ref<number>(-1)

// 显示控制按钮
const toggleControls = (event: Event, index: number) => {
  event.stopPropagation()
  // 只有当前选中的标签才能显示控制按钮
  if (props.appStatus.index === index) {
    showControlsIndex.value = showControlsIndex.value === index ? -1 : index
  }
  props.appStatus.index = index;
}

// 隐藏控制按钮
const hideControls = () => {
  showControlsIndex.value = -1
}

// 拖拽排序相关变量和方法
const draggedItem = ref<number>(-1) // 被拖拽的标签索引
const dragoverIndex = ref<number>(-1) // 拖拽悬停的目标索引

// 开始拖拽
const handleDragStart = (index: number) => {
  if (props.appSessionStatus.appMode === 'settings' && props.appStatus.index === index) {
    draggedItem.value = index
  }
}

// 拖拽经过
const handleDragOver = (event: DragEvent, index: number) => {
  if (props.appSessionStatus.appMode === 'settings' && event.dataTransfer) {
    event.preventDefault()
    // 获取当前拖拽经过的元素索引
    dragoverIndex.value = index
  }
}

// 放置拖拽元素
const handleDrop = (event: DragEvent, index: number) => {
  if (props.appSessionStatus.appMode === 'settings' && draggedItem.value !== -1 && draggedItem.value !== index) {
    event.preventDefault()
    // 移动标签
    const draggedTab = {...props.tabs[draggedItem.value]}
    props.tabs.splice(draggedItem.value, 1)
    props.tabs.splice(index, 0, draggedTab)

    // 更新当前选中的标签索引
    if (props.appStatus.index === draggedItem.value) {
      props.appStatus.index = index
    } else if (props.appStatus.index > draggedItem.value && props.appStatus.index <= index) {
      props.appStatus.index--
    } else if (props.appStatus.index < draggedItem.value && props.appStatus.index >= index) {
      props.appStatus.index++
    }

    draggedItem.value = -1
    dragoverIndex.value = -1
  }
}

// 拖拽结束
const handleDragEnd = () => {
  draggedItem.value = -1
  dragoverIndex.value = -1
}

// 拖拽离开
const handleDragLeave = (index: number) => {
  // 只有当离开的是当前目标元素时才重置
  if (dragoverIndex.value === index) {
    dragoverIndex.value = -1
  }
}
</script>

<template>
  <div class="tab-select">
    <div class="left-content">
      <template v-for="(tab,index) in props.tabs" :key="index">
        <div v-if="!tab.hide"
             class="tab-item"
             :class="{
              activity: props.appStatus.index === index, 
              draggable: props.appSessionStatus.appMode=='settings' && props.appStatus.index === index,
              'tab-drag-source': draggedItem === index,
              'tab-drag-over': dragoverIndex === index && draggedItem !== index
            }"
             @click.stop="toggleControls($event,index)"
             @mouseleave="hideControls()"
             :draggable="props.appSessionStatus.appMode=='settings' && props.appStatus.index === index"
             @dragstart="handleDragStart(index)"
             @dragover="handleDragOver($event,index)"
             @drop="handleDrop($event,index)"
             @dragend="handleDragEnd()"
             @dragleave="handleDragLeave(index)"
             @dragenter.prevent
             :data-index="index">
          {{ tab.title }}
          <div v-if="props.appSessionStatus.appMode=='settings' && !props.appSessionStatus.editWidth && props.appStatus.index === index && showControlsIndex === index" class="tab-controls">
            <button class="button-type-text" @click.stop="openEditModal(index)">编辑</button>
            <button class="button-type-text" @click.stop="handleDeleteTab(index)">删除</button>
          </div>
        </div>
      </template>
      <span v-if="props.appSessionStatus.appMode=='settings' &&  !props.appSessionStatus.editWidth" class="add-tab-btn" @click="openAddModal">+</span>

    </div>
    <div class="right-content">
      <span class="tab-text-button-item" v-if="props.appSessionStatus.appMode=='settings' && !props.appSessionStatus.editWidth" @click="props.appSessionStatus.editWidth=true">调整宽度</span>
      <span class="tab-text-button-item" v-if="props.appSessionStatus.appMode=='settings' && props.appSessionStatus.editWidth" @click="props.appSessionStatus.editWidth=false">完成</span>
      <span class="tab-text-button-item" v-if="!props.appSessionStatus.editWidth" @click="props.appSessionStatus.editSettings=true">设置</span>
      <span class="tab-text-button-item" v-if="props.appSessionStatus.appMode=='settings' && !props.appSessionStatus.editWidth" @click="props.appSessionStatus.appMode='show'">完成</span>
      <span class="tab-text-button-item" v-if="props.appSessionStatus.appMode=='show'" @click="props.appSessionStatus.appMode='settings'">编辑</span>
    </div>

    <div class="tab-box-border"></div>
  </div>

  <!-- 编辑模态框 -->
  <div v-if="showEditModal && currentEditingIndex>=0 ">
    <Modal v-model:visible="showEditModal" title="编辑标签">
      <input v-model="props.tabs[currentEditingIndex].title" placeholder="输入标签名称"/>
    </Modal>
  </div>

  <!-- 新增标签模态框 -->
  <Modal v-model:visible="showAddModal" title="新增标签">
    <input v-model="newTabTitle" placeholder="输入标签名称"/>
    <div class="modal-actions">
      <button @click="showAddModal = false">取消</button>
      <button @click="confirmAddTab">确定</button>
    </div>
  </Modal>

  <!-- 删除确认模态框 -->
  <ConfirmModal
      v-model:visible="showDeleteConfirm"
      title="删除tab"
      message="确定要删除这个tab吗？此操作不可撤销。"
      confirmText="删除"
      cancelText="取消"
      @confirm="confirmDeleteTab"
  />
</template>

<style scoped>
.tab-select {
  flex-grow: 1;
  overflow: scroll;
  padding: 4px 0 0 0;
  background-color: rgb(28, 25, 25);
  white-space: nowrap;
  overflow-x: hidden;
  overflow-y: hidden;
  display: flex;
  justify-content: space-between;
  align-items: end;
  width: 100%;
  position: relative;
}

.tab-select .left-content {
  flex: 0 1 auto; /* 不增长，可收缩，基于内容宽度 */
  overflow-x: auto; /* 水平滚动 */
  white-space: nowrap; /* 防止内容换行 */
  min-width: 0; /* 关键！允许收缩小于内容宽度 */
}

.tab-select .right-content {
  flex: 0 0 auto; /* 固定宽度，不伸缩 */
  margin-left: auto; /* 关键！将右侧推到最右 */
  padding: 0 2px 0 10px;
  font-size: 10px;
  display: flex;
}

.right-content .tab-text-button-item {
  padding: 2px;
  cursor: pointer;
}

.right-content .tab-item:hover {
  border: 0;
}

.tab-select .left-content::before {
  content: '';
  padding-left: 20px;
}

.tab-select .left-content::after {
  content: '';
  padding-right: 20px;
}

.tab-select .tab-item {
  position: relative;
  max-width: 300px;
  text-overflow: ellipsis;
  overflow: hidden;
  vertical-align: bottom;
  display: inline-block;
  padding: 0.1em 0.8em;
  margin: 0 0.1em;

  cursor: pointer;
  border-radius: 5px 5px 0 0;
  border: 1px solid rgb(0 0 0 / 0%);
}

.left-content .tab-item {
  min-width: 40px;
  text-align: center;
}

.tab-select .tab-item:hover {
  border: 1px solid rgb(143, 143, 143);
  background: rgb(65 70 74);
}

.tab-select .tab-item.activity {
  position: relative;
  border: 1px solid rgb(143, 143, 143);
  border-bottom: 1px solid rgb(38, 37, 37);
  z-index: 21;
  background: rgb(38, 37, 37);
}

.tab-select .tab-controls {
  position: absolute;
  top: 1px;
  left: 1px;
  gap: 2px;
  display: flex;
  background: #000000;
  padding: 1px 2px;
}

.tab-controls {
  background: #242424;
  border: 1px dashed rgb(131, 131, 131);
  border-radius: 3px;
}

.tab-controls .button-type-text {
  font-size: 10px;
  padding: 2px !important;
  margin: 0 !important;
  min-width: 10px !important;
  line-height: 10px !important;
}

.tab-select .tab-box-border {
  border-bottom: 1px solid rgb(143, 143, 143);
  width: 100%;
  position: absolute;
  bottom: 0;
  z-index: 10;
}


.modal-content h3 {
  margin-top: 0;
  margin-bottom: 15px;
}

.modal-content input {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #444;
  border-radius: 3px;
  background-color: #333;
  color: white;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.modal-actions button {
  padding: 6px 12px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.modal-actions button:first-child {
  background-color: #555;
  color: white;
}

.modal-actions button:last-child {
  background-color: #4a90e2;
  color: white;
}

.add-tab-btn {
  display: inline-block;
  padding: 0.1em 0.8em;
  margin: 0 0.1em;
  cursor: pointer;
  border-radius: 5px 5px 0 0;
}

.add-tab-btn:hover {
  background: rgb(65 70 74);
}

.tab-select .tab-item.draggable {
  cursor: move;
  position: relative;
}

/* 拖拽相关样式 */
.tab-select .tab-item.tab-drag-source {
  opacity: 0.5;
  border: 1px dashed #666;
  border-bottom: 0;
}

.tab-select .tab-item.tab-drag-over {
  outline: 1px dashed #4CAF50;
  outline-offset: -2px;
  background-color: rgba(76, 175, 80, 0.1);
}

/* 在设置模式下拖拽时禁用其他事件 */
.tab-select .tab-item.tab-drag-source * {
  pointer-events: none;
}

</style>