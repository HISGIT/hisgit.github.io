---
layout: post
title:  "How to Scientific-surfing Using a Cloud Server"
date:   2026-01-06 21:15:00 +0900
categories: blog
collection: VPN
read_time: true
ref: scientific-surfing-note
introduction: |
    -- Actually this guid was completed 3 years ago, but I only send it by email to two friends.
    To celebrate my new blog's opening, I've revised it slightly and publishing it now. --
---

## Table of Contents
* Preparation
* Register a Virtual Credit Card
* Purchase a VPS
* VPS Setup
* Client Setup

## Preparation
For one who have never used Linux before, the most confusing part of setting up your own server is usually the command line. In practice, you only need a very small set of basic commands to follow this guide:

ssh  `# login to a remote server`

ls   `# list files or directories`

cd   `# change the current directory`

vim  `# edit files`

As long as you understand the basic usage of these commands, you should have no trouble following the steps in this article.

## Register a Virtual Credit Card
While some VPS providers support multiple payment methods, using a virtual credit card is generally one of the most convenient option.

- a. Visit the [Global Cash](https://www.globalcash.hk/v4/) official website and click “Register”.
- b. Enter your email address and mobile phone number (a +86 number is also supported), then create a password.
- c. Verify your email and phone number, and fill in basic information such as your name and ID number. Real personal details are not strictly necessary, but you must provide a valid phone number to receive SMS verification codes.
- d. Go to the Global Cash top-up page and choose a recharge method, such as a bank card or Alipay.
- e. Before purchasing a VPS, make sure your virtual credit card balance is sufficient and that there are no unpaid orders exceeding the limit, otherwise the payment may fail.

## Purchase a VPS
a. Go to the [Vultr](https://www.vultr.com) official website, register an account, and login. (You may use [**Vultr promotional credits**](https://zhuanlan.zhihu.com/p/40144588) through certain links, or by contacting the author of this article.)

b. On the Vultr dashboard, click “Deploy New Server”.
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器0.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器.png)
c. Select “CentOS 7 x64” from the operating system list, then choose a VPS plan, such as the $5/month option.
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器2.png)
d. Choose a server location in the “Server Location” section.     
e. Under “Additional Features”, enable IPv6 and set a hostname for your server.
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器3.png)
f. Click “Deploy Now”. Servers are billed hourly, and charges continue until the server is destroyed. Fees will be deducted from your virtual credit card or account balance at the beginning of next month.

Once deployment is complete, open the server details page to find the IP address and login credentials.
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器4.png)

## VPS Setup

### 1. Login via SSH
In your terminal, run:
`ssh root@136.244.95.242`
![screenshot](/assets/2026-01-06-scientific-surfing-note/ssh_login.png)

Enter the root password provided by Vultr on Server Details page. Although it’s generally recommended not to operate use the root account, this guide uses the root account just for convenience.
Note that Linux does not display passwords as you type them.
If the connection times out, simply reconnect.

### 2. Install Required Software
Run the following commands to install essential tools using `yum`:
{% highlight shell linenos %}
# Install third-party repository
yum install epel-release -y
yum update epel-release
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/新加软件源1.png)

Install vim and fail2ban:
{% highlight shell linenos %}
# Install vim and fail2ban
yum install vim fail2ban -y
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/安装vim和fail2ban_2.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/安装vim和fail2ban_3.png)

Install compilation dependencies:
{% highlight shell linenos %}
# Required tools for compilation
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

Since the output is very long, screenshots are omitted. To avoid errors, it’s best to run each command one by one.

### 3. Compile and Install Shadowsocks-libev
{% highlight shell linenos %}
# Clone source code
git clone http://github.com/shadowsocks/shadowsocks-libev.git
# Change directory
cd shadowsocks-libev

# Build and install
git submodule update --init --recursive
./autogen.sh && ./configure --prefix=/usr && make
make install
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/编译安装shadowsocks-libev.png)

After installation, verify the installed binary:
`ls /usr/bin/ss-server`
![screenshot](/assets/2026-01-06-scientific-surfing-note/安装ss-server.png)

### 4. Configure Shadowsocks-libev
After installing Shadowsocks-libev, some configuration is required. These settings determine password and port used by the Shadowsocks service.
Edit the configuration file:
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

Change `"password"` value to your own password and set `"server_port"` to a custom port.
Using higher ports such as `8322` or `8443` is recommended to reduce the chance of blocking.

Finally, configure the Shadowsocks-libev service and set it to start on boot:
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

Verify that the file was written successfully:
![screenshot](/assets/2026-01-06-scientific-surfing-note/配置shadowsocks-libev.png)

Set firewall ports to match the `server_port` in the configuration:
{% highlight shell linenos %}
firewall-cmd --zone=public --add-port=8322/tcp --permanent
firewall-cmd --zone=public --add-port=8322/udp --permanent
# Reload firewall configuration
firewall-cmd --reload
# Restart firewall service
systemctl restart firewalld
{% endhighlight %}

Enable and start the service:
{% highlight shell linenos %}
systemctl enable shadowsocks
systemctl start shadowsocks
systemctl status shadowsocks
{% endhighlight %}

![screenshot](/assets/2026-01-06-scientific-surfing-note/查看服务状态和增加防火墙出口.png)

### 5. Basic Security Configuration

Create and edit the configuration file:
`vim /etc/fail2ban/jail.local`
Copy and paste the following content:
{% highlight shell linenos %}
[DEFAULT]
# Ban hosts for one hour:
bantime = 3600
# Override /etc/fail2ban/jail.d/00-firewalld.conf:
banaction = iptables-multiport

[sshd]
enabled = true
{% endhighlight %}

Enable and restart:
{% highlight shell linenos %}
systemctl enable fail2ban
systemctl restart fail2ban
{% endhighlight %}

Change the SSH login port. SSH typically uses port 22. To reduce the risk of scanning and brute-force attacks, some simple adjustments are recommended.
{% highlight shell linenos %}
# Edit sshd configuration file
vim /etc/ssh/sshd_config
{% endhighlight %}

Find:
`# Port 22`

Change it to:
`Port 5408`
![screenshot](/assets/2026-01-06-scientific-surfing-note/修改ssh登录端口.png)

Then update firewall rules and restart services:
{% highlight shell linenos %}
firewall-cmd --zone=public --add-port=5408/tcp --permanent
firewall-cmd --zone=public --add-port=5408/udp --permanent
{% endhighlight %}

{% highlight shell linenos %}
# Reload firewall configuration
firewall-cmd --reload
# Restart firewall and sshd services
systemctl restart firewalld
systemctl restart sshd
systemctl status sshd
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/修改ssh登录配置2.png)

Exit the server. From now on, you must use the new port to log in:
`ssh root@136.244.95.242 -p5408`

At this point, you can already proceed to the later steps and configure your client using the `"password"`, server IP, and `"server_port"` above to access the internet freely.

### Snapshot Deployment
After configuring the server, you typically only want to do it once. If the current IP becomes inaccessible for any reason, you can redeploy using a snapshot without reconfiguring everything.

First, create a snapshot of the configured server:
![screenshot](/assets/2026-01-06-scientific-surfing-note/生成快照1.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/生成快照2.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/生成快照3.png)

Save the original root password just in case:
![screenshot](/assets/2026-01-06-scientific-surfing-note/保存原始服务器的密码.png)

Although Vultr now appears to support fully restoring snapshots including root passwords, it is safer to keep a backup.

Once the snapshot is ready, it's OK to destroy the current server:
![screenshot](/assets/2026-01-06-scientific-surfing-note/快照完成.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/销毁旧服务器.png)

You can now deploy a new server using the snapshot. The only difference from the initial deployment is selecting your snapshot under “Operating System”:
![screenshot](/assets/2026-01-06-scientific-surfing-note/操作系统来自快照.png)

After the new server is created, simply update the IP address in your client configuration and it will work normally.
Note that the new server uses a new IP and the modified SSH port for login. If you change the Shadowsocks or other configurations, you must create a new snapshot and deploy new servers from it.

## Client Setup
There are many Shadowsocks clients available. This section demonstrates setup on Windows. Other platforms are very similar.

Download the client from the [official releases page](https://github.com/shadowsocks/shadowsocks-windows/releases), then configure it:
![screenshot](/assets/2026-01-06-scientific-surfing-note/客户端配置.png)

After configuration, you can also generate a QR code to share the configuration:
![screenshot](/assets/2026-01-06-scientific-surfing-note/获取配置.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/分享配置2.png)

With global proxy enabled, you should now be able to browse freely:
![screenshot](/assets/2026-01-06-scientific-surfing-note/全局代理.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/登录谷狗成功.png)

If you prefer not to use global proxy, disable the system proxy and configure your browser manually:
![screenshot](/assets/2026-01-06-scientific-surfing-note/非全局浏览器设置.png)

You will also be able to access Google normally.
