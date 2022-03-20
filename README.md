## 项目介绍
```
iTerm2 自带的 Status Bar 可以添加按钮，但是显示范围太小，可添加的按钮数较少，无法进行分组
本项目使用 iTerm2 的 Python API 在 Status Bar 添加一个按钮，点击按钮后显示一个html，进行按钮分组显示和编辑，适用于像我这种记不住命令的同学。
```
## 展示图
![image](https://raw.githubusercontent.com/web-xiaxia/iterm2_shortcut_html2/main/iterm2_shortcut_html2/html/image/readme.gif)

## 安装方法
```
1. 在iTerm2开启脚本支持环境
1.1. 点击菜单栏iTerm2->Preferences->General->Magic->Enable Python API
1.2. 点击菜单栏Scripts->Manage->Install Python Runtime

2. 安装插件环境
2.1. 点击菜单栏Scripts->Manage->New Python Script
2.2. 在弹框中选择Full Environment->Long-Running Daemon
2.3. 选择Scripts目录中的AutoLaunch(如果没有自己创建)
2.4. 在名称框中输入iterm2_shortcut_html2
2.5. 在PyPI Dependencies中输入setup.cfg文件中的install_requires的内容
2.6. 在Python Version中选择3.7.9
2.7. 点击保存

3. 安装插件
3.1 执行 mv ~/Library/Application\ Support/iTerm2/Scripts/AutoLaunch/iterm2_shortcut_html2/iterm2env ~/Library/Application\ Support/iTerm2/Scripts/AutoLaunch/
3.2 执行 rm -rf ~/Library/Application\ Support/iTerm2/Scripts/AutoLaunch/iterm2_shortcut_html2
3.3 执行 mv [[项目本地路径]] ~/Library/Application\ Support/iTerm2/Scripts/AutoLaunch/iterm2_shortcut_html2
3.4 执行 mv ~/Library/Application\ Support/iTerm2/Scripts/AutoLaunch/iterm2env ~/Library/Application\ Support/iTerm2/Scripts/AutoLaunch/iterm2_shortcut_html2/iterm2env
3.5 重新启动 iTerm2

4. 使用插件
4.1 在 Profiles 中选择一个 Profile 选择 Session Tab 在最下面勾选 Status bar enabled 点击 Configure Status Bar
4.2 在 Status Bar 添加 Shortcut html2 到 Status Bar 点击保存
4.3 可以在 Appearance 中的 General Tab 中可以设置 Status bar location 为 Bottom，按钮在窗口下面

```
