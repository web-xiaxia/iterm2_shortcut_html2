<script setup lang="ts">
import type {ButtonEditorCommonProps, ButtonProps} from "@/types/AppConfig.ts";
import {type AppButtonTypeConfigMultipleButton, AppButtonTypeConfigMultipleButtonExecuteInfo, ExecuteType} from "@/types/AppButton.ts";
import type {CSSProperties} from 'vue';
import {computed, ref} from "vue";
import Modal from '../common/CommonModal.vue';
import AppEditorCommon from "./AppEditorCommon.vue";
import {handleMouseenterEditWidth, handleMouseoutEditWidth} from "@/types/Common.ts";
import {AppButtonTypeButtonTypeMap} from "../AppButtonTypeButtonTypeConfig.ts";
import yaml from 'js-yaml';

const props = defineProps<ButtonProps<AppButtonTypeConfigMultipleButton>>();
const editorCommonProp = computed<ButtonEditorCommonProps>(() => ({
  buttonProps: props,
}))

interface ConfigTypeInfo {
  name: string
  key: string
  description: string
  getButtonList: (v: string) => AppButtonTypeConfigMultipleButtonExecuteInfo[]
}


const configTypeTextDescription = `
<div>
  <div class="description-title">格式1：</div>
  <div>名字:发送内容(默认会替换{{value(变量)}})</div>

  <div class="description-title">格式2:</div>
  <div>名字&gt;配置2,配置2:内容</div>
  <div>
  配置：<br/>
  &nbsp;&nbsp;&nbsp;&nbsp;disableEnter 不在末尾增加换行 <br/>
  &nbsp;&nbsp;&nbsp;&nbsp;disableReplace  不替换内容的{{value(变量)}} <br/>
  </div>
</div>
`

const configTypeTextToButtonConfigInfo = (v: string): {
  name: string
  type: ExecuteType
  disableReplace: boolean
  disableEnter: boolean
} => {
  let name = v
  let tempConfigType = 'send'
  let configOpt = ""
  if (v.includes("<")) {
    const valArr = v.split("<", 2)
    name = valArr[0]
    tempConfigType = valArr[1]
    if (tempConfigType.includes(">")) {
      const val2Arr = tempConfigType.split(">", 2)
      tempConfigType = val2Arr[0]
      configOpt = val2Arr[1]
    }
  } else if (v.includes(">")) {
    const valArr = v.split("<", 2)
    name = valArr[0]
    configOpt = valArr[1]
  }
  const tempConfigTypeSet = new Set(configOpt.split(","))
  const disableReplace = tempConfigTypeSet.has("disableReplace")
  const disableEnter = tempConfigTypeSet.has("disableEnter")
  return {
    name: name,
    type: tempConfigType as ExecuteType,
    disableReplace: disableReplace,
    disableEnter: disableEnter,
  }
}
const configTypeTextToButtonList = (v: string): AppButtonTypeConfigMultipleButtonExecuteInfo[] => {
  const configValue = v.trim()
  if (configValue.length == 0) {
    return []
  }
  const configArr = configValue.split("\n")
  const ret = <AppButtonTypeConfigMultipleButtonExecuteInfo[]>[]
  for (const configStr of configArr) {
    const configStrArr = configStr.split(":", 2)
    if (configStrArr.length != 2) {
      continue
    }

    const {name, type, disableReplace, disableEnter} = configTypeTextToButtonConfigInfo(configStrArr[0])
    const configValue = configStrArr[1]
    const replaceVariable = <string[]>[]
    if (!disableReplace) {
      const pattern = /\{\{(.+?)}}/g; // 使用全局标志g来查找所有匹配项
      const matches = configValue.match(pattern);
      if (matches) {
        for (const match of matches) {
          replaceVariable.push(match.substring(2, match.length - 2));
        }
      }
    }
    ret.push({
      name: name,
      value: configValue,
      type: type,
      disableReplace: disableReplace,
      replaceVariable: replaceVariable,
      disableEnter: disableEnter,
    })
  }
  return ret
}


interface ConfigTypeYmlInfo {
  disableReplace: boolean
  disableEnter: boolean
  value: string
  type: ExecuteType
}

const configTypeYamlDescription = `
名字:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;type: "send" | "send_variable" | "js" | "js_variable" | "py" | "py_variable" | "shell" | "shell_variable"<br/>
&nbsp;&nbsp;&nbsp;&nbsp;value: 内容<br/>
&nbsp;&nbsp;&nbsp;&nbsp;disableReplace: true<br/>
&nbsp;&nbsp;&nbsp;&nbsp;disableReplace: true<br/>
`

const configTypeYmlToButtonList = (v: string): AppButtonTypeConfigMultipleButtonExecuteInfo[] => {
  let yamlConfigs = undefined
  try {
    yamlConfigs = <{ [key: string]: ConfigTypeYmlInfo }>yaml.load(v);
  }catch (e) {
    return []
  }
  if (!yamlConfigs) {
    return []
  }

  const ret = <AppButtonTypeConfigMultipleButtonExecuteInfo[]>[]
  for (const k in yamlConfigs) {
    const v = yamlConfigs[k]
    if (!v){
      continue
    }
    const configValue = "" + (v.value || '')
    const replaceVariable = <string[]>[]
    if (!v.disableReplace) {
      const pattern = /\{\{(.+?)}}/g; // 使用全局标志g来查找所有匹配项
      const matches = configValue.match(pattern);
      if (matches) {
        for (const match of matches) {
          replaceVariable.push(match.substring(2, match.length - 2));
        }
      }
    }
    ret.push({
      name: k,
      value: configValue,
      type: v.type || 'send',
      disableReplace: v.disableReplace,
      replaceVariable: replaceVariable,
      disableEnter: v.disableEnter,
    })
  }
  return ret
}


const configTypeList = <ConfigTypeInfo[]>[{
  name: "文本",
  key: "",
  description: configTypeTextDescription,
  getButtonList: configTypeTextToButtonList
}, {
  name: "yaml",
  key: "yaml",
  description: configTypeYamlDescription,
  getButtonList: configTypeYmlToButtonList
}]
const configTypeMap = new Map<string, ConfigTypeInfo>(configTypeList.map(item => [item.key, item]));

const buttonList = computed<AppButtonTypeConfigMultipleButtonExecuteInfo[]>(() => {
  const configTypeInfo = configTypeMap.get(props.button.buttonInfo.configType)
  if (configTypeInfo) {
    return configTypeInfo.getButtonList(props.button.buttonInfo.configValue)
  }
  return configTypeTextToButtonList(props.button.buttonInfo.configValue)
})

const buttonStyle = computed<CSSProperties>(() => {
  return {
    color: props.button.color,
    borderColor: props.button.color,
    width: props.button.buttonInfo.width > 0 ? props.button.buttonInfo.width + "em" : undefined,
  }
});

const buttonTypeTitleMap = AppButtonTypeButtonTypeMap;

const showModal = ref(false);
const showConfigTypeDescription = ref(false);

function handleClickSettings() {
  if (props.appSessionStatus.appMode === 'settings') {
    showModal.value = true;
    return
  }
}

function handleClick(v: AppButtonTypeConfigMultipleButtonExecuteInfo) {
  if (props.appSessionStatus.editWidth) {
    return
  }
  const buttonType = buttonTypeTitleMap.get(v.type);
  if (buttonType) {
    let sendValue = v.value
    if (!v.disableReplace) {
      for (const variableName of v.replaceVariable) {
        const variableValues = props.executeContext.executeVariable.variable[variableName]?.values
        const variableValue = variableValues && variableValues.length > 0 ? variableValues[variableValues.length - 1] : ""
        sendValue = sendValue.replaceAll(`{{${variableName}}}`, variableValue)
      }
    }
    sendValue = sendValue.replace(/[\n\r]+$/, '');
    if (!v.disableEnter) {
      sendValue = sendValue + "\n"
    }
    buttonType.send(props.executeContext, sendValue)
  }
}

</script>

<template>
  <div @click="handleClickSettings" class="handle-click">
    <button v-for="v in buttonList" :class="{'edit-width-model':props.appSessionStatus.editWidth}"
            @mouseenter="handleMouseenterEditWidth($event,props)"
            @mouseout="handleMouseoutEditWidth(props.appSessionStatus)"
            :style="buttonStyle"
            @click="handleClick(v)"
    >
      {{ v.name }}
    </button>
    <label v-if="buttonList.length==0">无值</label>
  </div>

  <Modal
      v-model:visible="showModal"
      title="编辑配置按钮"
  >
    <AppEditorCommon v-bind="editorCommonProp"/>
    <div class="form-row">
      <div class="form-group">
        <div class="form-label">配置类型</div>
        <div class="form-input">
          <select v-model="props.button.buttonInfo.configType">
            <option :value="v.key" v-for="v in  configTypeList">{{ v.name }}</option>
          </select>
        </div>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group" style="align-items: flex-start;">
        <div class="form-label">
          <button @click="showConfigTypeDescription=!showConfigTypeDescription">{{ showConfigTypeDescription ? "关闭" : "打开" }}</button>
        </div>
        <div class="config-type-description" @click="showConfigTypeDescription=!showConfigTypeDescription" v-if="!showConfigTypeDescription" >
          点击打开说明
        </div>
        <div class="config-type-description" v-if="showConfigTypeDescription" v-html="configTypeMap.get(props.button.buttonInfo.configType)?.description">
        </div>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <div class="form-label">配置</div>
        <div class="form-input" style="">
          <textarea autocapitalize="off"
                    autocomplete="off"
                    spellcheck="false"
                    style="width: 37.3em"
                    v-model="props.button.buttonInfo.configValue"
                    rows="7"
          ></textarea>
        </div>
      </div>
    </div>

  </Modal>
</template>

<style scoped>
.config-type-description:deep(.description-title)   {
  color: #5dbd44;
}
</style>