<script setup lang="ts">
import {ref, computed} from 'vue';
import type {AppConfig} from "@/types/AppConfig.ts";
import type {AppVariableEventStore} from "@/types/AppButton.ts";
import {AppButtonVariableRefreshConfigList,AppButtonVariableRefreshConfigMap} from "../AppButtonVariableRefreshConfig";
import CommonSelect from "../common/CommonSelect.vue";

const props = defineProps<{
  appConfig: AppConfig
}>();

// 变量监听相关功能
const newEventType = ref('');
const newEventValue = ref('');
const newVariableName = ref('');
const variablesToAdd = ref<string[]>([]);
const editingEvent = ref<AppVariableEventStore | null>(null);

// 获取可用变量列表
const allVariables = computed<string[]>(() => {
  if (!props.appConfig.variable) return [];
  return Object.keys(props.appConfig.variable);
});

// 获取事件类型的输入模式
const getInputTypeForEvent = (eventType: string): 'input' | 'textarea'|'variable' => {
  const config = AppButtonVariableRefreshConfigList.find(item => item.key === eventType);
  return config?.inputType || 'textarea';
};

// 获取事件类型的可选值
const getOptionsForEvent = (eventType: string): string[] => {
  const config = AppButtonVariableRefreshConfigList.find(item => item.key === eventType);
  if (!config) return [];
  
  // 构造一个不完整但足够使用的对象
  return config.getOptions({
    variable: props.appConfig.variable || {},
    shell: props.appConfig.shell || {},
    js: props.appConfig.js || {},
    py: props.appConfig.py || {},
    event: props.appConfig.event || {},
    variable_event: (props.appConfig.variable_event || []) as AppVariableEventStore[]
  });
};

// 添加变量到临时列表
const addVariableToList = () => {
  if (newVariableName.value && !variablesToAdd.value.includes(newVariableName.value)) {
    variablesToAdd.value.push(newVariableName.value);
    newVariableName.value = '';
  }
};

// 从临时列表中移除变量
const removeVariableFromList = (index: number) => {
  variablesToAdd.value.splice(index, 1);
};

// 添加新的变量监听
const addNewVariableEvent = () => {
  if (newEventType.value && variablesToAdd.value.length > 0 && newEventValue.value) {
    if (!props.appConfig.variable_event) {
      props.appConfig.variable_event = [];
    }
    
    // 创建新的事件对象
    props.appConfig.variable_event.push({
      refreshType: newEventType.value as any,
      refreshValue: newEventValue.value,
      variables: [...variablesToAdd.value],
    });
    
    // 重置表单
    newEventType.value = '';
    newEventValue.value = '';
    variablesToAdd.value = [];
  }
};

// 开始编辑事件
const startEditing = (event: AppVariableEventStore) => {
  editingEvent.value =event;
};

// 取消编辑
const cancelEditing = () => {
  editingEvent.value = null;
};


// 从事件中移除变量
const removeVariableFromEvent = (event: AppVariableEventStore, variableIndex: number) => {
  if (!props.appConfig.variable_event) return;
  
  const eventIndex = props.appConfig.variable_event.findIndex(
    e => e.refreshType === event.refreshType &&
         JSON.stringify(e.variables) === JSON.stringify(event.variables)
  );
  
  if (eventIndex !== -1) {
    // 复制以避免直接修改
    const updatedEvent = {...event};
    updatedEvent.variables = [...event.variables];
    updatedEvent.variables.splice(variableIndex, 1);
    
    if (updatedEvent.variables.length === 0) {
      // 如果没有变量了，删除整个事件
      props.appConfig.variable_event.splice(eventIndex, 1);
    } else {
      // 更新事件
      props.appConfig.variable_event[eventIndex] = updatedEvent;
    }
  }
};

// 删除整个事件
const deleteEvent = (event: AppVariableEventStore) => {
  if (!props.appConfig.variable_event) return;
  
  const eventIndex = props.appConfig.variable_event.findIndex(
    e => e.refreshType === event.refreshType &&
         JSON.stringify(e.variables) === JSON.stringify(event.variables)
  );
  
  if (eventIndex !== -1) {
    props.appConfig.variable_event.splice(eventIndex, 1);
  }
};

// 添加一个专门在编辑状态下添加变量的方法
const addVariableToEditing = () => {
  if (!editingEvent.value || !newVariableName.value) return;
  
  // 检查变量是否已经存在于列表中
  if (!editingEvent.value.variables.includes(newVariableName.value)) {
    editingEvent.value.variables.push(newVariableName.value);
    newVariableName.value = '';
  }
};
</script>

<template>
  <div class="config-container">
    <h3>变量监听配置</h3>

    <!-- 变量监听列表 -->
    <div class="config-list">
      <!-- 添加新变量监听 (使用与列表相同的卡片式布局) -->
      <div class="monitor-item add-monitor-item">
        <div class="monitor-header">
          <div class="monitor-title">
            <span class="event-type">新建变量监听</span>
          </div>
        </div>
        
        <div class="monitor-body">
          <div class="monitor-section">
            <div class="section-title">执行类型：</div>
            <select v-model="newEventType" class="config-input">
              <option value="">请选择执行类型</option>
              <option v-for="buttonType in AppButtonVariableRefreshConfigList" :value="buttonType.key">
                {{ buttonType.name }}
              </option>
            </select>
          </div>
          
          <div v-if="newEventType" class="monitor-section">
            <div class="section-title">{{ AppButtonVariableRefreshConfigMap.get(newEventType)?.title || '执行内容' }}</div>

            <input v-if="getInputTypeForEvent(newEventType) == 'input'" v-model="newEventValue">
            <CommonSelect
                v-else-if="getInputTypeForEvent(newEventType) == 'variable'"
                :modelValue="newEventValue"
                :options="getOptionsForEvent(newEventType)"
                :hideAdd="true"
                :hideRemove="true"
                width="14.8em"
                height="2.2em"
                @update:modelValue="(newVal:string)=>newEventValue=newVal"
            />
            <textarea style="width: 37.3em" v-else v-model="newEventValue" rows="7"></textarea>
          </div>
          
          <div v-if="newEventType && newEventValue" class="monitor-section">
            <div class="section-title">监听变量：</div>
            <div class="input-with-button">
              <CommonSelect
                v-model="newVariableName"
                :options="allVariables"
                :hideRemove="true"
                width="14.8em"
                height="2.2em"
                @add-option="addVariableToEditing"
              />
              <button @click="addVariableToList" class="small-btn">添加</button>
            </div>
            <div class="variables-container">
              <div v-for="(variable, index) in variablesToAdd" :key="index" class="variable-tag">
                <span>{{ variable }}</span>
                <button class="remove-variable-btn" @click="removeVariableFromList(index)">×</button>
              </div>
            </div>
          </div>
          
          <div v-if="variablesToAdd.length > 0" class="form-actions">
            <button @click="addNewVariableEvent" class="save-btn">保存配置</button>
          </div>
        </div>
      </div>
      
      <!-- 已有的变量监听列表 -->
      <div 
          v-for="(event, eventIndex) in props.appConfig.variable_event || []" 
          :key="eventIndex" 
          class="monitor-item"
          :class="{'editing': editingEvent && editingEvent.refreshType === event.refreshType && JSON.stringify(editingEvent.variables) === JSON.stringify(event.variables)}"
      >
        <!-- 非编辑状态 -->
        <div v-if="!editingEvent" class="monitor-content">
          <div class="monitor-header">
            <div class="monitor-title">
              <span class="event-type">{{ AppButtonVariableRefreshConfigMap.get(event.refreshType)?.name }}</span>
            </div>
            <div class="monitor-actions">
              <button @click="startEditing(event)" class="edit-btn">编辑</button>
              <button @click="deleteEvent(event)" class="delete-btn">删除</button>
            </div>
          </div>
          
          <div class="monitor-body">
            <div class="monitor-section">
              <div class="section-title">{{ AppButtonVariableRefreshConfigMap.get(event.refreshType)?.title || '执行内容' }}</div>
              <div class="event-value-display">
                {{ event.refreshType }}
              </div>
            </div>

            <div class="monitor-section">
              <div class="section-title">监听变量：</div>
              <div class="variables-container">
                <div v-for="(variable, varIndex) in event.variables" :key="varIndex" class="variable-tag">
                  <span>{{ variable }}</span>
                  <button class="remove-variable-btn" @click="removeVariableFromEvent(event, varIndex)">×</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 编辑状态 -->
        <div v-else class="monitor-edit-form">
          <div class="monitor-section">
            <div class="section-title">执行类型：</div>
            <select v-model="editingEvent.refreshType" class="config-input">
              <option v-for="buttonType in AppButtonVariableRefreshConfigList" :value="buttonType.key">
                {{ buttonType.name }}
              </option>
            </select>
          </div>
          
          <div class="monitor-section">
            <div class="section-title">执行内容：</div>
            <input v-if="getInputTypeForEvent(editingEvent.refreshType) == 'input'" v-model="editingEvent.refreshValue">
            <CommonSelect
                v-else-if="getInputTypeForEvent(editingEvent.refreshType) == 'variable'"
                :modelValue="editingEvent.refreshValue"
                :options="getOptionsForEvent(editingEvent.refreshType)"
                :hideAdd="true"
                :hideRemove="true"
                width="14.8em"
                height="2.2em"
                @update:modelValue="(newVal:string)=>{if(editingEvent){editingEvent.refreshValue=newVal}}"
            />
            <textarea style="width: 37.3em" v-else v-model="editingEvent.refreshValue" rows="7"></textarea>
          </div>
          
          <div class="monitor-section">
            <div class="section-title">监听变量：</div>
            <div class="input-with-button">
              <CommonSelect
                v-model="newVariableName"
                :options="allVariables"
                :hideRemove="true"
                width="14.8em"
                height="2.2em"
                @add-option="addVariableToEditing"
              />
              <button 
                  @click="addVariableToEditing" 
                  class="small-btn"
              >添加</button>
            </div>
            <div class="variables-container">
              <div v-for="(variable, index) in editingEvent.variables" :key="index" class="variable-tag">
                <span>{{ variable }}</span>
                <button class="remove-variable-btn" @click="editingEvent.variables.splice(index, 1)">×</button>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button @click="cancelEditing" class="save-btn">完成</button>
          </div>
        </div>
      </div>
      
      <div v-if="!props.appConfig.variable_event?.length && variablesToAdd.length === 0" class="empty-message">
        暂无变量监听配置
      </div>
    </div>
  </div>
</template>

<style scoped>
.add-monitor-item {
  border-left: 3px solid #6b8e23;
  background-color: rgba(60, 70, 50, 0.5);
}

.add-monitor-item .event-type {
  background-color: #6b8e23;
}
</style> 