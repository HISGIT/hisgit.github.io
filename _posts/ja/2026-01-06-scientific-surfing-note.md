---
layout: post
title:  "How to Scientific-surfing Using a Cloud Server"
alt_title: "クラウドサーバーでVPNを構築しファイアウォールを突破する方法"
date:   2026-01-06 21:15:00 +0900
read_time: true
ref: scientific-surfing-note
introduction: |
    -- 実はこの記事、三年前にすで完成していたんです、でも当時はメールで友達２人に送っただけ。
    今回、新しいブログの立ち上がりを祝いに少し書き直して公開します。 --
---

## 目次
* 準備
* バーチャルクレジットカードを申し込む
* VPS購入
* VPS設置
* クライアント設置

## 準備
Linuxをこれまで使ったことがない人にとって、自分専用のサーバーをセットアップする際に最も分かりにくいのは、多分コマンドラインです。とはいえ、実際にはこのガイドを進めるために必要なのは、ほんの一部の基本的なコマンドだけです。

ssh  `# login to a remote server`

ls   `# list files or directories`

cd   `# change the current directory`

vim  `# edit files`

これらのコマンドの基本的な使い方さえ理解していれば、この記事の手順を問題なく進められるはずです。

## バーチャルクレジットカードを申し込む
一部のVPSプロバイダーは複数の支払い方法に対応していますが、一般的にはバーチャルクレジットカードを使うのが最も手軽な方法の一つです。

- a. [Global Cash](https://www.globalcash.hk/v4/) の公式サイトにアクセスし、「Register」をクリックします。
- b. メールアドレスと携帯電話番号（+86の番号も使用可能）を入力し、パスワードを作成します。
- c. メールアドレスと電話番号の認証を行い、氏名や身分証番号などの基本情報を入力します。実在していない個人情報をいれてもいいが、SMS認証コードを受け取るため、有効な電話番号は必須です。
- d. Global Cash のチャージページに進み、銀行カードやAlipayなどのチャージ方法を選択します。
- e. VPSを購入する前に、バーチャルクレジットカードの残高が十分であり、未払いの注文が上限を超えていないことを必ず確認してください。そうでない場合、支払いに失敗する可能性があります。

## VPS購入
a. [Vultr](https://www.vultr.com) の公式サイトにアクセスし、アカウントを登録してログインします。（特定のリンク経由、またはこの記事の作者に連絡することで [**Vultr promotional credits**](https://zhuanlan.zhihu.com/p/40144588) を利用できる場合があります。）

b. Vultr のダッシュボードで「Deploy New Server」をクリックします。
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器0.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器.png)

c. OSの一覧から「CentOS 7 x64」を選択し、月額 $5 のプランなどを選びます。
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器2.png)

d. 「Server Location」セクションでサーバーの設置場所を選択します.
e. 「Additional Features」で IPv6 を有効にし、サーバーのホスト名を設定します。
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器3.png)

f. 「Deploy Now」をクリックします。サーバーは時間単位で課金され、削除するまで料金が発生し続けます。料金は翌月初めにバーチャルクレジットカードまたアカウントの残高から引き落とされます。

デプロイが完了したら、サーバーの詳細ページを開き、IPアドレスとログイン情報を確認してください。
![screenshot](/assets/2026-01-06-scientific-surfing-note/发布新服务器4.png)

## VPS設置

### 1. SSHでログインする
ターミナルで次のコマンドを実行します。
`ssh root@136.244.95.242`
![screenshot](/assets/2026-01-06-scientific-surfing-note/ssh_login.png)

サーバー詳細ページに表示されている、Vultr から提供された root パスワードを入力します。一般的には root アカウントでの運用は勧められませんが、このガイドでは便利上 root を使用します。
Linux では、パスワードを入力しても文字が表示されない点に注意してください。
接続がタイムアウトした場合は、再度接続すればいい。

### 2. 必要なソフトウエアのインストール
以下のコマンドを実行し、`yum` を使って必要なツールをインストールします。
{% highlight shell linenos %}
# Install third-party repository
yum install epel-release -y
yum update epel-release
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/新加软件源1.png)

vim と fail2ban をインストールします。
{% highlight shell linenos %}
# Install vim and fail2ban
yum install vim fail2ban -y
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/安装vim和fail2ban_2.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/安装vim和fail2ban_3.png)

コンパイルに必要な依存パッケージをインストールします。
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

出力が非常に長くなるため、スクリーンショットは省略しています。エラーを避けるため、各コマンドは一つずつ実行することをおすすめします。

### 3. Shadowsocks-libev　のコンパイル と インストール
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

インストール後、以下のコマンドでバイナリが存在することを確認します。

`ls /usr/bin/ss-server`
![screenshot](/assets/2026-01-06-scientific-surfing-note/安装ss-server.png)

### 4. Shadowsocks-libev の設定
Shadowsocks-libev をインストールした後は、設定を行う必要があります。ここで設定する内容は、Shadowsocks サービスで使用するパスワードとポート番号です。
設定ファイルを編集します。
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

`"password"` を自分用のものに変更し、`"server_port"` には任意のポート番号を設定してください。
`8322` や `8443` のような高めのポート番号を使うことで、ブロックされる可能性を下げられます。

最後に、Shadowsocks-libev をサービスとして登録し、サーバーが起動時にサービスも自動起動するよう設定します。
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

ファイルが正しく保存されていることを確認します。
![screenshot](/assets/2026-01-06-scientific-surfing-note/配置shadowsocks-libev.png)

`server_port` に合わせてファイアウォールのポートを開放します。
{% highlight shell linenos %}
firewall-cmd --zone=public --add-port=8322/tcp --permanent
firewall-cmd --zone=public --add-port=8322/udp --permanent
# Reload firewall configuration
firewall-cmd --reload
# Restart firewall service
systemctl restart firewalld
{% endhighlight %}

サービスを有効化して起動します。
{% highlight shell linenos %}
systemctl enable shadowsocks
systemctl start shadowsocks
systemctl status shadowsocks
{% endhighlight %}
![screenshot](/assets/2026-01-06-scientific-surfing-note/查看服务状态和增加防火墙出口.png)

### 5. 基本的なセキュリティ配置
設定ファイルを作成して編集します。
`vim /etc/fail2ban/jail.local`
以下の内容をコピーして貼り付けます。
{% highlight shell linenos %}
[DEFAULT]
# Ban hosts for one hour:
bantime = 3600
# Override /etc/fail2ban/jail.d/00-firewalld.conf:
banaction = iptables-multiport

[sshd]
enabled = true
{% endhighlight %}

有効化して再起動します。
{% highlight shell linenos %}
systemctl enable fail2ban
systemctl restart fail2ban
{% endhighlight %}

SSH のログインポートを変更します。SSH は通常ポート 22 を使用しますが、スキャンやブルートフォース攻撃のリスクを下げるため、変更することをおすすめします。
{% highlight shell linenos %}
# Edit sshd configuration file
vim /etc/ssh/sshd_config
{% endhighlight %}

次の行を探します。
`# Port 22`

以下のように変更します。
`Port 5408`
![screenshot](/assets/2026-01-06-scientific-surfing-note/修改ssh登录端口.png)

ファイアウォールを更新し、サービスを再起動します。
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

サーバーからログアウトし、今後は新しいポート番号でログインしてください。
`ssh root@136.244.95.242 -p5408`

ここまでで、上記の `"password"`、サーバーIP、`"server_port"` を使って、クライアント側の設定を行えば自由にインターネットにアクセスできる状態になります。

### スナップショットでデプロイ
サーバーの設定は基本的に一度だけ行えば十分です。何らかの理由で現在の IP がアクセスできなくなった場合でも、スナップショットを使えば再設定なしで再展開できます。

まず、設定済みサーバーのスナップショットを作成します。
![screenshot](/assets/2026-01-06-scientific-surfing-note/生成快照1.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/生成快照2.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/生成快照3.png)

念のため、元の root パスワードを保存しておきます。
![screenshot](/assets/2026-01-06-scientific-surfing-note/保存原始服务器的密码.png)

現在では Vultr は root パスワードを含めた完全なスナップショット復元に対応しているようですが、安全のためバックアップを保持しておくことをおすすめします。

スナップショットの準備ができたら、現在のサーバーを削除しても問題ありません。
![screenshot](/assets/2026-01-06-scientific-surfing-note/快照完成.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/销毁旧服务器.png)

スナップショットを使って新しいサーバーをデプロイします。初回デプロイとの違いは、「Operating System」でスナップショットを選択する点だけです。
![screenshot](/assets/2026-01-06-scientific-surfing-note/操作系统来自快照.png)

新しいサーバーが作成されたら、クライアント設定の IP アドレスを更新するだけで通常通り動作します。新しいサーバーでは IP アドレスと SSH ポートが変更されている点に注意してください。Shadowsocks などの設定を変更した場合は、新しいスナップショットを作成し、それを使って再デプロイする必要があります。

## クライアント設置
Shadowsocks クライアントには多くの種類があります。ここでは Windows での設定例を示しますが、他のプラットフォームでも手順はほぼ同じです。

[公式リリースページ](https://github.com/shadowsocks/shadowsocks-windows/releases) からクライアントをダウンロードし、設定します。
![screenshot](/assets/2026-01-06-scientific-surfing-note/客户端配置.png)

設定後、QR コードを生成して設定内容を共有することもできます。
![screenshot](/assets/2026-01-06-scientific-surfing-note/获取配置.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/分享配置2.png)

グローバルプロキシを有効にすれば、自由にインターネットを閲覧できるようになります。
![screenshot](/assets/2026-01-06-scientific-surfing-note/全局代理.png)
![screenshot](/assets/2026-01-06-scientific-surfing-note/登录谷狗成功.png)

グローバルプロキシを使いたくない場合は、システムプロキシを無効にし、ブラウザを手動で設定してください。
![screenshot](/assets/2026-01-06-scientific-surfing-note/非全局浏览器设置.png)

これで Google にも通常通りアクセスできるようになります。
