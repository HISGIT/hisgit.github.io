---
layout: post
title:  "How to scientific-surfing using a cloud server"
alt_title: "如何使用云服务器科学上网"
date:   2026-01-06 21:15:00 +0900
read_time: true
ref: scientific-surfing-note
introduction: |
    -- 实际上，这篇指南在三年前就已经完成了，不过当时只是通过邮件发给了两位朋友。
    为了庆祝新博客的上线，我稍微修改了一下，现在正式发布。--
---

## 目录
* 预备
* 注册虚拟信用卡
* 购买VPS
* VPS设置
* 客户端设置

## 预备
自建梯子对大部分没有使用过Linux的人来说，可能最难以理解的部分在于命令行操作。本文认为自建需要的最基础的命令行操作为以下几个，

ssh  `#用于远程登录服务器`

ls  `#查看文件或者目录`

cd  `#切换当前目录`

vim  `#编辑文件`

需要先了解基本用法，才能理解并完成本文的命令行操作。

## 注册虚拟信用卡
虽然也有购买VPS时也有其他支付方式，但是虚拟信用卡便利性更好。
- a. 前往[全球付](https://www.globalcash.hk/v4/)官网，点击“注册”按钮进入注册页面。
- b. 在注册页面输入你的邮箱地址和手机号码（+86手机号也可），并创建一个密码。
- c. 验证你的邮箱和手机号码，填写你的基本信息，如姓名、身份证号码等。不是必须填写真实姓名地址，但是需要可用的手机号码接收短信验证码。
- d. 在全球付官网充值页面，选择一个充值方式，如银行卡、支付宝等，完成充值。
- e. 用全球付虚拟信用卡进行VPS购买时，请确保你的虚拟信用卡余额足够支付，也需要保证卡内没有超过限制的未支付订单，否则可能会导致支付失败。

## 购买Vultr VPS
a. 前往[Vultr](https://www.vultr.com)官网，注册一个账户并登录（通过另外一些链接有[**Vultr赠送金额**](https://zhuanlan.zhihu.com/p/40144588)或者联系本文作者获取）。

b. 在Vultr主页上，点击“Deploy New Server”按钮。
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器0.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器.png)
c. 在下拉菜单中选择“CentOS 7 x64”，选择你想要的VPS套餐，例如5美元/月的套餐。
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器2.png)
d. 在“Server Location”选项卡中选择你想要的服务器地理位置。     
e. 在“Additional Features”选项卡中，勾选“Enable IPv6”选项，并填写你想要设置的主机名。
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器3.png)
f. 点击“Deploy Now”按钮，服务器会按照小时计费，只有销毁服务器才能停止计费。在每月月初，费用将会从设置好的虚拟信用卡或者账号余额扣款。服务器发布完成后，点击server details里查看ip地址和用于登录的账号密码。
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器4.png)

## VPS设置

### 1.通过SSH登录VPS
在终端中输入以下命令：
`ssh root@136.244.95.242`
![screenshot](/assets/2026-01-06-scientific-surfing-note/ssh_login.png)
在Server Details页面拿到root用户密码，需要输入VPS的root用户密码进行登录。为了安全起见，一般建议不要使用root用户进行操作。但在这里为了方便操作服务器，所有命令都用root账号执行。
Linux服务器输入密码时不显示密码，请直接输入密码。
有时候会因为超时出现断连，重新登录即可。

### 2.安装软件

在终端中输入以下命令，基本都是yum 的安装命令，安装一些设置和维护的必要软件。
{% highlight shell linenos %}
#安装第三方软件源
yum install epel-release -y
yum update epel-release
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/新加软件源1.png)安装vim和fail2ban，在终端中输入以下命令：
{% highlight shell linenos %}
#安装vim和fail2ban
yum install vim fail2ban -y
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/安装vim和fail2ban_2.png)![screenshot](/assets/2026-01-06-scientific-surfing-note/安装vim和fail2ban_3.png)
安装编译工具：

{% highlight shell linenos %}
#安装编译时必需的软件
yum install git -y
yum install wget -y
yum install gcc -y
yum install gettext -y
yum install autoconf -y
yum install libtool -y
yum install automake -y
yum install make -y
yum install pcre-devel -y
yum install asciidoc -y
yum install xmlto -y
yum install c-ares-devel -y
yum install libev-devel -y
yum install libsodium-devel -y
yum install mbedtls-devel -y
{% endhighlight %} 

由于输出内容过多太多，不再截图。为了保证每个安装命令执行成功，建议逐句执行。
### 3.编译安装Shadowsocks-libev

{% highlight shell linenos %}
#拉取git仓库源代码
git clone http://github.com/shadowsocks/shadowsocks-libev.git
#切换目录
cd shadowsocks-libev
#编译及安装
git submodule update --init --recursive
./autogen.sh && ./configure --prefix=/usr && make
make install
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/编译安装shadowsocks-libev.png)
安装成功后可以通过 `ls` 查看安装后的可执行文件位置：
`ls /usr/bin/ss-server`
![screenshot](/assets/2026-01-06-scientific-surfing-note/安装ss-server.png)

### 4.配置Shadowsocks-libev

安装 Shadowsocks-libev 后，需要进行一些配置。这些配置将确定 Shadowsocks 服务的登录密码，相应的登录端口。

首先，编辑 Shadowsocks-libev 的配置文件：
`vim /root/config.json`
{% highlight json linenos %}
{
"server":["::0","0.0.0.0"],
"server_port":8322,
"password":"jksdf@",
"timeout":600,
"method":"chacha20-ietf-poly1305",
"mode":"tcp_and_udp",
"fast_open":false
}
{% endhighlight %}
需要将其中的 `"password"` 后的字段值替换为自己的 Shadowsocks 密码，并将 `"server_port"` 后的字段值替换为自定义的端口号。

建议使用较高的端口号，例如 `8322` 或 `8443`，以避免受到墙对标准端口的封锁。
最后，配置 Shadowsocks-libev 服务并为它为设置系统启动项：
`vim /etc/systemd/system/shadowsocks.service`
{% highlight shell linenos %}
[Unit]
Description=shadowsocks-libev
After=network.target

[Service]
ExecStart=/usr/bin/ss-server -c /root/config.json
Restart=on-abort

[Install]
WantedBy=multi-user.target
{% endhighlight %}
可以查看一下是否成功编辑文件：
![screenshot](/assets/2026-01-06-scientific-surfing-note/配置shadowsocks-libev.png)
设置防火墙端口，和配置文件里的`server_port`一致：
{% highlight shell linenos %}
firewall-cmd --zone=public --add-port=8322/tcp --permanent
firewall-cmd --zone=public --add-port=8322/udp --permanent
#重新加载防火墙配置
firewall-cmd --reload
#重启防火墙服务firewalld
systemctl restart firewalld
{% endhighlight %}
设置自启动并查看运行状态:
{% highlight shell linenos %}
systemctl enable shadowsocks
systemctl start shadowsocks
systemctl status shadowsocks
{% endhighlight %}

![screenshot](/assets/2026-01-06-scientific-surfing-note/查看服务状态和增加防火墙出口.png)

### 5.简单防护配置

新建并修改配置文件：
`vim /etc/fail2ban/jail.local`
把以下内容复制粘贴进去并保存：
{% highlight shell linenos %}
[DEFAULT]
# Ban hosts for one hour:
bantime = 3600
# Override /etc/fail2ban/jail.d/00-firewalld.conf:
banaction = iptables-multiport
[sshd]
enabled = true
{% endhighlight %}
设置自启动，重启fail2ban服务:
{% highlight shell linenos %}
systemctl enable fail2ban
systemctl restart fail2ban
{% endhighlight %}
修改ssh登录端口。ssh一般用22端口登录，为减少防止服务器被扫描并爆破密码登录，需做一些简单的设置。
{% highlight shell linenos %}
#修改sshd服务配置文件
vim /etc/ssh/sshd_config
{% endhighlight %}
找到以下文本：
`# Port 22`
修改为：
`Port 5408`
![screenshot](/assets/2026-01-06-scientific-surfing-note/修改ssh登录端口.png)
然后修改防火墙端口设置，增加刚刚修改的ssh登录端口。
{% highlight shell linenos %}
firewall-cmd --zone=public --add-port=5408/tcp --permanent
firewall-cmd --zone=public --add-port=5408/udp --permanent
{% endhighlight %}

{% highlight shell linenos %}
#重新加载防火墙配置
firewall-cmd --reload
#重启防火墙服务firewalld和sshd服务，查看运行状态
systemctl restart firewalld
systemctl restart sshd
systemctl status sshd
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/修改ssh登录配置2.png)
然后退出服务器，之后都要使用新的端口登录：
`ssh root@136.244.95.242 -p5408`

完成到这一步，其实已经可以跳到后面的说明，使用上面配置里的 `"password"` 、服务器IP和`"server_port"`，
进行客户端配置然后科学上网了。
### 快照部署
在我们设置好服务器之后，当然只想设置一次，如果当前ip因为什么原因无法连接，那就要使用新ip重新部署。这时使用快照部署将无需重新配置，开机即用。
首先我们要给已经配置好的服务器生成一份快照：![screenshot](/assets/2026-01-06-scientific-surfing-note/生成快照1.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/生成快照2.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/生成快照3.png)
这时最好保存好原始服务器的root登录密码，防止丢失：
![screenshot](/assets/2026-01-06-scientific-surfing-note/保存原始服务器的密码.png)
虽然Vultr好像已经能做到完全使用快照的设置，包括root密码，生成新服务器，但是还是保险一点好。

我们看到快照已经准备好了，就可以销毁当前服务器了：
![screenshot](/assets/2026-01-06-scientific-surfing-note/快照完成.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/销毁旧服务器.png)
这时已经可以使用快照部署新服务器了，和一开始发布新服务器只有一个地方不同，"操作系统" 选择那里，选择我们刚才创建的快照然后发布：
![screenshot](/assets/2026-01-06-scientific-surfing-note/操作系统来自快照.png)
服务器创建成功后，只需要修改客户端的ip配置就能正常使用了。
注意，新部署的服务器使用新ip和修改后的端口登录用于ssh登录。如果服务器修改了shadowsocks配置配置或者其他配置，需重新生成新的快照，并在后续使用新的快照部署服务器。
## 客户端设置
ss客户端有各种各样，这里仅介绍Windows系统下的客户端设置。其他客户端的设置都大同小异，基本都差不多。
通过[official releases page](https://github.com/shadowsocks/shadowsocks-windows/releases)下载安装好后，运行客户端然后进行配置：
![screenshot](/assets/2026-01-06-scientific-surfing-note/客户端配置.png)

客户端设置好后，可以通过分享配置获取配置的二维码：
![screenshot](/assets/2026-01-06-scientific-surfing-note/获取配置.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/分享配置2.png)

正常运行客户端，如果开了全局代理且运行正常，即可正常科学上网上谷狗：
![screenshot](/assets/2026-01-06-scientific-surfing-note/全局代理.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/登录谷狗成功.png)

当然还有不使用全局代理的方法。系统代理那里选择禁用，然后浏览器的网络配置修改如下：
![screenshot](/assets/2026-01-06-scientific-surfing-note/非全局浏览器设置.png)
然后也能访问谷狗。