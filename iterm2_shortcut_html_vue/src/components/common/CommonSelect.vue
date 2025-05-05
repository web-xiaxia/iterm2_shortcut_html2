<script setup lang="ts">
import {computed, type CSSProperties, onMounted, onUnmounted, type PropType, ref, watch} from 'vue'


const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  options: {
    type: Array as PropType<string[]>,
    required: true
  },
  width: {
    type: String,
    default: '10em' // 默认宽度为10em（约10个字符）
  },
  height: {
    type: String,
    default: '' // 默认宽度为10em（约10个字符）
  },
  color: {
    type: [String],
    default: '#ffffff' // 默认宽度为10em（约10个字符）
  },
  disabled: {
    type: Boolean,
    default: false
  },
  bindClass: {
    default: {},
  },
  hideAdd: {
    type: Boolean,
    default: false
  },
  hideRemove: {
    type: Boolean,
    default: false
  }
});
const emits = defineEmits<{
  'update:modelValue': [newVal: string],
  'add-option': [addVal: string],
  'remove-option': [removeVal: string],
}>()

const isOpen = ref(false)
const searchText = ref(props.modelValue)
const selectedValue = ref(props.modelValue)
const inputRef = ref<HTMLInputElement | null>(null)
const isMouseDownInSelect = ref(false)

// 当外部 modelValue 变化时更新内部值
watch(() => props.modelValue, (newVal) => {
  selectedValue.value = newVal
  searchText.value = newVal
})

// 过滤后的选项
const filteredOptions = computed(() => {
  if (!searchText.value) return props.options
  return props.options.filter(option =>
      option.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

// 是否显示添加新选项
const showAddOption = computed(() => {
  if (!searchText.value) return false
  return !props.options.some(
      option => option.toLowerCase() === searchText.value.toLowerCase()
  )
})

// 检查选项是否已选中
const isSelected = (option: string) => {
  return selectedValue.value === option
}

// 完全重写控制点击事件
const handleControlClick = () => {
  if (props.disabled) return;

  isOpen.value = !isOpen.value
  if (isOpen.value) {
    // 让输入框获得焦点但不触发焦点事件
    setTimeout(() => {
      if (inputRef.value) {
        inputRef.value.focus()
      }
    }, 10)
  }
}

// 关闭下拉框
const closeDropdown = () => {
  isOpen.value = false
  searchText.value=selectedValue.value
}

// 选择选项
const selectOption = (option: string) => {
  if (props.disabled) return;

  selectedValue.value = option
  emits('update:modelValue', option)
  closeDropdown()
  searchText.value = option
}

const setNewValue = () => {
  if (props.disabled || !searchText.value) {
    closeDropdown()
    return;
  }
  const newOption = searchText.value
  selectedValue.value = newOption
  selectOption(newOption)
}
// 添加新选项
const addNewOption = () => {
  if (props.disabled || !searchText.value) {
    closeDropdown()
    return;
  }

  const newOption = searchText.value
  emits('add-option', newOption)
  selectOption(newOption)
}

// 删除选项
const removeOption = (option: string) => {
  if (props.disabled) return;

  if (selectedValue.value === option) {
    selectedValue.value = ''
    emits('update:modelValue', '')
  }

  emits('remove-option', option)
}

// 处理回车键
const handleEnterKey = (e: KeyboardEvent) => {
  if (props.disabled) return;

  {
    setNewValue()
  }

  (e.target as HTMLElement).blur()
}


// 添加鼠标按下事件监听器
const handleMouseDown = () => {
  if (props.disabled) return;

  isMouseDownInSelect.value = true
}

// 点击外部关闭
const handleOutsideClick = (event: MouseEvent) => {
  if (props.disabled) return;

  const element = event.target as HTMLElement
  const select = document.querySelector('.searchable-select')
  if (select && !select.contains(element) && isOpen.value) {
    closeDropdown()
  }
}

// 挂载时添加点击事件监听器
onMounted(() => {
  document.addEventListener('mousedown', handleOutsideClick)
})

// 卸载时移除点击事件监听器
onUnmounted(() => {
  document.removeEventListener('mousedown', handleOutsideClick)
})

// 计算样式
const selectStyle = computed<CSSProperties>(() => {
  return {
    width: props.width,
  }
})
const selectControlStyle = computed<CSSProperties>(() => {
  return {
    borderColor: props.color != null && props.color.length > 0 ? props.color : undefined,
    height: props.height,
  }
})
const selectInputStyle = computed<CSSProperties>(() => {
  return {
    color: props.color != null && props.color.length > 0 ? props.color : undefined
  }
})
</script>

<template>
  <div class="searchable-select"
       @mousedown="handleMouseDown"
       :style="selectStyle"
       :class="{'select-pointer': props.disabled}">
    <!-- 输入框和下拉箭头 -->
    <div class="select-control" :class="props.bindClass" :style="selectControlStyle" @click="handleControlClick">
      <input
          ref="inputRef"
          v-model="searchText"
          type="text"
          autocapitalize="off"
          class="select-input"
          :style="selectInputStyle"
          @keydown.enter="handleEnterKey"
          :readonly="props.disabled"
      />
      <span class="arrow" :class="{ 'arrow-up': isOpen }">▼</span>
    </div>

    <!-- 下拉选项列表 -->
    <ul v-show="isOpen && !props.disabled" class="dropdown-menu">
      <!-- 添加新选项的提示 -->
      <li
          v-if="showAddOption"
          class="dropdown-item add-option"
          @mousedown="setNewValue"
      >
        设置 "<strong>{{ searchText }}</strong>"
      </li>
      <li
          v-if="showAddOption && !props.hideAdd"
          class="dropdown-item add-option"
          @mousedown="addNewOption"
      >
        添加 "<strong>{{ searchText }}</strong>"
      </li>

      <!-- 搜索结果或全部选项 -->
      <li
          v-for="option in filteredOptions"
          :key="option"
          class="dropdown-item dropdown-item-option"
          :class="{ 'selected': isSelected(option) }"
      >
        <span class="option-text" @mousedown="selectOption(option)">{{ option }}</span>
        <span class="remove-icon" v-if="!props.hideRemove" @mousedown.stop="removeOption(option)">×</span>
      </li>


    </ul>
  </div>
</template>


<style scoped>
.searchable-select {
  position: relative;
  font-family: inherit;
  font-size: inherit;
}

.searchable-select.select-pointer {
  cursor: pointer;
}

.select-control {
  position: relative;
  border: 1px dashed #FFFFFF;
  border-radius: 4px;
  padding: 0 0.3em 0 0.4em;
  cursor: text;
  display: flex;
  align-items: center;
  min-height: 1.2em;
  box-sizing: border-box;
}

.select-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 0;
  margin: 0;
  font-size: 0.8rem;
  line-height: 1;
  height: 1.5em;
  box-sizing: border-box;
  max-width: calc(100% - 1em);
}

.select-input::placeholder {
  color: v-bind(color);
  opacity: 1;
}

.arrow {
  margin-left: 0;
  transition: transform 0.2s;
  font-size: 0.7em;
  color: v-bind(color);
  display: inline-flex;
  align-self: center;
  line-height: 1;
  min-width: 0.6em;
  padding-right: 0;
  text-align: center;
  position: absolute;
  right: 0.3em;
}

.arrow-up {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 200px;
  overflow-y: auto;
  margin: 0.25em 0 0;
  padding: 0;
  border: 1px solid #444;
  border-radius: 4px;
  background: #1a1a1a;
  z-index: 1000;
  list-style: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  font-size: inherit;
}

.dropdown-item {
  padding: 0.1em 0.3em;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #e0e0e0;
  min-height: 1.5em;
  line-height: 1.5;
}

.dropdown-item:hover {
  background-color: #2c2c2c;
}

.dropdown-item.selected {
  background-color: #303030;
}
.dropdown-item-option{
  display: flex;
  justify-content: flex-end;
}
.dropdown-item-option .option-text {
  overflow: hidden; /* 隐藏溢出的内容 */
  text-overflow: ellipsis; /* 超出部分显示为省略号 */
  white-space: nowrap; /* 防止文本换行 */
  flex: 1; /* 让左边元素尽可能地填充剩余空间 */
}

.add-option {
  color: #1890ff;
  font-style: italic;
  white-space: nowrap;
}
.add-option strong {
  text-overflow: ellipsis;
  overflow: hidden;
}

.option-text {
  flex: 1;
}

.remove-icon {
  color: #ff4d4f;
  font-weight: bold;
  padding: 0 0.25em;
  font-size: 1.25em;
  opacity: 0;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 1.5em;
  width: 1.5em;
}

.dropdown-item:hover .remove-icon {
  opacity: 1;
}

.remove-icon:hover {
  color: #ff7875;
  background-color: #3a2a2a;
  border-radius: 50%;
}
</style>