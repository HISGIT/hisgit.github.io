---
layout: post
title:  "Build a Jekyll blog"
alt_title: "Jekyllブログを構築しよう"
sub_title: "rubyとjavascriptがわからなくても平気"
ref: build-a-jekyll-blog
# actions:
#   - label: "Learn More"
#     icon: github  # references name of svg icon, see full list below
#     url: "http://url-goes-here.com"
#   - label: "Download"
#     icon: download  # references name of svg icon, see full list below
#     url: "http://url-goes-here.com"
date: 2026-01-20 22:35:00 +0900
read_time: true
introduction: |
    **GitHub Pages でデプロイする静的ブログをゼロから構築する**。
---

## 目录
1. なぜ Jekyll を選ぶのか
2. ローカル部署とテスト
3. GitHub による自動ビルドとデプロイ
4. カスタムドメインの設定
5. あとがき〜Markdown の問題とテーマのカスタマイズ
6. さらにあとがき〜多言語対応機能の実装後に

## なぜ Jekyll を選ぶのか
1. 静的ページで、デプロイが簡単
2. Markdown 形式での編集に対応している
3. シンプルだが簡素すぎず、プラグインで機能を少しずつ拡張できる

最後に Jekyll を選びました。

## ローカル部署とテスト
[公式ドキュメント -> Jekyll on macOS](https://jeky llrb.com/docs/installation/macos/) に従い、  
まず Ruby をインストールする必要があります。ここで少し時間がかかりました（筆者の回線が遅いため）。

{% highlight shell linenos %}{% raw %}
# Use curl to fetch the Ruby installation bootstrap script and execute it with bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install chruby ruby-install
ruby-install ruby 3.4.1

# Write Ruby configuration into the shell config file ~/.zshrc
echo "source $(brew --prefix)/opt/chruby/share/chruby/chruby.sh" >> ~/.zshrc
echo "source $(brew --prefix)/opt/chruby/share/chruby/auto.sh" >> ~/.zshrc
echo "chruby ruby-3.4.1" >> ~/.zshrc # run 'chruby' to see actual version

# Open a new terminal
ruby -v
{% endraw %}
{% endhighlight %}

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/check_ruby_version.png)

この時点で表示された Ruby のバージョンが、  
`echo "chruby ruby-3.x.x"` 実行後に表示されるものと一致していれば、  
インストールは成功です。

{% highlight shell linenos %}{% raw %}
gem install bundler jekyll
# The directory name myblog can be changed to anything you like
jekyll new myblog
cd myblog
# Run the local Jekyll service
bundle exec jekyll serve
{% endraw %}
{% endhighlight %}

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/run_jekyll_serve.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/jekyll_blog.png)

起動に成功すると表示されるサービスアドレス  
`Server address: http://127.0.0.1:4000/`  
にアクセスすると、自分のブログ内容を確認できます。  
普段もこの方法でデバッグや記事の最終表示確認を行います。

## GitHub による自動ビルドとデプロイ

まず GitHub 上で新しいリポジトリを作成します。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/creat_new_repository.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/creat_new_repository_1.png)

ローカルでの動作確認後、GitHub リポジトリにアップロードし、  
GitHub Pages を通してデプロイします。  
つまり、ここでブログ記事を正式に公開するわけです――衝撃の初公開！

{% highlight shell linenos %}{% raw %}
# Initialize a local Git repository
git init
# Add the remote Git repository address
# https://github.com/HISGIT/myblog.git is the remote repository address; please change it to your own.
git remote add origin https://github.com/HISGIT/myblog.git
# Rename the main branch (?)
git branch -M main
# Add files in the current directory to the local Git repository
git add .
git add _post
# Commit existing files and changes
git commit -m "first commit"
# Push to the remote Git repository
git push -u origin main
{% endraw %}
{% endhighlight %}

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/git_push_remote_repository.png)

この作業が終わったら、続いて GitHub 上で設定を変更します。

GitHub のリポジトリ画面で  
`setting -> code and automation -> Pages`  
に進み、`Build and deployment` を変更します。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_repository_setting.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_actions_create0.png)

ここを `Github Action` に変更します。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/jekyll_workflowfile_edit_01.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/jekyll_workflowfile_edit_02.png)

そのままコミットすれば、GitHub が自動的にビルドとデプロイを行います。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_building_01.png)

`Action` ページでビルドの詳細を確認し、エラーがないかチェックします。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_building_02.png)

赤くなっており、ビルド失敗です。  
詳細を見て確認すると、重要なメッセージが表示されていました。

{% highlight shell linenos %}{% raw %}
Please run `bundle lock --normalize-platforms` and commit the resulting lockfile.
Alternatively, you may run `bundle lock --add-platform <list-of-platforms-that-you-want-to-support>`
public_suffix-7.0.2 requires ruby version >= 3.2, which is incompatible with the
current version, 3.1.6
Error: The process '/opt/hostedtoolcache/Ruby/3.1.6/x64/bin/bundle' failed with exit code 5
{% endraw %}
{% endhighlight %}

明らかに、ビルド時に使用されている Ruby のバージョンが古すぎます。  
そのため、Workflow ファイル `jekyll.yml` を修正する必要があります。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_change_rubyersion-01.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_change_rubyersion-02.png)

`ruby-version` を最新の `3.4.1` に変更し、もう一度 GitHub リポジトリへコミットします。

再び `Action` を確認すると、ビルドとデプロイが正常に完了しているのが分かります。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/action_build_sucessful_01.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/action_build_sucessful_02.png)

その後、deploy 情報に表示されているブログの URL  
http://blog.contextmode.xyz/myblog/  
にアクセスすれば完了です。

通常は  
[your GitHub username].github.io  
のような形式になります。例：http://hisgit.github.io。

ここで GitHub のサブドメインではない理由は、  
すでに自分のカスタムドメインを有効化しているため、  
GitHub のサブドメインから自動的にカスタムドメインへリダイレクトされているからです。

## カスタムドメインの設定
GitHub Pages でカスタムドメインを使用するには、  
DNS サービス提供元と GitHub アカウントの両方で設定を行う必要があります。

### GitHub ドメイン認証
サブドメイン `blog.contextmode.xyz` を例にします。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_01.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_02.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_03.png)

ここに表示されている 2 つの値をコピーし、  
DNS サービス側の設定で使用します。

### DNS 設定
Cloudflare などの DNS（ホスティング）サービスで TXT レコードを追加します。

Domains 管理画面から対象ドメインを選択し、  
DNS 設定で TXT レコードを 1 つ追加します。  
先ほどコピーした値を Name と Content にそれぞれ入力します。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_04.png)

保存をクリックし、反映されるまで待ちます。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_05.png)

ここで認証状態を確認できます。  
緑が Verified、赤が Unverified です。  
DNS の反映には時間がかかることがあるので、もう暫く待ちましょう。

### GitHub Pages への CNAME 追加
以下のように、DNS 管理画面で デプロイ成功後に表示された  
[your GitHub username].github.io　にCNAME レコードを追加します。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/cname_to_github_pages.png)

すべての設定が完了すると、  
[your GitHub username].github.io にアクセスしても、  
カスタムドメインにアクセスしても、  
最終的にはカスタムドメインが表示されます。  
つまり、GitHub Pages へのアクセスは自分のドメインへ自動転送している形です。

## あとがき～markdownとカスタマイズリフォーム
今後、以下の内容について詳しく解説する予定です。
1. Jekyll における Markdown の使い方
2. シンタックスハイライトとコードブロック表示
3. テーマの設定とカスタマイズ

## さらにあとがき～複数言語機能
完成。