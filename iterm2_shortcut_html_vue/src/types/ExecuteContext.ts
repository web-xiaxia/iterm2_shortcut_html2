import {ComputedRef, ref} from "vue";
import {AppExecuteContext, AppExecuteJsContext, AppExecuteKeyInfo, AppExecuteVariable, type AppSessionStatus} from "@/types/AppConfig.ts";
import {safeExecuteJs} from "@/utils/executeJs.ts";
import {executePy, executeShell, sendText} from "@/api/execute.ts";


export function newAppExecuteContext(appSessionStatus: ComputedRef<AppSessionStatus>, executeVariable: ComputedRef<AppExecuteVariable>): AppExecuteContext {
    const keyboardInfo = ref<AppExecuteKeyInfo>({
        command: false,
        option: false,
        control: false,
        shift: false,
        key: "",
        code: "",
    })
    const jsContext = <AppExecuteJsContext>{
        VARIABLE: {
            getValue: (key: string): string => {
                const variableInfo = executeVariable.value.variable[key]
                if (!variableInfo) {
                    return ""
                }
                const variableValues = variableInfo.values
                if (!variableValues || variableValues.length == 0) {
                    return ""
                }
                return variableValues[variableValues.length - 1]
            },
            setValue: (key: string, value: string): void => {
                const variableInfo = executeVariable.value.variable[key]
                if (!variableInfo) {
                    executeVariable.value.variable[key] = {
                        values: [value],
                        options: []
                    }
                } else {
                    variableInfo.values = [value]
                }
            },
            getValues: (key: string): string[] => {
                const variableInfo = executeVariable.value.variable[key]
                if (!variableInfo) {
                    return []
                }
                const variableValues = variableInfo.values
                if (!variableValues || variableValues.length == 0) {
                    return []
                }
                return variableValues
            },
            setValues: (key: string, value: string[]): void => {
                const variableInfo = executeVariable.value.variable[key]
                if (!variableInfo) {
                    executeVariable.value.variable[key] = {
                        values: value,
                        options: []
                    }
                } else {
                    variableInfo.values = value
                }
            },
            getOptions: (key: string): string[] => {
                const variableInfo = executeVariable.value.variable[key]
                if (!variableInfo) {
                    return []
                }
                const variableValues = variableInfo.options
                if (!variableValues || variableValues.length == 0) {
                    return []
                }
                return variableValues
            },
            setOptions: (key: string, value: string[]): void => {
                const variableInfo = executeVariable.value.variable[key]
                if (!variableInfo) {
                    executeVariable.value.variable[key] = {
                        values: [],
                        options: value
                    }
                } else {
                    variableInfo.options = value
                }
            },
        },
        JS: {
            execute: (name: string, ...args: any[]): any => {
                // 已完成在下方
                console.log(`jsContext 执行js`, name, args)
                return ""
            }
        },
        PY: {
            execute: (name: string, ...args: any[]): string => {
                const jsText = executeVariable.value.py[name]
                if (!jsText) {
                    return ""
                }
                return executePy(jsText, ...args)
            }
        },
        SHELL: {
            execute: (name: string, ...args: any[]): string => {
                const jsText = executeVariable.value.shell[name]
                if (!jsText) {
                    return ""
                }
                return executeShell(jsText, ...args)
            }
        },
        FUNC: {
            sendText: sendText,
        },
        KEYBOARD: keyboardInfo.value,
    }
    jsContext.JS.execute = (name: string, ...args: any[]): any => {
        const jsText = executeVariable.value.js[name]
        if (!jsText) {
            return undefined
        }
        console.log(`jsContext 执行js`, name, args)
        // 可以在这里注入自定义变量和函数
        const injectedEnvironment = {
            "APP": jsContext,
        };
        return safeExecuteJs(jsText, injectedEnvironment, ...args);
    }
    return {
        jsContext: jsContext,
        executeVariable: executeVariable.value,
        execute: {
            sendText: (name: string): void => {
                if (keyboardInfo.value.command && !appSessionStatus.value.showFullScreenInputModal) {
                    appSessionStatus.value.fullScreenInputValue = name
                    appSessionStatus.value.showFullScreenInputModal = true
                    return
                }
                sendText(name)
            },
            sendTextWithVariable: (name: string): void => {
                const values = executeVariable.value.variable[name]?.values
                if (values && values.length > 0) {
                    const sendTextVal = values[values.length - 1]
                    if (keyboardInfo.value.command && !appSessionStatus.value.showFullScreenInputModal) {
                        appSessionStatus.value.fullScreenInputValue = sendTextVal
                        appSessionStatus.value.showFullScreenInputModal = true
                        return
                    }
                    sendText(sendTextVal)
                }
            },
            executeJs: (str: string): void => {
                console.log("execute js: ", str)
                safeExecuteJs(str, {
                    "APP": jsContext,
                })
            },
            executeJsWithConfig: (name: string): void => {
                const value = executeVariable.value.js[name]
                if (value && value.length > 0) {
                    console.log("execute js: ", value)
                }
            },
            executePy: (str: string): void => {
                executePy(str)
            },
            executePyWithConfig: (name: string): void => {
                const value = executeVariable.value.py[name]
                if (value && value.length > 0) {
                    executePy(value)
                }
            },
            executeShell: (str: string): void => {
                executeShell(str)
            },
            executeShellWithConfig: (name: string): void => {
                const value = executeVariable.value.shell[name]
                if (value && value.length > 0) {
                    executeShell(value)
                }
            }
        },
        keyboard: keyboardInfo.value,
    }
}