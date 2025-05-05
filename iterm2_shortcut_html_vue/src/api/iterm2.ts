import {commonSendHttp} from "@/api/common.ts";

export function iterm2_alert(message: string) {
    commonSendHttp({
        url: "/api/iterm2_alert",
        method: "POST",
        data: {
            'title': message,
            'subtitle': ""
        },
    })
}

export function iterm2_confirm(message: string) {
    return commonSendHttp({
        url: "/api/iterm2_confirm",
        method: "POST",
        data: {
            'title': message,
            'subtitle': ""
        },
    }).status
}
export function iterm2_prompt(message: string):string {
    return commonSendHttp({
        url: "/api/iterm2_prompt",
        method: "POST",
        data: {
            'title': message,
            'subtitle': ""
        },
    }).data as string
}