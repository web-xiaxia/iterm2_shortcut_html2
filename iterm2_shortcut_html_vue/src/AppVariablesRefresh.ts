import {computed, ref, watchEffect, type Ref, watch, UnwrapRef} from 'vue'
import {debounce} from 'lodash'
import {AppConfig, AppExecuteContext, AppVariableHistoryStore} from "@/types/AppConfig"
import {AppButtonInfoTypeRefreshExecuteInfo, AppButtonInfoTypeRefreshInfo} from "@/types/AppButton"
import {AppButtonVariableRefreshConfigMap} from "@/components/AppButtonVariableRefreshConfig"

export function appVariablesChange(appConfig: Ref<AppConfig>) {
    let needInitLastVariable = true
    const lastVariable = ref<{ [key: string]: any }>({})
    const changedVariables = ref<string[]>([])

    watchEffect(() => {
        const currentVariable = appConfig.value.variable||{}
        if (needInitLastVariable) {
            needInitLastVariable = false
            lastVariable.value = JSON.parse(JSON.stringify(currentVariable))
            return
        }

        const allKeys = new Set([
            ...Object.keys(currentVariable || {}),
            ...Object.keys(lastVariable.value || {})
        ])

        const changedKeys = Array.from(allKeys).filter((key: string) => {
            return JSON.stringify(currentVariable[key]) !== JSON.stringify(lastVariable.value[key])
        })

        if (changedKeys.length > 0) {
            changedVariables.value = changedKeys
        }
        lastVariable.value = JSON.parse(JSON.stringify(currentVariable))
    })
    return (f: (newVal: string[]) => void) => {
        const debouncedRefresh = debounce((changedKeys: string[]) => {
            f(changedKeys)
        }, 500)
        watch(changedVariables, (newVal) => {
            debouncedRefresh(newVal)
        })
    }
}

export function appVariablesRefreshFunc(
    appConfig: Ref<AppConfig>,
    appExecuteContext: AppExecuteContext
) {
    const needRefreshOfVariablesGroup = computed<Map<string, AppButtonInfoTypeRefreshExecuteInfo[]>>(() => {
        const ret = new Map<string, AppButtonInfoTypeRefreshExecuteInfo[]>()

        // 按钮自动刷新逻辑
        for (const tab of appConfig.value.tabs) {
            for (const group of tab.buttonGroups) {
                for (const button of group.buttons) {
                    const typeVariable = button.buttonInfo as AppButtonInfoTypeRefreshInfo
                    if (typeVariable.refreshType && typeVariable.refreshOfVariables) {
                        for (const ofVariable of typeVariable.refreshOfVariables) {
                            let typeVariableArr = ret.get(ofVariable)
                            if (!typeVariableArr) {
                                typeVariableArr = []
                                ret.set(ofVariable, typeVariableArr)
                            }
                            typeVariableArr.push(typeVariable)
                        }
                    }
                }
            }
        }

        // 设置项自动刷新逻辑
        for (const typeVariable of appConfig.value.variable_event) {
            for (const ofVariable of typeVariable.variables) {
                let typeVariableArr = ret.get(ofVariable)
                if (!typeVariableArr) {
                    typeVariableArr = []
                    ret.set(ofVariable, typeVariableArr)
                }
                typeVariableArr.push(typeVariable)
            }
        }
        return ret
    })
    return (changedKeys: string[]) => {
        console.log('变化的变量:', changedKeys)
        for (const key of changedKeys) {
            const typeVariableArr = needRefreshOfVariablesGroup.value?.get(key)
            typeVariableArr?.forEach(typeVariable => {
                AppButtonVariableRefreshConfigMap.get(typeVariable.refreshType)
                ?.refresh(appExecuteContext, typeVariable.refreshValue)
            })
        }
    }
}

export function appVariableHistoryFunc(appExecuteContext: AppExecuteContext, appVariableHistoryStore: Ref<AppVariableHistoryStore>) {
    return (newVal: string[]) => {
        for (const key of newVal) {
            const values = appExecuteContext.executeVariable.variable[key]?.values
            if (values && values.length > 0) {
                const value = "" + values[values.length - 1];
                if (!value || value.length === 0) {
                    continue
                }
                const appVariableHistory = appVariableHistoryStore.value[key]
                if (appVariableHistory) {
                    appVariableHistory.lastUpdateTime = new Date().getTime()
                    const arr = appVariableHistory.values.filter(item => item != value)
                    arr.unshift(value)
                    while (arr.length > 20) {
                        arr.pop()
                    }
                    appVariableHistory.values = arr
                } else {
                    appVariableHistoryStore.value[key] = {
                        lastUpdateTime: new Date().getTime(),
                        values: [value],
                    }
                }
            }
        }
    }
}