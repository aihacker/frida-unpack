## 夜神模拟器安装frida

### 安装frida
>
> 开始 python3.7 直接 pip install frida 和 pip install frida-tools一直卡在 Running setup.py install for frida ... – 了，最后的解决好的办法是到 https://pypi.org/project/frida/#files 下载 frida-xx.x.xx-py3.7-win-amd64.egg，并把它放到安装的python目录的 \Python37\Lib\site-packages 中。

> 然后找到对应的 frida-tools 版本pip3 install frida-tools执行即可安装，如果不对应，执行命令可能会把frida-xx.x.xx-py3.7-win-amd64.egg删掉又卡在Running setup.py install for frida ... –地方，可以根据发布日期来判断相应的 frida-tools 版本。

> 然后 python3.7 安装 easy_install，执行easy_install frida-xx.x.xx-py3.7-win-amd64.egg，即可在 python 中 import frida了。


查看对应手机的cpu版本
```shell
adb shell getprop ro.product.cpu.abi
```

### 以windows为例
#### 1.打开模拟器usb调试
#### 2.进入到安装模拟器文件夹的bin目录中
```shell
adb connect 127.0.0.1:port
```

```python
注：谷歌模拟器端口为5555
夜神模拟器 adb connect 127.0.0.1:62001
逍遥模拟器 adb connect 127.0.0.1:21503
木木模拟器 adb connect 127.0.0.1:7555
```
#### 3.下载frida服务端
https://github.com/frida/frida/releases
下载对应版本即可：frida-server-xx.x.xx-android-platform.xz
#### 4.将下载好的文件传到模拟器
```python
adb  push  frida-server-12.6.12-android-arm64  /data/loacl/tmp
```

#### 5.运行
```python
adb shell
cd /data/local/tmp
chmod +x frida-server-12.4.0-android-arm
./frida-server-12.4.0-android-arm
```

————————————————
版权声明：本文为CSDN博主「风音往」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_43145985/article/details/105340961

### 后记：
因为使用查看对应手机的cpu版本命令，返回的是x86，所以我测试时用的是frida-server-12.8.20-android-x86.xz
```python
> adb shell getprop ro.product.cpu.abi
> x86
```

但是运行后可以使用，但有警告提醒如下：未解决
```python
> ./frida-server-12.8.20-android-x86 &
> [1] 3385
> root@shamu:/data/local/tmp # WARNING: linker: ./f86: unused DT entry: type 0x6ffffef5 arg 0x1c24
```
