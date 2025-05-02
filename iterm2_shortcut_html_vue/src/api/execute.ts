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
    //todo
    console.log(`jsContext 执行py`, code, args)
    return ""
}

export function executeShell(code: string, ...args: any[]): string {
    //todo
    console.log(`jsContext 执行shell`, code, args)
    return ""
}

export function sendHttp(httpRequest: HttpRequest): HttpResponse {
    return commonSendHttp({
        url: "/api/proxy",
        method: "POST",
        data: httpRequest,
    })
}

export interface HttpRequest {
    url: string
    method: string
    headers?: { [key: string]: any }
    params?: { [key: string]: any }
    data?: any
}

export interface HttpResponse {
    status: boolean
    message: string
    data?: any
}


function commonSendHttp(httpRequest: HttpRequest): HttpResponse {
    const xhr = new XMLHttpRequest();
    xhr.open(httpRequest.method, httpRequest.url, false);
    xhr.setRequestHeader("Content-Type", "application/json");
    for (const header in httpRequest.headers) {
        xhr.setRequestHeader(header, httpRequest.headers[header]);
    }
    try {
        xhr.send(JSON.stringify(httpRequest.data));
        if (xhr.status >= 200 && xhr.status < 300) {
            const data = JSON.parse(xhr.responseText);
            return {status: true, message: '成功', data: data};
        } else {
            return {status: false, message: `请求失败: 状态码 ${xhr.status}`};
        }
    } catch (error) {
        console.error('HTTP 请求出错:', error);
        return {status: false, message: '请求失败: ' + error};
    }
}