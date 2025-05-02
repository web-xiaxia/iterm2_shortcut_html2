import {computed, type ComputedRef, type WritableComputedRef} from "vue";

export interface AppVariableTool {
    variable: ComputedRef<AppVariable>
    value: WritableComputedRef<string | undefined>
}

class AppVariableToolImpl implements AppVariableTool {
    variable: ComputedRef<AppVariable>
    value: WritableComputedRef<string | undefined>

    constructor(a: ComputedRef<AppVariable>) {
        this.variable = a
        if (a.value.values == undefined) {
            a.value.values = []
        }
        this.value = computed({
            get: () => {
                if (this.variable.value.values && this.variable.value.values.length > 0) {
                    return this.variable.value.values[this.variable.value.values.length - 1]
                }
                return undefined
            },
            set: (v: string | undefined): void => {
                if (!v) {
                    v = ""
                }
                this.variable.value.values = [v]
            }
        })
    }
}

function getAppVariable(getVariableName: ComputedRef<string | undefined> | undefined, globalVariable: AppVariableStore, add: boolean): AppVariable {
    const variableName = getVariableName?.value
    if (!variableName) {
        return {
            values: [],
            options: [],
        }
    }
    let ret = globalVariable[variableName]
    if (ret) {
        return ret
    }
    if (add) {
        globalVariable[variableName] = {
            values: [],
            options: [],
        }
        return globalVariable[variableName]
    }
    return {
        values: [],
        options: [],
    }
}

export function GetAppVariableRef(buttonInfo: AppButtonInfoTypeVariableInfo, globalVariable: AppVariableStore): ComputedRef<AppVariableTool> {
    return GetAppVariableRefWithGetFunc(() => buttonInfo.variableName, globalVariable)
}

export function GetAppVariableRefWithGetFunc(getFunc: () => string | undefined, globalVariable: AppVariableStore): ComputedRef<AppVariableTool> {
    const getVal = computed<string | undefined>(getFunc)
    return computed({
        get: (): AppVariableTool => {
            return new AppVariableToolImpl(computed(() => getAppVariable(getVal, globalVariable, true)))
        },
        set: (newVal: AppVariableTool) => {
            const v = getAppVariable(getVal, globalVariable, true)
            v.values = newVal.variable.value.values
            v.options = newVal.variable.value.options;
        }
    })
}

export function GetColorList(): string[] {
    return [
        "white",
        "purple",
        "cyan",
        "golden",
        "green",
        "red",
        "blue",
    ]
}

export type AppVariableStore = { [key: string]: AppVariable }
export type AppKvStrStore = { [key: string]: string }

export interface AppVariableEventStore extends AppButtonInfoTypeRefreshExecuteInfo {
    variables: string[]
}

export type ExecuteType = "send" | "send_variable" | "js" | "js_variable" | "py" | "py_variable" | "shell" | "shell_variable"

export interface AppButtonTypeButtonExecute {
    type: ExecuteType
    value: string
}

export interface AppVariable {
    values: string[]
    options: string[]
}

export type AppButtonInfoType = AppButtonTypeButton | AppButtonTypeRadio | AppButtonTypeCheckbox | AppButtonTypeSelect | AppButtonTypeInput | AppButtonTypeText | AppButtonTypeVariableText | AppButtonTypeMarkdown | AppButtonTypeHtml | AppButtonTypeBlank | AppButtonTypeLine | AppButtonTypeMultipleButton

export interface AppButtonInfoTypeVariableInfo {
    variableName: string
    historyVariableValue: boolean
}

export interface AppButtonInfoTypeRefreshExecuteInfo {
    refreshType: "" | "js" | "js_variable" | "py" | "py_variable" | "shell" | "shell_variable"
    refreshValue: string
}

export interface AppButtonInfoTypeRefreshInfo extends AppButtonInfoTypeRefreshExecuteInfo {
    refreshShow: "hide" | "fixed" | "focus"
    // refreshOnStart: boolean // todo 打开时更新
    // refreshInterval: number // todo 间隔更新
    refreshOfVariables: string[]
}

export interface AppButtonInfoTypeWidth {
    width: number
}

export interface AppButtonShowConfig {
    full?: boolean
}

export interface AppButtonEditConfig {
    width?: boolean
    minWidth?: number
    widthTitle?: string
    notMargin?: boolean
    disableColor?: boolean
    refreshVariable?: boolean
    historyVariableValue?: boolean
}

export interface AppButtonInfoTypeWidthEdit {
    width: WritableComputedRef<number, number>

    getMinWidth(): number
}

export type TypeButtonInfoType = "button" | "radio" | "checkbox" | "select" | "input" | "text" | "variable_text" | "markdown" | 'html' | 'blank' | 'line' | 'multiple_button' | 'config_multiple_button'
export type TypeButtonInfoColor = "white" | "purple" | "cyan" | "golden" | "green" | "red" | "blue"

export interface AppButtonInfo<AppButtonInfoType> {
    linkage: string
    linkage_type: 'value_true' | 'value_false'
    beforeMargin: number
    afterMargin: number
    type: TypeButtonInfoType
    color: TypeButtonInfoColor
    buttonInfo: AppButtonInfoType
    // buttonInfo?: AppButtonTypeButton
    // radioInfo?: AppButtonTypeRadio
    // checkboxInfo?: AppButtonTypeCheckbox
    // selectInfo?: AppButtonTypeSelect
    // inputInfo?: AppButtonTypeInput
    // textInfo?: AppButtonTypeText
    // markdownInfo?: AppButtonTypeMarkdown
}


export interface AppButtonTypeButton extends AppButtonTypeButtonExecute {
    title: string
    width: number

}

export interface AppButtonTypeMultipleButton extends AppButtonTypeButtonExecute, AppButtonInfoTypeVariableInfo {
    width: number
}

export interface AppButtonTypeConfigMultipleButton {
    width: number
    configType: "" | "yaml"
    configValue: string
}

export interface AppButtonTypeConfigMultipleButtonExecuteInfo extends AppButtonTypeButtonExecute {
    name: string
    disableReplace: boolean
    replaceVariable: string[]
    disableEnter: boolean
}

export interface AppButtonTypeRadio extends AppButtonInfoTypeVariableInfo, AppButtonInfoTypeRefreshInfo {
    width: number
}

export interface AppButtonTypeCheckbox extends AppButtonInfoTypeVariableInfo, AppButtonInfoTypeRefreshInfo {
    width: number
}

export interface AppButtonTypeSelect extends AppButtonInfoTypeVariableInfo, AppButtonInfoTypeRefreshInfo {
    width: number
}

export interface AppButtonTypeInput extends AppButtonInfoTypeVariableInfo, AppButtonInfoTypeRefreshInfo {
    width: number
    showType: "" | "number"
}

export interface AppButtonTypeText {
    text: string
}

export interface AppButtonTypeVariableText extends AppButtonInfoTypeVariableInfo, AppButtonInfoTypeRefreshInfo {
    width: number
}

export interface AppButtonTypeMarkdown {
    markdown: string
}

export interface AppButtonTypeHtml {
    html: string
}

export interface AppButtonTypeBlank {
    width: number
}

export interface AppButtonTypeLine {
    width: number
}