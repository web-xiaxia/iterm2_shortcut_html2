<script setup lang="ts">
import TabButton from '../components/TabButton.vue'
import CommonModal from '../components/common/CommonModal.vue'
import ConfirmModal from '../components/common/ConfirmModal.vue'
import {AppExecuteContext, AppGroup, AppSessionStatus, AppStatus, AppVariableHistoryStore} from "../types/AppConfig";
import {ref} from "vue";
import {componentMap} from "./AppButtonComponent.ts";

const props = defineProps<{
  buttonGroups: AppGroup[],
  appStatus: AppStatus,
  appSessionStatus: AppSessionStatus,
  executeContext: AppExecuteContext,
  variableHistory: AppVariableHistoryStore,
}>()

const emit = defineEmits<{
  moveGroupToOtherTab: [groupIndex: number]
}>()

const fontLevel = (level: number) => {
  return `font-level${level}`
}

// 新增分组
const showAddModal = ref(false)
const newGroup = ref<AppGroup>({
  fontLevel: 3,
  buttons: []
})

const handleAddGroup = () => {
  // 重置新按钮组
  newGroup.value = {
    fontLevel: 3,
    buttons: []
  }
  showAddModal.value = true
}

const saveNewGroup = () => {
  // 直接修改props的buttonGroups
  props.buttonGroups.push({...newGroup.value})
  showAddModal.value = false
}


// 修改分组
const showEditModal = ref(false)
const currentEditGroup = ref<AppGroup | null>(null)

const handleEdit = (group: AppGroup) => {
  currentEditGroup.value = group
  showEditModal.value = true
}

// 删除分组
const currentDeleteIndex = ref<number>(-1)
const showDeleteConfirm = ref(false)

const handleDelete = (index: number) => {
  currentDeleteIndex.value = index
  showDeleteConfirm.value = true
}

const confirmDelete = () => {
  if (currentDeleteIndex.value !== -1) {
    props.buttonGroups.splice(currentDeleteIndex.value, 1)
    currentDeleteIndex.value = -1
  }
}

// 新增按钮
const newButton = ref<string>("button")
const showAddButtonModal = ref(false)
const currentAddButtonIndex = ref<number>(-1)
const handleAddButton = (index: number) => {
  currentAddButtonIndex.value = index
  showAddButtonModal.value = true
}
const saveNewButton = () => {
  const newButtonType = newButton.value
  const newButtonInfo = componentMap[newButtonType].init()
  const addButtonGroup = props.buttonGroups[currentAddButtonIndex.value]
  addButtonGroup.buttons.push(newButtonInfo)
  showAddButtonModal.value = false
}


// 删除按钮
const showDeleteButtonConfirm = ref(false)
const currentDeleteButtonGroupIndex = ref<number>(-1)
const currentDeleteButtonIndex = ref<number>(-1)

const handleDeleteButton = (groupIndex: number, index: number) => {
  currentDeleteButtonGroupIndex.value = groupIndex
  currentDeleteButtonIndex.value = index
  showDeleteButtonConfirm.value = true
}
const confirmDeleteButton = () => {
  if (currentDeleteButtonGroupIndex.value !== -1 && currentDeleteButtonIndex.value !== -1) {
    props.buttonGroups[currentDeleteButtonGroupIndex.value].buttons.splice(currentDeleteButtonIndex.value, 1)
    currentDeleteButtonGroupIndex.value = -1
    currentDeleteButtonIndex.value = -1
  }
}

// 拖动

const draggedGroupIndex = ref<number | null>(null)
const draggedIndex = ref<number | null>(null)
const dragoverIndex = ref<number | null>(null);
const dragoverGroupIndex = ref<number | null>(null);
const isDraggingButton = ref(false); // 标记当前是否正在拖动按钮
const isDraggingGroup = ref(false); // 标记当前是否正在拖动组

// 按钮拖动
const dragStart = (groupIndex: number, index: number, event: DragEvent) => {
  // 阻止事件冒泡，防止触发组的拖动
  event.stopPropagation();

  draggedGroupIndex.value = groupIndex;
  draggedIndex.value = index;
  isDraggingButton.value = true;
}

const dragOver = (groupIndex: number, index: number) => {
  // 兼容原有逻辑
  dragoverGroupIndex.value = groupIndex;
  dragoverIndex.value = index;
}

const dragLeave = () => {
  dragoverIndex.value = null;
  dragoverGroupIndex.value = null;
}

const drop = (groupIndex: number, dropIndex: number) => {
  if (draggedGroupIndex.value !== null && draggedIndex.value !== null) {
    const sourceGroupIndex = draggedGroupIndex.value;
    const sourceItemIndex = draggedIndex.value;

    // 如果同组内拖动
    if (sourceGroupIndex === groupIndex) {
      // 原有的同组拖动逻辑
      if (sourceItemIndex !== dropIndex) {
        const items = props.buttonGroups[groupIndex].buttons;
        const draggedItem = items.splice(sourceItemIndex, 1)[0];
        items.splice(dropIndex, 0, draggedItem);
      }
    } else {
      // 跨组拖动的新逻辑
      const draggedItem = props.buttonGroups[sourceGroupIndex].buttons[sourceItemIndex];
      props.buttonGroups[sourceGroupIndex].buttons.splice(sourceItemIndex, 1);
      props.buttonGroups[groupIndex].buttons.splice(dropIndex, 0, draggedItem);
    }
  }
}

const dragEnd = () => {
  draggedGroupIndex.value = null;
  draggedIndex.value = null;
  dragoverIndex.value = null;
  dragoverGroupIndex.value = null;
  isDraggingButton.value = false;
}

// 按钮组拖动
const draggedGroup = ref<number | null>(null);
const dragoverGroup = ref<number | null>(null);

const groupDragStart = (index: number, event: DragEvent) => {
  // 如果当前正在拖动按钮，则不允许拖动组
  if (isDraggingButton.value) {
    event.preventDefault();
    return;
  }

  draggedGroup.value = index;
  isDraggingGroup.value = true;
}

const groupDragOver = (index: number) => {
  if (draggedGroup.value !== null && draggedGroup.value !== index) {
    dragoverGroup.value = index;
  }
}

const groupDragLeave = () => {
  dragoverGroup.value = null;
}

const groupDrop = (dropIndex: number) => {
  if (draggedGroup.value !== null && draggedGroup.value !== dropIndex) {
    const draggedItem = props.buttonGroups.splice(draggedGroup.value, 1)[0];
    props.buttonGroups.splice(dropIndex, 0, draggedItem);
  }
}

const groupDragEnd = () => {
  draggedGroup.value = null;
  dragoverGroup.value = null;
  isDraggingGroup.value = false;
}

// 移动按钮组到其他tab
const handleMoveToTab = (groupIndex: number) => {
  emit('moveGroupToOtherTab', groupIndex)
}

</script>

<template>
  <div class="button-group-box"
       :class="[fontLevel(buttonGroup.fontLevel), {
         'group-drag-source': draggedGroup === groupIndex && !isDraggingButton,
         'group-drag-over': dragoverGroup === groupIndex && draggedGroup !== groupIndex && !isDraggingButton,
         'button-drag-target': dragoverGroupIndex === groupIndex && draggedGroupIndex !== null && 
                              draggedIndex !== null && draggedGroupIndex !== groupIndex,
         'group-drag': draggedGroup,
       }]"
       v-for="(buttonGroup, groupIndex) in props.buttonGroups"
       :key="buttonGroup.fontLevel"
       :draggable="props.appSessionStatus.appMode == 'settings' && !props.appSessionStatus.editWidth && !isDraggingButton"
       @dragstart="(e) => groupDragStart(groupIndex, e)"
       @dragover.prevent="groupDragOver(groupIndex)"
       @dragleave="groupDragLeave"
       @dragenter.prevent
       @drop.prevent="groupDrop(groupIndex)"
       @dragend="groupDragEnd">
    <template v-if="buttonGroup.buttons && buttonGroup.buttons.length > 0">
      <div v-for="(button,index) in buttonGroup.buttons"
           :key="index"
           :style="{width:componentMap[button.type].showConfig.full?'100%':undefined}"
           :class="{
             'drag-source': draggedGroupIndex === groupIndex && draggedIndex === index,
             'drag-over-target': dragoverIndex === index &&  dragoverGroupIndex === groupIndex && !isDraggingGroup
           }"
           :draggable="props.appSessionStatus.appMode == 'settings' && !props.appSessionStatus.editWidth  && !isDraggingGroup"
           @dragstart="(e) => dragStart(groupIndex, index, e)"
           @dragover.prevent="(e) => { e.stopPropagation(); dragOver(groupIndex, index); }"
           @dragleave="(e) => { e.stopPropagation(); dragLeave(); }"
           @dragenter.prevent="(e) => e.stopPropagation()"
           @drop.prevent="(e) => { e.stopPropagation(); drop(groupIndex, index); }"
           @dragend="dragEnd"
      >
        <TabButton
            :buttons="buttonGroup.buttons"
            :button-index="index"
            :appStatus="props.appStatus"
            :appSessionStatus="props.appSessionStatus"
            :executeContext="props.executeContext"
            :variableHistory="props.variableHistory"
            @handleDelete="()=>{handleDeleteButton(groupIndex,index)}"
            :class="fontLevel(buttonGroup.fontLevel)"
        />
      </div>
    </template>
    <div v-else class="empty-buttons-text">无</div>
    <div class="button-group-settings-box" v-if="props.appSessionStatus.appMode=='settings'">
      <div class="button-group-settings-box-buttons">
        <button class="button-type-text" @click="handleAddButton(groupIndex)">+</button>
        <button class="button-type-text" @click="handleEdit(buttonGroup)">编辑</button>
        <button class="button-type-text" @click="handleDelete(groupIndex)">删除</button>
        <button class="button-type-text" @click="handleMoveToTab(groupIndex)">移动</button>
      </div>
    </div>
  </div>
  <div class="button-group-box button-group-add-box" style="border-bottom: 0;" v-if="props.appSessionStatus.appMode=='settings' &&  !props.appSessionStatus.editWidth">
    <input class="button-type-text" type="button" value="+" @click="handleAddGroup"/>
  </div>
  <div class="modal">
    <!-- 编辑按钮组模态框 -->
    <CommonModal
        v-model:visible="showEditModal"
        title="编辑按钮组"
    >
      <div class="form-row" v-if="currentEditGroup">
        <label>字体大小 (1-5)</label>
        <input type="number" v-model="currentEditGroup.fontLevel" min="1" max="5"/>
      </div>
      <div class="font-preview" v-if="currentEditGroup">
        <h4>字体大小预览：</h4>
        <div class="preview-item">
          <span class="font-level1">字体大小 1 (18px) - 大标题</span>
        </div>
        <div class="preview-item">
          <span class="font-level2">字体大小 2 (16px) - 小标题</span>
        </div>
        <div class="preview-item">
          <span class="font-level3">字体大小 3 (14px) - 正常文本</span>
        </div>
        <div class="preview-item">
          <span class="font-level4">字体大小 4 (12px) - 小文本</span>
        </div>
        <div class="preview-item">
          <span class="font-level5">字体大小 5 (10px) - 极小文本</span>
        </div>
      </div>
    </CommonModal>

    <!-- 新增按钮组模态框 -->
    <CommonModal
        v-model:visible="showAddModal"
        title="新增按钮组"
    >
      <div class="form-row">
        <label>字体大小 (1-5)</label>
        <input type="number" v-model="newGroup.fontLevel" min="1" max="5"/>
      </div>
      <div class="font-preview">
        <h4>字体大小预览：</h4>
        <div class="preview-item">
          <span class="font-level1">字体大小 1 - 大标题</span>
        </div>
        <div class="preview-item">
          <span class="font-level2">字体大小 2 - 小标题</span>
        </div>
        <div class="preview-item">
          <span class="font-level3">字体大小 3 - 正常文本</span>
        </div>
        <div class="preview-item">
          <span class="font-level4">字体大小 4 - 小文本</span>
        </div>
        <div class="preview-item">
          <span class="font-level5">字体大小 5 - 极小文本</span>
        </div>
      </div>
      <div class="modal-footer">
        <button class="button-primary" @click="saveNewGroup">保存</button>
      </div>
    </CommonModal>

    <!-- 新增按钮组模态框 -->
    <CommonModal
        v-model:visible="showAddButtonModal"
        title="新增按钮"
    >
      <select v-model="newButton">
        <option :value="v" v-for="(k,v) in componentMap" :key="v">{{ k.name }}</option>
      </select>
      <div class="modal-footer">
        <button class="button-primary" @click="saveNewButton">保存</button>
      </div>
    </CommonModal>

    <!-- 删除确认模态框 -->
    <ConfirmModal
        v-model:visible="showDeleteConfirm"
        title="删除按钮组"
        message="确定要删除这个按钮组吗？此操作不可撤销。"
        confirmText="删除"
        cancelText="取消"
        @confirm="confirmDelete"
    />

    <!-- 删除确认模态框 -->
    <ConfirmModal
        v-model:visible="showDeleteButtonConfirm"
        title="删除按钮"
        message="确定要删除这个按钮吗？此操作不可撤销。"
        confirmText="删除"
        cancelText="取消"
        @confirm="confirmDeleteButton"
    />
  </div>

</template>

<style scoped>
.button-group-box {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  border-bottom: 1px dashed rgb(131, 131, 131);
  padding: 0.2em 0.6em;
  position: relative;
  column-gap: 0.2em;
  row-gap: 0.1em;
}

.button-group-settings-box {
  flex: 1;
  display: none;
  position: absolute;
  z-index: 88;
  top: 100%;
  padding: 0 45px 0 10px;
  border-radius: 0 0 15px 0;
}
.button-group-box:hover .button-group-settings-box {
  display: flex;
}
.app-settings-edit-width .button-group-box:hover .button-group-settings-box {
  display: none;
}
.button-group-settings-box-buttons{
  background: #242424;
  border: 1px dashed rgb(131, 131, 131);
  border-top: none;
  border-radius: 0 0 3px 3px;
  padding: 0.1em 0.2em;
  font-size: 10px;
}


.font-level1 {
  font-size: 16px;
}

.font-level2 {
  font-size: 14px;
}

.font-level3 {
  font-size: 12px;
}

.font-level4 {
  font-size: 10px;
}

.font-level5 {
  font-size: 8px;
}

.font-preview {
  margin-top: 1rem;
  padding: 1rem;
  background: #333;
  border-radius: 4px;
  font-size: 14px;
}

.font-preview h4 {
  margin: 0 0 0.5rem 0;
  color: #ccc;
  font-size: 0.9rem;
}

.preview-item {
  margin: 0.5rem 0;
}

.preview-item span {
  display: inline-block;
  padding: 0.5rem;
  background: #444;
  border-radius: 3px;
  line-height: 1.5;
}

.modal-footer {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

.button-primary {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button-primary:hover {
  background-color: #45a049;
}

.empty-buttons-text {
  color: #888;
  font-style: italic;
  padding: 0.5em;
}

.drag-source {
  opacity: 0.5;
}

.drag-over-target {
  outline: 2px dashed skyblue;
  outline-offset: -2px;
  background-color: rgba(135, 206, 235, 0.1);
}

.group-drag-source {
  opacity: 0.5;
  border: 2px dashed #666;
}

.group-drag-over {
  outline: 2px dashed #4CAF50;
  outline-offset: -2px;
  background-color: rgba(76, 175, 80, 0.1);
}

.app-settings .group-drag * {
  pointer-events: none;
}

.button-drag-target {
  outline: 2px dashed orange;
  outline-offset: -2px;
  background-color: rgba(255, 165, 0, 0.1);
}
</style>