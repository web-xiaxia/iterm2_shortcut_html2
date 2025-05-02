import type {AppSessionStatus, ButtonProps} from "./AppConfig.ts";
import type {AppButtonInfoTypeWidth, AppButtonInfoTypeWidthEdit} from "./AppButton.ts";


export function handleMouseenterEditWidth(event: MouseEvent, props: ButtonProps<AppButtonInfoTypeWidth>) {
    handleMouseenterEditWidthWithTypeWidthEdit(event, props.appSessionStatus, <AppButtonInfoTypeWidthEdit>{
        width: {
            get value(): number {
                return props.button.buttonInfo.width
            },
            set value(newVal: number) {
                props.button.buttonInfo.width = newVal
            }
        },
        getMinWidth(): number {
            return props.editConfig.minWidth || 1
        }
    })
}

export function handleMouseenterEditWidthWithTypeWidthEdit(event: MouseEvent, appSessionStatus: AppSessionStatus, editWidth: AppButtonInfoTypeWidthEdit) {
    if (!appSessionStatus.editWidth) {
        return
    }
    appSessionStatus.editWidthNow = editWidth
    if (event.target) {
        appSessionStatus.editWidthTarget = event.target as HTMLElement
    }

}

export function handleMouseoutEditWidth(appSessionStatus: AppSessionStatus) {
    appSessionStatus.editWidthNow = undefined
    appSessionStatus.editWidthTarget = undefined
}

export function getEditWidthNowWidth(appSessionStatus: AppSessionStatus): number {
    if (!appSessionStatus.editWidthNow || !appSessionStatus.editWidthTarget) {
        return 0
    }
    let nowWidth = appSessionStatus.editWidthNow.width.value || 0
    if (nowWidth > 0) {
        return nowWidth
    }
    // // 获取当前DOM元素（假设是事件触发的元素）
    const currentElement = appSessionStatus.editWidthTarget; // 或者 document.getElementById('yourId') 等其他选择方法
    // 获取元素的宽度（像素值）
    const widthInPx = currentElement.offsetWidth;
    // 获取元素的计算样式中的字体大小（这将返回像素值）
    const fontSizeInPx = parseFloat(window.getComputedStyle(currentElement, null).getPropertyValue('font-size'));
    // 将宽度转换为em
    return widthInPx / fontSizeInPx;
}

export function handleEditWidth(key: string, appSessionStatus: AppSessionStatus) {
    if (!appSessionStatus.editWidth) {
        return
    }
    key = key.toLowerCase()
    if (!appSessionStatus.editWidthNow || !appSessionStatus.editWidthTarget) {
        return
    }
    if (key === 'r') {
        appSessionStatus.editWidthNow.width.value = 0
        return;
    }
    const editWidthMap = <{ [ket: string]: number }>{
        "q": -0.1,
        "w": 0.1,
        "a": -1,
        "s": 1,
    }
    const editWidth = editWidthMap[key]
    if (!editWidth) {
        return;
    }
    const nowWidth = getEditWidthNowWidth(appSessionStatus)
    const newWidth = nowWidth + editWidth
    if (newWidth > 0) {
        const minWidth = appSessionStatus.editWidthNow.getMinWidth()
        if (newWidth <= minWidth) {
            appSessionStatus.editWidthNow.width.value = minWidth
        } else {
            appSessionStatus.editWidthNow.width.value = newWidth
        }
    }
}