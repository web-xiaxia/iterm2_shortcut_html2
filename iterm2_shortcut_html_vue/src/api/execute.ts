export function sendText(text: string): void {
    console.log("sendText:", text);
}


export function executePy(code: string, ...args: any[]): string {
    //todo
    console.log(`jsContext 执行py`, code, args)
    return ""
}

export function executeShell(code: string, ...args: any[]): string {
    //todo
    console.log(`jsContext 执行shell`, code, args)
    return ""
}

export interface HttpRequest {
    url: string
    method: string
    headers: { [key: string]: any }
    params: { [key: string]: any }
    data: any
    jsonData: any
}

export interface HttpResponse {
    status: boolean
    message: string
}

export function sendHttp(httpRequest: HttpRequest): HttpResponse | any {
    let d = {"status": false, "message": "未成功"}
    //todo
    return d
}