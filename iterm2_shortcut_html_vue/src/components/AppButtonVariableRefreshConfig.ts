import type {AppButtonVariableRefreshInfo, AppExecuteContext, AppExecuteVariable} from "../types/AppConfig";

export const AppButtonVariableRefreshConfigList = <AppButtonVariableRefreshInfo[]>[{
    key: "js",
    name: "执行文本js",
    title: "js代码",
    inputType: "textarea",
    refresh: (executeContext: AppExecuteContext, refreshValue: string) => {
        executeContext.execute.executeJs(refreshValue)
    },
    getOptions: () => []
}, {
    key: "js_variable",
    name: "执行配置js",
    title: "配置名称",
    inputType: "variable",
    refresh: (executeContext: AppExecuteContext, refreshValue: string) => {
        executeContext.execute.executeJsWithConfig(refreshValue)
    },
    getOptions: (appConfig: AppExecuteVariable) => Object.keys(appConfig.js)
}, {
    key: "py",
    name: "执行文本py",
    title: "py代码",
    inputType: "textarea",
    refresh: (executeContext: AppExecuteContext, refreshValue: string) => {
        executeContext.execute.executePy(refreshValue)
    },
    getOptions: () => []
}, {
    key: "py_variable",
    name: "执行配置py",
    title: "配置名称",
    inputType: "variable",
    refresh: (executeContext: AppExecuteContext, refreshValue: string) => {
        executeContext.execute.executePyWithConfig(refreshValue)
    },
    getOptions: (appConfig: AppExecuteVariable) => Object.keys(appConfig.py)
}, {
    key: "shell",
    name: "执行文本shell",
    title: "shell代码",
    inputType: "textarea",
    refresh: (executeContext: AppExecuteContext, refreshValue: string) => {
        executeContext.execute.executeShell(refreshValue)
    },
    getOptions: () => []
}, {
    key: "shell_variable",
    name: "执行配置shell",
    title: "配置名称",
    inputType: "variable",
    refresh: (executeContext: AppExecuteContext, refreshValue: string) => {
        executeContext.execute.executeShellWithConfig(refreshValue)
    },
    getOptions: (appConfig: AppExecuteVariable) => Object.keys(appConfig.shell)
}]
export const AppButtonVariableRefreshConfigMap = new Map<string, AppButtonVariableRefreshInfo>(AppButtonVariableRefreshConfigList.map(item => [item.key, item]));