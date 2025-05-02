import {AppButtonEditConfig, AppButtonInfo, AppButtonInfoType, AppButtonInfoTypeRefreshInfo, AppButtonInfoTypeVariableInfo, AppButtonInfoTypeWidthEdit, AppKvStrStore, AppVariableEventStore, AppVariableStore} from "./AppButton.ts";

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
    hideToolbelt?: boolean
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

export interface AppExecuteVariableContextOfJs {
    getValue: (key: string) => string
    setValue: (key: string, value: string) => void
    getValues: (key: string) => string[]
    setValues: (key: string, value: string[]) => void
    getOptions: (key: string) => string[]
    setOptions: (key: string, value: string[]) => void
}

export interface AppExecuteJsContextOfJs {
    execute: (name: string, ...args: any[]) => any
}

export interface AppExecutePyContextOfJs {
    execute: (name: string, ...args: any[]) => string
}

export interface AppExecuteShellContextOfJs {
    execute: (name: string, ...args: any[]) => string
}

export interface AppExecuteFuncContextOfJs {
    sendText: (text: string) => void
}

export interface AppExecuteKeyInfo {
    command: boolean
    option: boolean
    control: boolean
    shift: boolean
    key: string
    code: string
}

export interface AppExecuteContext {
    jsContext: AppExecuteJsContext
    executeVariable: AppExecuteVariable
    execute: AppExecute
    keyboard: AppExecuteKeyInfo
}

export interface AppExecute {
    sendText: (str: string) => void
    sendTextWithVariable: (name: string) => void
    executeJs: (str: string) => void
    executeJsWithConfig: (name: string) => void
    executePy: (str: string) => void
    executePyWithConfig: (name: string) => void
    executeShell: (str: string) => void
    executeShellWithConfig: (name: string) => void
}

export interface AppExecuteJsContext {
    VARIABLE: AppExecuteVariableContextOfJs
    JS: AppExecuteJsContextOfJs
    PY: AppExecutePyContextOfJs
    SHELL: AppExecuteShellContextOfJs
    FUNC: AppExecuteFuncContextOfJs
    KEYBOARD: AppExecuteKeyInfo
}

export interface AppExecuteVariable {
    variable: AppVariableStore
    variable_event: AppVariableEventStore[]
    shell: AppKvStrStore
    js: AppKvStrStore
    py: AppKvStrStore
    event: AppKvStrStore
}


export interface AppConfig extends AppExecuteVariable {
    tabs: AppTab[]
    toolbelt: AppToolbelt
}
