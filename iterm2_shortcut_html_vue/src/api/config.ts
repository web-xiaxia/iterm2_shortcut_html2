import {commonSendHttp, type HttpRequest, type HttpResponse} from '@/api/common.ts'
import {AppConfig} from "@/types/AppConfig.ts";

export interface SystemConfig {
    storage_path: string
}


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