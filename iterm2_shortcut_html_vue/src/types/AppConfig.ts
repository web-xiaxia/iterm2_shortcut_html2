import {AppButtonEditConfig, AppButtonInfo, AppButtonInfoType, AppButtonInfoTypeRefreshInfo, AppButtonInfoTypeVariableInfo, AppButtonInfoTypeWidthEdit, AppButtonTypeButtonExecute, AppKvStrStore, AppVariableEventStore, AppVariableStore} from "./AppButton.ts";
import {HttpRequest, HttpResponse} from "@/api/common.ts";

export interface AppButtonTypeButtonTypeInfo {
    key: string
    name: string
    title: string
    inputType: "input" | "textarea" | "variable"
    send: (executeContext: AppExecuteContext, executeValue: string) => void
    getOptions: (appConfig: AppExecuteVariable) => string[]
}

export interface AppButtonVariableRefreshInfo {
    key: string
    name: string
    title: string
    inputType: "input" | "textarea" | "variable"
    refresh: (executeContext: AppExecuteContext, refreshValue: string) => void
    getOptions: (appConfig: AppExecuteVariable) => string[]
}

export interface AppStatus {
    index: number
    hideToolbelt: boolean
    toolbeltHeight: number
    fullScreenInputTypeTextarea: boolean
}

export interface AppSessionStatus {
    appMode: "show" | "settings"
    editWidth: boolean
    showFullScreenInputModal: boolean
    fullScreenInputValue: string
    editWidthNow?: AppButtonInfoTypeWidthEdit
    editWidthTarget?: HTMLElement
    editSettings?: boolean
}


export interface ButtonProps<AppButtonInfoType> {
    button: AppButtonInfo<AppButtonInfoType>
    appStatus: AppStatus
    appSessionStatus: AppSessionStatus
    executeContext: AppExecuteContext
    editConfig: AppButtonEditConfig
}

export interface ButtonEditorCommonProps {
    buttonProps: ButtonProps<AppButtonInfoType>
}

export interface ButtonEditorVariableProps {
    buttonProps: ButtonProps<AppButtonInfoTypeVariableInfo>
}

export interface ButtonEditorRefreshProps {
    buttonProps: ButtonProps<AppButtonInfoTypeRefreshInfo>
}

export interface ButtonEditorButtonTypeProps {
    buttonProps: ButtonProps<AppButtonTypeButtonExecute>
}


export interface AppGroup {
    fontLevel: number
    buttons: AppButtonInfo<AppButtonInfoType>[]
}

export interface AppTab {
    title: string
    model?: 'toolbelt'
    hide?: boolean
    buttonGroups: AppGroup[]
}

export interface AppToolbelt {
    height: number
}

export interface AppVariableHistoryInfo {
    lastUpdateTime: number
    values: string[]
}

export type AppVariableHistoryStore = { [key: string]: AppVariableHistoryInfo }


export interface AppExecuteKeyInfo {
    command: boolean
    option: boolean
    control: boolean
    shift: boolean
    key: string
    code: string
}

export interface AppExecute {
    sendText: (text: string, ...args: any[]) => void
    sendTextWithVariable: (name: string, ...args: any[]) => void
    executeJs: (text: string, ...args: any[]) => any
    executeJsWithConfig: (name: string, ...args: any[]) => any
    executePy: (text: string) => string
    executePyWithConfig: (name: string, ...args: any[]) => string
    executeShell: (text: string) => string
    executeShellWithConfig: (name: string) => string
    sendHttp: (req: HttpRequest) => HttpResponse | any
}

export interface AppExecuteContextBase {
    variable: AppExecuteVariableTool
    exec: AppExecute
    keyboard: AppExecuteKeyInfo
}

export interface AppExecuteContext extends AppExecuteContextBase {
    jsContext: AppExecuteJsContext
    executeVariable: AppExecuteVariable
}

export interface AppExecuteJsContext extends AppExecuteContextBase {
}

export interface AppExecuteVariableTool {
    getValue: (key: string) => string
    setValue: (key: string, value: string) => void
    getValues: (key: string) => string[]
    setValues: (key: string, value: string[]) => void
    getOptions: (key: string) => string[]
    setOptions: (key: string, value: string[]) => void
}

export interface AppExecuteConfig{
    shell: string
}
export interface AppExecuteVariable {
    variable: AppVariableStore
    variable_event: AppVariableEventStore[]
    shell: AppKvStrStore
    js: AppKvStrStore
    py: AppKvStrStore
    event: AppKvStrStore
    exec_config: AppExecuteConfig
}


export interface AppConfig extends AppExecuteVariable {
    tabs: AppTab[]
}
