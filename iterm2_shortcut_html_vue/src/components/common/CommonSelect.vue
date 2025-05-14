<script setup lang="ts">
import { computed, ref, watch, type PropType } from 'vue'
import { ElMessage } from 'element-plus'

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
    default: '10em'
  },
  height: {
    type: String,
    default: ''
  },
  color: {
    type: [String],
    default: '#ffffff'
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

const searchText = ref(props.modelValue)
const selectedValue = ref(props.modelValue)

// 当外部 modelValue 变化时更新内部值
watch(() => props.modelValue, (newVal) => {
  selectedValue.value = newVal
  searchText.value = newVal
})

// 是否显示添加新选项
const showAddOption = computed(() => {
  if (!searchText.value) return false
  return !props.options.some(
      option => option.toLowerCase() === searchText.value.toLowerCase()
  )
})

// 处理搜索输入变化
const handleSearchChange = (value: string) => {
  searchText.value = value
}

// 处理选项选择
const handleSelect = (value: string) => {
  selectedValue.value = value
  emits('update:modelValue', value)
}

// 添加新选项
const addNewOption = () => {
  if (props.disabled || !searchText.value) return

  const newOption = searchText.value
  emits('add-option', newOption)
  handleSelect(newOption)
  ElMessage.success(`添加选项: ${newOption}`)
}

// 删除选项
const removeOption = (option: string) => {
  if (props.disabled) return

  if (selectedValue.value === option) {
    selectedValue.value = ''
    emits('update:modelValue', '')
  }

  emits('remove-option', option)
  ElMessage.success(`删除选项: ${option}`)
}

// 设置新值
const setNewValue = () => {
  if (props.disabled || !searchText.value) return
  
  const newOption = searchText.value
  selectedValue.value = newOption
  emits('update:modelValue', newOption)
}

// 自定义样式
const selectStyle = computed(() => ({
  width: props.width,
  '--el-input-border-color': props.color,
  '--el-select-input-color': props.color,
  '--el-select-border-color-hover': props.color,
}))
</script>

<template>
  <div class="el-select-wrapper" :style="selectStyle">
    <el-select
      v-model="selectedValue"
      filterable
      :disabled="disabled"
      allow-create
      default-first-option
      remote
      :remote-method="handleSearchChange"
      @change="handleSelect"
      :class="[bindClass]"
      :placeholder="'请选择'"
      :style="{ height }"
    >
      <!-- 添加新选项 -->
      <template #prefix v-if="showAddOption && !hideAdd">
        <el-button
          link
          type="primary"
          size="small"
          @click.stop="addNewOption"
          :disabled="disabled"
        >
          添加
        </el-button>
      </template>

      <!-- 设置新值 -->
      <template #header v-if="showAddOption">
        <div class="select-header-action" @click.stop="setNewValue">
          设置 "{{ searchText }}"
        </div>
      </template>

      <!-- 选项列表 -->
      <el-option
        v-for="option in options"
        :key="option"
        :label="option"
        :value="option"
      >
        <div class="option-container">
          <span>{{ option }}</span>
          <el-button
            v-if="!hideRemove"
            link
            type="danger"
            size="small"
            @click.stop="removeOption(option)"
            :disabled="disabled"
          >
            删除
          </el-button>
        </div>
      </el-option>
    </el-select>
  </div>
</template>

<style scoped>
/* 已移动到全局 style.css 文件 */
</style>