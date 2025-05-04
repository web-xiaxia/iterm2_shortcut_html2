import {commonSendHttp, type HttpRequest, type HttpResponse} from '@/api/common.ts'
import {AppConfig} from "@/types/AppConfig.ts";


export function getConfig(): AppConfig {
    return commonSendHttp({
        url: "/api/storage",
        method: "GET",
        data: {},
    }).data as AppConfig
}

export function saveConfig(conf: AppConfig) {
    return commonSendHttp({
        url: "/api/storage",
        method: "POST",
        data: conf,
    })
}

export interface SettingsSystemConfig {
    window_width: number
    window_height: number
}

export function getSystemConfig(): SettingsSystemConfig {
    let config = commonSendHttp({
        url: "/api/system_config",
        method: "GET",
        data: {},
    }).data as SettingsSystemConfig
    if (!config) {
        config = {
            window_height: 480,
            window_width: 950
        }
    }
    if (!config.window_height) {
        config.window_height = 480
    }
    if (!config.window_width) {
        config.window_width = 950
    }
    return config
}

export function saveSystemConfig(data: SettingsSystemConfig) {
    return commonSendHttp({
        url: "/api/system_config",
        method: "POST",
        data: data,
    })
}
