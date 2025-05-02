import type {AppButtonTypeButtonTypeInfo, AppExecuteContext, AppExecuteVariable} from "../types/AppConfig.ts";


export const AppButtonTypeButtonTypeList = <AppButtonTypeButtonTypeInfo[]>[{
    key: "send",
    name: "发送文本",
    title: "文本内容",
    inputType: "textarea",
    send: (executeContext: AppExecuteContext, executeValue: string) => {
        executeContext.exec.sendText(executeValue,"fullScreenInput")
    },
    getOptions: () => []
}, {
    key: "send_variable",
    name: "发送变量文本",
    title: "变量",
    inputType: "variable",
    send: (executeContext: AppExecuteContext, executeValue: string) => {
        executeContext.exec.sendTextWithVariable(executeValue,"fullScreenInput")
    },
    getOptions: (appConfig: AppExecuteVariable) => Object.keys(appConfig.variable)
}, {
    key: "js",
    name: "执行文本js",
    title: "js代码",
    inputType: "textarea",
    send: (executeContext: AppExecuteContext, executeValue: string) => {
        executeContext.exec.executeJs(executeValue)
    },
    getOptions: () => []
}, {
    key: "js_variable",
    name: "执行配置js",
    title: "配置名称",
    inputType: "variable",
    send: (executeContext: AppExecuteContext, executeValue: string) => {
        executeContext.exec.executeJsWithConfig(executeValue)
    },
    getOptions: (appConfig: AppExecuteVariable) => Object.keys(appConfig.js)
}, {
    key: "py",
    name: "执行文本py",
    title: "py代码",
    inputType: "textarea",
    send: (executeContext: AppExecuteContext, executeValue: string) => {
        executeContext.exec.executePy(executeValue)
    },
    getOptions: () => []
}, {
    key: "py_variable",
    name: "执行配置py",
    title: "配置名称",
    inputType: "variable",
    send: (executeContext: AppExecuteContext, executeValue: string) => {
        executeContext.exec.executePyWithConfig(executeValue)
    },
    getOptions: (appConfig: AppExecuteVariable) => Object.keys(appConfig.py)
}, {
    key: "shell",
    name: "执行文本shell",
    title: "shell代码",
    inputType: "textarea",
    send: (executeContext: AppExecuteContext, executeValue: string) => {
        executeContext.exec.executeShell(executeValue)
    },
    getOptions: () => []
}, {
    key: "shell_variable",
    name: "执行配置shell",
    title: "配置名称",
    inputType: "variable",
    send: (executeContext: AppExecuteContext, executeValue: string) => {
        executeContext.exec.executeShellWithConfig(executeValue)
    },
    getOptions: (appConfig: AppExecuteVariable) => Object.keys(appConfig.shell)
}]
export const AppButtonTypeButtonTypeMap = new Map<string, AppButtonTypeButtonTypeInfo>(AppButtonTypeButtonTypeList.map(item => [item.key, item]));
