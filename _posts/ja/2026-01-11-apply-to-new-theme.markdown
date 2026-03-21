---
layout: post #default,post,page,home,categories,tags,collection,category,tag
title:  "気軽にテーマコードをカスタマイズしよう"
# alt_title: "Basically Basic"
sub_title: "テーマのカスタマイズにより、自分でテーマコードを書く道へ"
date:   2026-03-14 21:50:00 +0900
read_time: true
ref: apply-to-new-theme
comments:
  host: wxw.moe
  username: ToT
  id: 116227599453343515
introduction: |
    **Basically Basic** は、Jekyll のデフォルトテーマの代わりとなるテーマです --- *[Minima](https://github.com/jekyll/minima)*。Minima に含まれるすべての規約と機能は、**Basically Basic** でも完全にサポートされています。
---

## 目次
1. 基本テーマ
2. *jekyll-theme-basically-basic* テーマを異なる方法でインストールする
3. 多言語機能を部分的に実装する
4. インラインコードの背景色の問題
5. リンクページを自動的に追加・生成する
6. Mastodon のトゥートをコメントにする
7. フォントスタイルを変える
8. 参考資料

## 基本テーマ
Minima テーマは Jekyll のデフォルトテーマです。シンプルで見た目が良く、使いやすいです。`_config.yml` ファイルに以下のような設定コードが見つかります：
{% highlight json linenos %}
# Build settings
theme: minima
plugins:
  - jekyll-feed
{% endhighlight %}
`Gemfile` にも以下のようにあります：
{% highlight json linenos %}
# This is the default theme for new Jekyll sites. You may change this to anything you like.
gem "minima", "~> 2.5"
{% endhighlight %}

しかし、このテーマは私のニーズを満たすには基本的すぎました。開発者ではなく一般ユーザーとして、Minima に似ているが、もっと多くの機能とカスタマイズオプションがあるテーマが欲しかったのです。そこで、*[Basically Basic](https://github.com/jekyll/minima)* というテーマを見つけました。
## 異なる方法でテーマをインストールする
Ruby gem を使うか、GitHub のリポジトリの README に従って Git を使ってインストールできます。

Ruby gem を使うインストール方法が最も簡単です。以下のように `_config.yml` と `Gemfile` のコードを変更するだけです。
Jekyll サイトの `Gemfile` に以下の行を追加してください：
{% highlight json linenos %}
gem "jekyll-theme-basically-basic"
{% endhighlight %}

次に、Jekyll サイトの `_config.yml` ファイルに以下の行を追加してください：
{% highlight json linenos %}
theme: jekyll-theme-basically-basic
{% endhighlight %}

最後に、`bundle install` コマンドを実行してテーマ gem と依存関係をインストールしてください：
{% highlight js linenos %}
bundle install
{% endhighlight %}

インストールコマンドを実行すると、以下のような出力が表示されます：
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/Screenshot 2026-02-06 at 23.28.49.png)

`bundle exec jekyll serve` コマンドを実行すると、`http://localhost:4000` で新しいテーマが適用された Jekyll サイトを確認できます。

最後に、マニュアルでインストール方法を見てみましょう。まず、GitHub リポジトリ *[jekyll-theme-basically-basic](https://github.com/mmistakes/jekyll-theme-basically-basic)* から元のコードをダウンロードし、ファイル構造を確認してください：
{% highlight json linenos %}
jekyll-theme-basically-basic
├── _data                      # data files
|  └── theme.yml               # theme settings and custom text
├── _includes                  # theme includes and SVG icons
├── _layouts                   # theme layouts (see below for details)
├── _sass                      # Sass partials
├── assets
|  ├── javascripts
|  |  └── main.js
|  └── stylesheets
|     └── main.scss
├── _config.yml                # sample configuration
└── index.md                   # sample home page (all posts/not paginated)
{% endhighlight %}
ダウンロードしたフォルダ内のファイルを 自分のJekyll サイトフォルダにコピーしてください：
{% highlight js linenos %}
cp -a jekyll-theme-basically-basic/{_layouts,_includes,assets,_sass,_data,_config.yml} path/to/myblog
{% endhighlight %}

その後、Gem を使う方法と同じように `Gemfile` と `_config.yml` を更新してください：
{% highlight js linenos %}
# Gemfile
gem "jekyll-theme-basically-basic"

# _config.yml
theme: jekyll-theme-basically-basic
{% endhighlight %}

これでテーマが Jekyll サイトに適用され、テーマコードを必要に応じて変更できるようになります。
## 多言語機能を部分的に実装する
このテーマは、Jekyll が静的サイトジェネレータであるため、多言語機能をサポートしていません。しかし、この目標を達成するために、いくつかの回避策を使うことができます。
「jekyll multilingual」で Google を検索すると、*[jekyll-multiple-languages-plugin](https://github.com/Anthony-Gaudino/jekyll-multiple-languages-plugin)* のようなソリューションが見つかります。

多言語機能を実装する別の方法が存在しているはずです。*[multilingual-jekyll-websites](https://www.usecue.com/blog/multilingual-jekyll-websites/)* を調べ、何度も git hard-reset で実験した後、やっと多言語機能を実装する方法を見つけました：異なる言語ファイルにコンテンツを分離し、フロントマター `ref` を使用して同じコンテンツを異なる言語ファイルで関連付ける、右上隅に言語セレクタを配置するという方法です。 

例えば、`_posts` フォルダに `_posts/en/2026-01-16-this-way-we-make-it-and-again.markdown` と `_posts/zh/2026-01-16-this-way-we-make-it-and-again.markdown` のように言語別のフォルダを作成し、異なる言語のコンテンツを作成します。その後、フロントマター `ref` を使用して、これらのファイルを関連付けます。ホームページには `language: en` のファイルのみが表示され、その他は非表示になります。言語セレクタをクリックすると、対応する言語版のコンテンツが表示されます。

`_config.yml` で、異なる言語ファイルのパーマリンクと言語を設定するために、以下のようなコードを追加してください：
{% highlight json linenos %}
lang: en

defaults:
 # ---------- EN ----------
- scope:
    path: "_posts/en/"
  values:
    permalink: /en/:slug/
    language: en
    lang_name: English
    layout: "post"
 # ---------- JA ----------
- scope:
    path: "_posts/ja"
  values:
    permalink: /ja/:slug/
    language: ja
    lang_name: 日本語
    layout: "post"
 # ---------- CH ----------
- scope:
    path: "_posts/zh"
  values:
    permalink: /zh/:slug/
    language: zh
    lang_name: 中文
    layout: "post"
{% endhighlight %}

`_includes/posts-all.html` ファイル:
{% highlight html linenos %}{% raw %}
{% assign posts = site.posts | where:'language', site.lang %}
{% for post in posts %}
  {% include entry.html %}
{% endfor %}
{% endraw %}
{% endhighlight %}

その後、記事ページの右上隅に、以下のような `_includes/masthead.html` に [言語セレクタ](https://github.com/HISGIT/hisgit.github.io/commit/7f828eed1fba6c40b5f2706070fbd3aef9ce50e1#diff-5ca4edb2e5a8b2d7e97c0e91357a897fa1f1432e5eab143198ec7e9b7c2b8325R19-R42) を追加してください：
{% highlight html linenos %}{% raw %}
<div class="header-right">
  <div class="language-selector-header">
    {% assign posts_language_version = site.posts | where_exp:'item', "page.ref != nil and item.ref == page.ref" | map: "language" %}
    {% assign path = page.url | split: '/' | slice: 2, segments.size | join: '/' %}
    {% if posts_language_version.size > 0 %}
      <ul>
        {% if posts_language_version contains "en" %}
        <li><a href="/en/{{ path }}" lang="en">English</a></li>
        {% endif %}
        {% if posts_language_version contains "zh" %}
        <li><a href="/zh/{{ path }}" lang="zh">中文</a></li>
        {% endif %}
        {% if posts_language_version contains "ja" %}
        <li><a href="/ja/{{ path }}" lang="ja">日本語</a></li>
        {% endif %}
      </ul>
    {% endif %}
  </div>
</div>
{% endraw %}  {% endhighlight %}

スタイルファイル `_sass/basically-basic/_sidebar.scss`も：
{% highlight css linenos %}{% raw %}
.header-right {
  position: absolute;
  top: 0;
  right: 10rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1.8125rem 1rem 0 0;
}

.language-selector-header ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 0.5rem;
}

.language-selector-header a {
  padding: 0.25rem 0.5rem;
  color: $text-color;
  text-decoration: none;
}
{% endraw %}{% endhighlight %}

同じタイトルの記事が複数言語で重なるのを避けるため、`_posts/en` フォルダ内の記事のみが `tags`/`tag` と `categories`/`categorie` フロントマターを持ちます。他の言語の記事ではこれらのフロントマターを削除してください。
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/multilingual_selector_post.png)
<p style="text-align: center; font-weight: bold;">記事ページの多言語セレクタ</p>
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/archives_page.png)
<p style="text-align: center; font-weight: bold;">アーカイブページ</p>

## インラインコードの背景色の問題
新しいテーマを適用した後、インラインコードの背景色が正しく表示されなくなりました。これを修正するために、`assets/stylesheets/main.scss` ファイルにインラインコードの背景色を追加してください：
{% highlight css linenos %}{% raw %}
:not(pre) > code,
.code-inline { 
  background-color: #d1dddd98; 
  color: inherit;          /* keep the text color normal */
  padding: 0.2em 0.4em;    /* small padding for readability */
  border-radius: 3px;      /* rounded corners */
}

pre > code {
  background-color: inherit;
}
{% endraw %}{% endhighlight %}

## リンクページを自動的に追加・生成する
やっとブログにリンクページを追加する時が来ました。まず、Jekyll サイトのルートフォルダに新しいファイル `links.md` を作成し、以下のようにフロントマターを入れてください：
{% highlight json linenos %}{% raw %}
---
layout: blogroll
title: Links
permalink: /blogroll/
---
{% endraw %}
{% endhighlight %}

次に、`_layouts/blogroll.html` ファイルをレイアウトファイルとして追加してください。リンク集ページは、過去 90 日以内に更新されたリンクのブログを優先し、各リンクから最新の 3 つの記事を取得し、新着順で表示するように自動生成したいと考えました。この記事 *[automatic-blogroll](https://www.alexmolas.com/2023/07/20/automatic-blogroll.html)* にヒントを得ました。

Python スクリプト `build_blogroll.py` を調整し、友人のブログ URL を保存する `_data/websites.txt` ファイルを作成しました。その後、このスクリプトを実行してリンク集ページを自動生成します。
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/blogroll_python_script.png)
このようにしてリンク集ページが自動生成されます。
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/links_page.png)

## Mastodon のトゥートをコメントにする

通常、静的ブログにコメント機能を追加するにはプラグインを導入する必要がありますが、プラグインなしで実装する方法があります。Mastodon API と [`comments.html`](https://github.com/HISGIT/hisgit.github.io/blob/main/_includes/comments.html) ファイルの JavaScript を組み合わせることで、*[Mastodon のトゥートをコメントとして表示する](https://carlschwan.eu/2020/12/29/adding-comments-to-your-static-blog-with-mastodon/)* ことができます。

まず、記事レイアウトファイル `_layouts/post.html` に以下のように `comments.html` を含めてください：
{% highlight html linenos %}{% raw %}
{% include comments.html %}
{% endraw %}{% endhighlight %}

次に、記事のフロントマターにコメント情報を追加することでコメント機能を有効にしてください：
{% highlight json linenos %}{% raw %}
comments:
  host: wxw.moe
  username: ToT
  id: xxxxxxx
{% endraw %}
{% endhighlight %}
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/comments_frontmatter.png)

記事を公開するとき、記事へのリンクを含むトゥートを Mastodon に投稿してください。記事ページにはコメントを読み込むボタンが表示されます。ページを開く時ではなく、クリックするたびにコメントが取得されます。
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/loaded_comments.png)
<p style="text-align: center; font-weight: bold;">読み込まれたコメント</p>

## フォントスタイルを変える

*[Revivance Blog](https://revivance.blog)* を参考にして、そのタイポグラフィに感銘を受け、同様のフォントスタイル設定を採用することにしました。

SCSS ファイル *[_sass/basically-basic/_base.scss](https://github.com/HISGIT/hisgit.github.io/blob/main/_sass/basically-basic/_base.scss)* の `body` セクションを次のように変更してください：
{% highlight css linenos %}{% raw %}
body {
  background: $background-color;
  color: #333;
  font-feature-settings: "lnum" 1;
  font-variant-numeric: lining-nums;
  font-size: 18px;
  font-weight: 400;
  line-height: 1.53;
  font-variant-ligatures: normal;
  text-rendering: optimizeLegibility;
}
{% endraw %}{% endhighlight %}

タイトルのフォントスタイルも変更するために、`_sass/basically-basic/_variables.scss` ファイルを編集して、ベースフォントファミリーを更新します。元のコードは以下の通りです：
{% highlight css linenos %}{% raw %}
$base-font-family: "Fira Sans", sans-serif !default;
{% endraw %}{% endhighlight %}
以下のように変更します：
{% highlight css linenos %}{% raw %}
$base-font-family: "Freight Text W03 Book", "Noto Serif SC", georgia, "Songti SC", Simsun, serif;
{% endraw %}{% endhighlight %}
完了です。

## 参考資料
1. *jekyll-theme-basically-basic*: `https://github.com/mmistakes/jekyll-theme-basically-basic`
2. *Basically Basic*: `https://github.com/jekyll/minima`
3. *automatic-blogroll*: `https://www.alexmolas.com/2023/07/20/automatic-blogroll.html`
4. *adding-comments-to-your-static-blog-with-mastodon*: `https://carlschwan.eu/2020/12/29/adding-comments-to-your-static-blog-with-mastodon/`
5. *revivance.blog*: `https://revivance.blog`
6. *multilingual-jekyll-websites*: `https://www.usecue.com/blog/multilingual-jekyll-websites/`