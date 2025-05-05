import {ComputedRef, ref} from "vue";
import {AppExecuteContext, AppExecuteContextBase, AppExecuteJsContext, AppExecuteKeyInfo, AppExecuteVariable, AppExecuteVariableTool, type AppSessionStatus} from "@/types/AppConfig.ts";
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
    const variableTool = <AppExecuteVariableTool>{
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
    }

    const executeContextBase = <AppExecuteContextBase>{
        variable: variableTool,
        exec: {
            sendText: (name: string, ...args: any[]): void => {
                if (!name || name.length == 0) {
                    return;
                }
                if (args && args.length > 0) {
                    if (args[0] == "fullScreenInput") {
                        if (keyboardInfo.value.command && !appSessionStatus.value.showFullScreenInputModal) {
                            appSessionStatus.value.fullScreenInputValue = name
                            appSessionStatus.value.showFullScreenInputModal = true
                            return
                        }
                    }
                }
                sendText(name)
            },
            sendTextWithVariable: (name: string, ...args: any[]) => {
                const sendTextVal = variableTool.getValue(name)
                if (!sendTextVal || sendTextVal.length == 0) {
                    return;
                }
                if (args && args.length > 0) {
                    if (args[0] == "fullScreenInput") {
                        if (keyboardInfo.value.command && !appSessionStatus.value.showFullScreenInputModal) {
                            appSessionStatus.value.fullScreenInputValue = sendTextVal
                            appSessionStatus.value.showFullScreenInputModal = true
                            return
                        }
                    }
                }
                sendText(sendTextVal)
            },
            executeJs: (code: string, ...args: any[]): any => {
                // 已完成在下方
                console.log(`jsContext 执行js`, code, args)
                return ""
            },
            executeJsWithConfig: (name: string, ...args: any[]): any => {
                // 已完成在下方
                console.log(`jsContext 执行js`, name, args)
                return ""
            },
            executePy: executePy,
            executePyWithConfig: (name: string, ...args: any[]): string => {
                const jsText = executeVariable.value.py[name]
                if (!jsText || jsText.length == 0) {
                    return ""
                }
                return executePy(jsText, ...args)
            },
            executeShell: executeShell,
            executeShellWithConfig: (name: string): string => {
                const jsText = executeVariable.value.shell[name]
                if (!jsText || jsText.length == 0) {
                    return ""
                }
                return executeShell(jsText)
            },
        },
        keyboard: keyboardInfo.value,
    }
    executeContextBase.exec.executeJsWithConfig = (code: string, ...args: any[]): any => {
        console.log(`jsContext 执行js`, code, args)
        // 可以在这里注入自定义变量和函数
        const injectedEnvironment = {
            "APP": jsContext,
        };
        return safeExecuteJs(code, injectedEnvironment, ...args);
    }
    executeContextBase.exec.executeJsWithConfig = (name: string, ...args: any[]): any => {
        const jsText = executeVariable.value.js[name]
        if (!jsText || jsText.length == 0) {
            return undefined
        }
        return jsContext.exec.executeJsWithConfig(jsText, ...args)
    }


    const jsContext = <AppExecuteJsContext>{
        ...executeContextBase
    }

    return {
        ...executeContextBase,
        jsContext: jsContext,
        executeVariable: executeVariable.value,
    }
}