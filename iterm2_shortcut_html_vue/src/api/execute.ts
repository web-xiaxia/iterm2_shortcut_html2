import {commonSendHttp, type HttpRequest, type HttpResponse} from '@/api/common.ts'

export function sendText(text: string): void {
    const resp = commonSendHttp({
        url: "/api/send_text",
        method: "POST",
        data: {
            "send_text": text,
        },
    })
    console.log(resp)
}


export function executePy(code: string, ...args: any[]): string {
    return commonSendHttp({
        url: "/api/exec_py",
        method: "POST",
        data: {
            "py": code,
            "params": args,
        },
    }).data as string
}

export function executeShell(code: string): string {
    return commonSendHttp({
        url: "/api/exec_shell",
        method: "POST",
        data: {
            "shell": code,
        },
    }).data as string
}

export function sendHttp(httpRequest: HttpRequest): HttpResponse {
    return commonSendHttp({
        url: "/api/proxy",
        method: "POST",
        data: httpRequest,
    })
}
