import type {Component} from 'vue';
import AppButton from "./button/AppButton.vue";
import AppRadio from "./button/AppRadio.vue";
import AppCheckbox from "./button/AppCheckbox.vue";
import AppSelect from "./button/AppSelect.vue";
import AppInput from "./button/AppInput.vue";
import AppText from "./button/AppText.vue";
import AppVariableText from "./button/AppVariableText.vue";
import AppMarkdown from "./button/AppMarkdown.vue";
import type {AppButtonEditConfig, AppButtonInfo, AppButtonInfoType, AppButtonShowConfig, AppButtonTypeBlank, AppButtonTypeButton, AppButtonTypeCheckbox, AppButtonTypeConfigMultipleButton, AppButtonTypeHtml, AppButtonTypeInput, AppButtonTypeLine, AppButtonTypeMarkdown, AppButtonTypeMultipleButton, AppButtonTypeRadio, AppButtonTypeSelect, AppButtonTypeText, AppButtonTypeVariableText} from "../types/AppButton.ts";
import AppHtml from "./button/AppHtml.vue";
import AppLine from "./button/AppLine.vue";
import AppBlank from "./button/AppBlank.vue";
import AppMultipleButton from "./button/AppMultipleButton.vue";
import AppConfigMultipleButton from "@/components/button/AppConfigMultipleButton.vue";

interface AppButtonComponent {
    handler: Component
    name: string
    showConfig: AppButtonShowConfig
    editConfig: AppButtonEditConfig
    init: () => AppButtonInfo<AppButtonInfoType>
}

export const componentMap = <{ [key: string]: AppButtonComponent }>{
    'button': {
        handler: AppButton,
        name: '按钮',
        showConfig: {},
        editConfig: {
            width: true,
        },
        init: () => {
            return {
                type: "button",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeButton>{
                    title: "Button",
                },
            }
        }
    },
    'multiple_button': {
        handler: AppMultipleButton,
        name: '动态按钮',
        showConfig: {},
        editConfig: {
            width: true,
        },
        init: () => {
            return {
                type: "multiple_button",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeMultipleButton>{
                    variableName: "",
                },
            }
        }
    },
    'config_multiple_button': {
        handler: AppConfigMultipleButton,
        name: '配置按钮',
        showConfig: {},
        editConfig: {
            width: true,
        },
        init: () => {
            return {
                type: "config_multiple_button",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeConfigMultipleButton>{
                    configType: "",
                    configValue:"",
                },
            }
        }
    },
    'radio': {
        handler: AppRadio,
        name: '单选',
        showConfig: {},
        editConfig: {
            width: true,
            minWidth: 5,
            widthTitle: "最大宽度",
            refreshVariable: true,
        },
        init: () => {
            return {
                type: "radio",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeRadio>{
                    variableName: "",
                },
            }
        }
    },
    'checkbox': {
        handler: AppCheckbox,
        name: '多选',
        showConfig: {},
        editConfig: {
            width: true,
            minWidth: 5,
            widthTitle: "最大宽度",
            refreshVariable: true,
        },
        init: () => {
            return {
                type: "checkbox",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeCheckbox>{
                    variableName: "",
                },
            }
        }
    },
    'select': {
        handler: AppSelect,
        name: '下拉框',
        showConfig: {},
        editConfig: {
            width: true,
            refreshVariable: true,
            historyVariableValue: true,
        },
        init: () => {
            return {
                type: "select",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeSelect>{
                    variableName: "",
                },
            }
        }
    },
    'input': {
        handler: AppInput,
        name: '输入框',
        showConfig: {},
        editConfig: {
            width: true,
            refreshVariable: true,
            historyVariableValue: true,
        },
        init: () => {
            return {
                type: "input",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeInput>{
                    variableName: "",
                },
            }
        }
    },
    'text': {
        handler: AppText,
        name: '文本',
        showConfig: {},
        editConfig: {},
        init: () => {
            return {
                type: "text",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeText>{
                    text: "Text",
                },
            }
        }
    },
    'variable_text': {
        handler: AppVariableText,
        name: '变量文本',
        showConfig: {},
        editConfig: {},
        init: () => {
            return {
                type: "variable_text",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeVariableText>{
                    variableName: "",
                },
            }
        }
    },
    'markdown': {
        handler: AppMarkdown,
        name: 'markdown',
        showConfig: {
            full: true
        },
        editConfig: {},
        init: () => {
            return {
                type: "markdown",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeMarkdown>{
                    markdown: "Markdown",
                },
            }
        }
    },
    'html': {
        handler: AppHtml,
        name: "html",
        showConfig: {
            full: true
        },
        editConfig: {
            disableColor: true,
        },
        init: () => {
            return {
                type: "html",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeHtml>{
                    html: "",
                }
            }
        }
    },
    "blank": {
        handler: AppBlank,
        name: "间隔",
        showConfig: {},
        editConfig: {
            width: true,
            minWidth: 0.2,
            disableColor: true,
        },
        init: () => {
            return {
                type: "blank",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeBlank>{
                    width: 2,
                }
            }
        }
    },
    "line": {
        handler: AppLine,
        name: "换行",
        showConfig: {
            full: true
        },
        editConfig: {
            width: true,
            minWidth: 0.1,
            widthTitle: "高度",
            disableColor: true,
        },
        init: () => {
            return {
                type: "line",
                linkage: "",
                linkage_type: "value_true",
                afterMargin: 0,
                beforeMargin: 0,
                color: "white",
                buttonInfo: <AppButtonTypeLine>{
                    width: 0.2,
                }
            }
        }
    }
};