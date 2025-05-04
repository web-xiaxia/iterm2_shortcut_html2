
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


export function commonSendHttp(httpRequest: HttpRequest): HttpResponse {
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