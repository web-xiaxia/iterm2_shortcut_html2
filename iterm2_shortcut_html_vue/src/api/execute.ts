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