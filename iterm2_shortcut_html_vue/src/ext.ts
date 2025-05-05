import {iterm2_alert, iterm2_confirm, iterm2_prompt} from "@/api/iterm2.ts";

window.alert = function (message) {
    iterm2_alert(message)
}
window.confirm = function (message) {
    return iterm2_confirm(message || "")
}
window.prompt = function (message, _default = "") {
    return iterm2_prompt(message || "")
}
