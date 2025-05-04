import {AppConfig, AppStatus, AppVariableHistoryStore} from "../types/AppConfig";
import type {AppButtonTypeButton, AppButtonTypeCheckbox, AppButtonTypeInput, AppButtonTypeRadio, AppButtonTypeSelect} from "../types/AppButton.ts";
import {getConfig, saveConfig} from "@/api/config.ts";


export function getAppStatus(): AppStatus {
    let item = localStorage.getItem("appStatus");
    if (item) {
        return JSON.parse(item);
    }
    return {
        index: 0,
        fullScreenInputTypeTextarea: false,
        hideToolbelt: false,
        toolbeltHeight: 150
    }
}

export function setAppStatus(appStatus: AppStatus) {
    localStorage.setItem("appStatus", JSON.stringify(appStatus));
}


export function getAppVariableHistoryStore(): AppVariableHistoryStore {
    let item = localStorage.getItem("appVariableHistory");
    if (item) {
        return JSON.parse(item);
    }
    return {}
}

export function setAppVariableHistoryStore(appStatus: AppVariableHistoryStore) {
    localStorage.setItem("appVariableHistory", JSON.stringify(appStatus));
}


export function getAppConfig(): AppConfig {
    const config = getConfig()
    if (config.tabs == undefined) {
        config.tabs = []
        config.variable = {}
        config.variable_event = []
        config.shell = {}
        config.js = {}
        config.py = {}
        config.event = {}
    }
    return config
}

export function setAppConfig(appConfig: AppConfig) {
    saveConfig(appConfig);
}