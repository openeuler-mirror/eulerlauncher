# OmniVirt开发者文档

## 构建OmniVirt

OmniVirt使用Python语言编写，源代码可以跨平台运行，但需要安装Python运行时。为了方便用户使用，可以将源代码编译为二进制形式。在不同的操作系统上构建的步骤略有不同，具体请参照下述指南。

## 在MacOS上构建OmniVirt

### 准备阶段

**安装Python:**

参考[Python社区首页][1]完成Python安装，推荐安装Python 3.10及以上版本

**安装Homebrew**

参考[Homebrew官网][2]完成Homebrew安装

OmniVirt使用`Pyinstaller`将源码编译为MacOS可执行文件(Unix二进制文件)及`.app`文件，使用`create-dmg`工具将`.app`构建成为`.dmg`磁盘文件以方便软件安装。

使用下面命令安装`Pyinstaller`

``` Shell
pip3 install pyinstaller
```

使用下面命令安装`create-dmg`

``` Shell
brew install create-dmg
```

进入项目目录并准备开始工作

``` Shell
cd /path/to/OmniVirt
```

安装项目依赖

``` Shell
pip3 install -r requirements.txt
```

### 构建

OmniVirt可执行文件包括以下几个部分：

1. OmniVirtd: omnivirt守护进程，以root权限运行在后台，与调用虚拟化组件(Qemu、HyperV、KVM等)及镜像组件进行相关操作；
2. OmniVirt.app: OmniVirt服务端主程序，将omnivirtd及其他相关程序、数据、文件等打包为MacOS APP软件包，便于分发和使用。
3. omnivirt: MacOS可执行文件，OmniVirt客户端CLI工具，用于与服务端交互。
4. install: MacOS可执行文件，将OmniVirt运行所需配置文件及相关数据文件安装至`Application Support`文件夹。

由于`OmniVirt.app`对`OmniVirtd`有依赖关系，请严格按照以下顺序构建`OmniVirtd`及`OmniVirt.app`:

1. OmniVirtd:

    项目源码中已包含用于构建OmniVirtd的Spec脚本`OmniVirtd-Mac.spec`, 若非必要，请勿修改该文件，使用一下命令开始构建：
    ``` Shell
    pyinstaller --clean --noconfirm OmniVirtd-Mac.spec
    ```

2. OmniVirt.app:

    项目源码中已包含用于构建OmniVirt的Spec脚本`OmniVirt-MacOS.spec`, 若非必要，请勿修改该文件，使用一下命令开始构建：
    ``` Shell
    pyinstaller --clean --noconfirm OmniVirt-MacOS.spec
    ```

构建`omnivirt` CLI 及 `install` 脚本, cli与install之间有依赖关系，请严格按照下面的顺序进行构建:

``` Shell
pyinstaller --clean --noconfirm cli.spec
pyinstaller --clean --noconfirm install.spec
```

### 制作`.dmg`：

首先，我们创建一个新目录并将文件移动到其中。
``` Shell
mkdir -p dist/dmg
cp -R dist/OmniVirt.app dist/dmg
```

然后，我们可以使用下面的命令来制作磁盘镜像文件:
``` Shell
create-dmg --volname "OmniVirt" --volicon "etc/images/favicon.png" --window-pos 200 120 --window-size 600 300 --icon-size 100 --icon "OmniVirt.app" 175 120 --hide-extension "OmniVirt.app" --app-drop-link 425 120 "dist/OmniVirt.dmg" "dist/dmg/"
```

`OmniVirt.dmg`中将只包含`OmniVirt.app`主程序，需要将`install`脚本及`omnivirt` CLI工具一并压缩后再进行分发。

[1]: https://www.python.org/
[2]: https://brew.sh/