import {AppConfig, AppStatus, AppVariableHistoryStore} from "../types/AppConfig";
import type {AppButtonTypeButton, AppButtonTypeCheckbox, AppButtonTypeInput, AppButtonTypeRadio, AppButtonTypeSelect} from "../types/AppButton.ts";


export function getAppStatus(): AppStatus {
    let item = localStorage.getItem("appStatus");
    if (item) {
        return JSON.parse(item);
    }
    return {
        index: 0,
        fullScreenInputTypeTextarea: false,
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
    return {

    }
}

export function setAppVariableHistoryStore(appStatus: AppVariableHistoryStore) {
    localStorage.setItem("appVariableHistory", JSON.stringify(appStatus));
}



export function getAppConfig(): AppConfig {
    let item = localStorage.getItem("appConfig");
    if (item) {
        return JSON.parse(item);
    }
    return {
        tabs: [{
            title: "test1",
            buttonGroups: [{
                fontLevel: 1,
                buttons: [{
                    type: "input",
                    beforeMargin: 0,
                    afterMargin: 0,
                    color: "cyan",
                    linkage: "",
                    linkage_type: "value_true",
                    buttonInfo: <AppButtonTypeInput>{
                        variableName: "xxx",
                    },
                }, {
                    type: "radio",
                    beforeMargin: 0,
                    afterMargin: 0,
                    color: "cyan",
                    linkage: "",
                    linkage_type: "value_true",
                    buttonInfo: <AppButtonTypeRadio>{
                        variableName: "xxx",
                    }
                }, {
                    type: "checkbox",
                    beforeMargin: 0,
                    afterMargin: 0,
                    color: "cyan",
                    linkage: "",
                    linkage_type: "value_true",
                    buttonInfo: <AppButtonTypeCheckbox>{
                        variableName: "xxx",
                    }
                }, {
                    type: "select",
                    beforeMargin: 0,
                    afterMargin: 0,
                    color: "cyan",
                    linkage: "",
                    linkage_type: "value_true",
                    buttonInfo: <AppButtonTypeSelect>{
                        variableName: "xxx",
                    }
                }, {
                    type: "button",
                    beforeMargin: 0,
                    afterMargin: 0,
                    color: "cyan",
                    linkage: "",
                    linkage_type: "value_true",
                    buttonInfo: <AppButtonTypeButton>{
                        title: "test button",
                    }
                }],
            }]
        }, {
            title: "test1",
            buttonGroups: [{
                fontLevel: 3,
                buttons: [{
                    type: "button",
                    beforeMargin: 0,
                    afterMargin: 0,
                    color: "cyan",
                    linkage: "",
                    linkage_type: "value_true",
                    buttonInfo: <AppButtonTypeButton>{
                        title: "test button",
                        type: "send",
                        value: "",
                        width: 0,
                    }
                }],
            }]
        }],
        toolbelt: {
            height: 200,
        },
        variable: {
            "xxx": {
                values: ["xxx"],
                options: ["xxx", "xxx2"]
            }
        },
        variable_event: [],
        js: {},
        py: {},
        shell: {},
        event: {}
    }
}

export function setAppConfig(appConfig: AppConfig) {
    localStorage.setItem("appConfig", JSON.stringify(appConfig));
}