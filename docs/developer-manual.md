# EulerLauncher开发者文档

## 构建EulerLauncher

EulerLauncher使用Python语言编写，源代码可以跨平台运行，但需要安装Python运行时。为了方便用户使用，可以将源代码编译为二进制形式。在不同的操作系统上构建的步骤略有不同，具体请参照下述指南。

## 在MacOS上构建EulerLauncher

### 准备阶段

**安装Python:**

参考[Python社区首页][1]完成Python安装，推荐安装Python 3.9及以上版本

**安装Homebrew**

参考[Homebrew官网][2]完成Homebrew安装

EulerLauncher使用`Pyinstaller`将源码编译为MacOS可执行文件(Unix二进制文件)及`.app`文件，使用`create-dmg`工具将`.app`构建成为`.dmg`磁盘文件以方便软件安装。

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
cd /path/to/EulerLauncher
```

安装项目依赖

``` Shell
pip3 install -r requirements.txt
```

### 构建

EulerLauncher可执行文件包括以下几个部分：

1. EulerLauncherd: EulerLauncher守护进程，以root权限运行在后台，与调用虚拟化组件(Qemu、HyperV、KVM等)及镜像组件进行相关操作；
2. EulerLauncher.app: EulerLauncher服务端主程序，将EulerLauncher及其他相关程序、数据、文件等打包为MacOS APP软件包，便于分发和使用。
3. EulerLauncher: MacOS可执行文件，EulerLauncher客户端CLI工具，用于与服务端交互。
4. install: MacOS可执行文件，将EulerLauncher运行所需配置文件及相关数据文件安装至`Application Support`文件夹。

由于`EulerLauncher.app`对`EulerLauncherd`有依赖关系，请严格按照以下顺序构建`EulerLauncherd`及`EulerLauncher.app`:

1. EulerLauncherd:

    项目源码中已包含用于构建EulerLauncherd的Spec脚本`EulerLauncherd-Mac.spec`, 若非必要，请勿修改该文件，使用一下命令开始构建：
    ``` Shell
    pyinstaller --clean --noconfirm specs/EulerLauncherd-Mac.spec
    ```

2. EulerLauncher.app:

    项目源码中已包含用于构建EulerLauncher的Spec脚本`EulerLauncher-MacOS.spec`, 若非必要，请勿修改该文件，使用一下命令开始构建：
    ``` Shell
    pyinstaller --clean --noconfirm specs/EulerLauncher-MacOS.spec
    ```

构建`eulerlauncher` CLI 及 `install` 脚本, cli与install之间有依赖关系，请严格按照下面的顺序进行构建:

``` Shell
pyinstaller --clean --noconfirm specs/cli-mac.spec
pyinstaller --clean --noconfirm specs/install.spec
```

### 制作`.dmg`：

首先，我们创建一个新目录并将文件移动到其中。
``` Shell
mkdir -p dist/dmg
cp -R dist/EulerLauncher.app dist/dmg
```

然后，我们可以使用下面的命令来制作磁盘镜像文件:
``` Shell
create-dmg --volname "EulerLauncher" --volicon "etc/images/favicon.png" --window-pos 200 120 --window-size 600 300 --icon-size 100 --icon "EulerLauncher.app" 175 120 --hide-extension "EulerLauncher.app" --app-drop-link 425 120 "dist/EulerLauncher.dmg" "dist/dmg/"
```

`EulerLauncher.dmg`中将只包含`EulerLauncher.app`主程序，需要将`install`脚本及`EulerLauncher` CLI工具一并压缩后再进行分发。


## 在Windows上构建EulerLauncher

**安装Python:**

参考[Python社区首页][1]完成Python安装，推荐安装Python 3.9及以上版本

EulerLauncher使用`Pyinstaller`将源码编译为Windows可执行文件(.exe)。

使用下面命令安装`Pyinstaller`

``` Shell
pip3 install pyinstaller
```

进入项目目录并准备开始工作

``` Shell
cd \\path\\to\\EulerLauncher
```

安装项目依赖

``` Shell
pip3 install -r requirements-win.txt
```

### 构建

EulerLauncher可执行文件包括以下几个部分：

- eulerlauncherd.exe：EulerLauncher的主进程，是运行在后台的守护进程，负责与各类虚拟化后端交互，管理虚拟机、容器以及镜像的生命周期，eulerlauncherd.exe是运行在后台的守护进程。
- eulerlauncher.exe：EulerLauncher的CLI客户端，用户通过该客户端与eulerlauncherd守护进程交互，对虚拟机、镜像等进行相关操作。
- config-env.bat: 帮助用户快速配置环境变量

1. 构建`eulerlauncherd.exe`:

项目源码中已包含用于构建EulerLauncherd的Spec脚本`EulerLauncherd-win.spec`, 若非必要，请勿修改该文件，使用一下命令开始构建：

    ``` Shell
    pyinstaller --clean --noconfirm specs\\EulerLauncherd-win.spec
    ```

2. 构建`eulerlauncher.exe`:

``` Shell
pyinstaller --clean --noconfirm specs\\cli-mac.spec
```

3. 将`etc\bin`目录下的`config-env.bat`及`qemu-img`文件夹拷贝到制品目录，并进行压缩。

[1]: https://www.python.org/
[2]: https://brew.sh/