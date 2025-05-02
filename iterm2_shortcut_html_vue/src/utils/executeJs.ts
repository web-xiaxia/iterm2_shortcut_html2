
export function safeExecuteJs(code: string, injectedVars: Record<string, any> = {}, ...args: any[]): any {
    try {
        // 处理代码
        const trimmedCode = code.trim();

        // 创建一个函数来执行代码
        let executionFunction: Function;

        // 为了支持传递函数和复杂对象，我们使用参数传递而不是字符串拼接
        if (/^function\s*\w*\s*\([^)]*\)\s*\{/.test(trimmedCode)) {
            // 函数定义 - 转换为可执行的函数
            executionFunction = new Function(
                ...Object.keys(injectedVars), // 变量名作为参数名
                `
                'use strict';
                const func = ${trimmedCode};
                return func(...${JSON.stringify(args)});
                `
            );
        } else if (trimmedCode.includes('\n') || trimmedCode.includes(';')) {
            // 多行代码或包含分号的代码
            // 检查最后一行是否有 return 语句
            if (!trimmedCode.trim().split(/[\n;]/).filter(line => line.trim()).pop()?.trim().startsWith('return')) {
                // 如果最后一行没有 return，添加一个默认的 return 语句
                executionFunction = new Function(
                    ...Object.keys(injectedVars), // 变量名作为参数名
                    `
                    'use strict';
                    ${trimmedCode}
                    return undefined;
                    `
                );
            } else {
                // 最后一行有 return
                executionFunction = new Function(
                    ...Object.keys(injectedVars), // 变量名作为参数名
                    `
                    'use strict';
                    ${trimmedCode}
                    `
                );
            }
        } else if (trimmedCode.startsWith('return ')) {
            // 单行 return 表达式
            executionFunction = new Function(
                ...Object.keys(injectedVars), // 变量名作为参数名
                `
                'use strict';
                ${trimmedCode}
                `
            );
        } else if (trimmedCode.startsWith('retrun ')) {
            // 处理拼写错误的 return
            const correctedCode = 'return ' + trimmedCode.substring(7);
            executionFunction = new Function(
                ...Object.keys(injectedVars), // 变量名作为参数名
                `
                'use strict';
                ${correctedCode}
                `
            );
        } else {
            // 普通表达式
            executionFunction = new Function(
                ...Object.keys(injectedVars), // 变量名作为参数名
                `
                'use strict';
                return (${trimmedCode});
                `
            );
        }

        // 执行函数，传入变量值
        return executionFunction(...Object.values(injectedVars));
    } catch (error) {
        console.error('JavaScript execution error:', error);
        return "";
    }
}

