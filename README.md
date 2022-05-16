# B站(bilibili)实用脚本

## 已有脚本功能
- bilidanmaku.py: 直播区签到（获得2个辣条）、向有勋章的直播间发送弹幕（对应勋章获得100经验值）
- bilisignGroup.py: 已参加的应援团签到（对应勋章获得10经验值）

## 所需依赖
- python3 环境
- requests 包（需另行下载安装）

## 使用须知

本仓库中现有脚本均相互独立。

### 获取 cookie
**所有的脚本均需要这一步**。此步目的是获取自己的 cookie，也可以使用自己熟悉的方式获取。
1. 在浏览器中访问 [B站](https://www.bilibili.com) 并登录，打开浏览器的开发者工具（一般是按 F12 打开）
2. 找到并打开开发者工具中 Console 选项卡，复制粘贴以下代码并回车:

    ```js
    document
      .cookie
      .split(/\s*;\s*/)
      .map(it => it.split('='))
      .filter(it => ['DedeUserID','bili_jct', 'SESSDATA'].indexOf(it[0]) > -1)
      .map(it => it.join('='))
      .join('; ')
      .split()
      .forEach(it => copy(it) || console.log(it))
    ```

3. 复制输出的 `SESSDATA=...` 数据（共 3 项，分别为 `SESSDATA`、`bili_jct` 和 `DedeUserID`）
4. 用文本编辑器打开下载的脚本，将刚复制的内容粘贴到文件约 8 到 9 行处 `cookie = {"cookie": ""}` 的空双引号中并保存

### bilidanmaku.py

在 [获取 cookie](https://github.com/Ranlajetech/bilibili_Useful_Scripts#%E8%8E%B7%E5%8F%96-cookie) 之后，还需要获取自己的 csrf 值：

1. 进入一个B站直播间（请尽量挑选一个未开播的直播间），打开开发者工具的 Network 选项卡，发送任意弹幕，会发现新增了一个名为 send 的数据，点击该数据并查看 payload 选项卡，找到键值 `csrf` 和 `csrf_token` （一般是相同的），复制该值
2. 将刚复制的内容粘贴到第 41 行 `'csrf': ''` 和第 43 行 `'csrf_token': ''}` 的空单引号中并保存。关闭文件。
3. 运行脚本

### bilisignGroup.py

[获取 cookie](https://github.com/Ranlajetech/bilibili_Useful_Scripts#%E8%8E%B7%E5%8F%96-cookie) 后无需进一步操作，直接运行脚本
