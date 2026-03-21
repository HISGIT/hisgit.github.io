---
layout: post #default,post,page,home,categories,tags,collection,category,tag
title:  "随时修改主题代码"
# alt_title: "Basically Basic"
sub_title: "定制主题注定要走上自己编码主题的道路"
date:   2026-03-14 21:50:00 +0900
read_time: true
ref: apply-to-new-theme
comments:
  host: wxw.moe
  username: ToT
  id: 116227599453343515
introduction: |
    **Basically Basic** 是 Jekyll 默认主题--- *[Minima](https://github.com/jekyll/minima)*的一个替代。在Minima中有的用法和功能都能在**Basically Basic** 中得到完整的支持。
---
## 目录
1. 基础主题
2. 用不同方式安装 *jekyll-theme-basically-basic* 主题
3. 部分实现多语言功能
4. 内联代码背景色问题
5. 自动添加并生成友链页面
6. 将 Mastodon toot 作为评论
7. 更改字体样式
8. 参考

## 基础主题
Minima 主题是 Jekyll 的默认主题。它简单、干净、易于使用。我们可以在 `_config.yml` 文件中找到如下配置代码：
{% highlight json linenos %}
# Build settings
theme: minima
plugins:
  - jekyll-feed
{% endhighlight %}
也可以在 `Gemfile` 中看到：
{% highlight json linenos %}
# This is the default theme for new Jekyll sites. You may change this to anything you like.
gem "minima", "~> 2.5"
{% endhighlight %}

然而，它太基础，无法满足我的需求。作为普通用户（非开发者），我想要一个类似 Minima 但具有更多功能和可定制选项的主题。因此我找到了一个名为 *[Basically Basic](https://github.com/jekyll/minima)* 的主题。
## 不同方式安装主题
通过 Ruby gem 或 Git 安装，按 GitHub 仓库的 README 操作。

使用 Ruby gem 安装是最简单的方法。只需在 `_config.yml` 和 `Gemfile` 中更改代码。
向 Jekyll 站点的 `Gemfile` 添加这行：
{% highlight json linenos %}
gem "jekyll-theme-basically-basic"
{% endhighlight %}
向 Jekyll 站点的 `_config.yml` 添加这行：
{% highlight json linenos %}
theme: jekyll-theme-basically-basic
{% endhighlight %}
然后运行 `bundle` 命令安装主题 gem 和依赖：
{% highlight js linenos %}
bundle install
{% endhighlight %}
运行安装命令后，你可能会看到类似输出：
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/Screenshot 2026-02-06 at 23.28.49.png)
运行 `bundle exec jekyll serve` 命令后，你可以在 `http://localhost:4000` 看到新主题已应用到你的 Jekyll 站点。

最后，让我们试试手动安装方式。先从 GitHub 仓库 *[jekyll-theme-basically-basic](https://github.com/mmistakes/jekyll-theme-basically-basic)* 下载原始代码，然后查看文件结构：
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
然后将下载目录中的文件复制到你的 Jekyll 站点目录：
{% highlight js linenos %}
cp -a jekyll-theme-basically-basic/{_layouts,_includes,assets,_sass,_data,_config.yml} path/to/myblog
{% endhighlight %}
然后像以前一样更改 `Gemfile` 和 `_config.yml` 以使用该主题：
{% highlight js linenos %}
# Gemfile
gem "jekyll-theme-basically-basic"

# _config.yml
theme: jekyll-theme-basically-basic
{% endhighlight %}
最终主题就应用到你的 Jekyll 站点了，并且你可以随时修改主题代码。
## 部分实现多语言功能
该主题没有内建多语言功能，因为 Jekyll 是静态站点生成器。但我们可以用一些变通方法实现这个目标。
只要我在 Google 搜索 “jekyll multilingual”，就能找到一些解决方案，比如 *[jekyll-multiple-languages-plugin](https://github.com/Anthony-Gaudino/jekyll-multiple-languages-plugin)*。

可能还有其他方式实现多语言功能。经过浏览 *[multilingual-jekyll-websites](https://www.usecue.com/blog/multilingual-jekyll-websites/)* 并多次尝试 git hard-reset 后，终于找到一种实现方法：将内容分为不同语言文件，并用 front-matter `ref` 来关联同一内容的不同语言文件，并在右上角放置语言选择器。

例如，在 `_posts` 目录中创建两个文件 `_posts/en/2026-01-16-this-way-we-make-it-and-again.markdown` 和 `_posts/zh/2026-01-16-this-way-we-make-it-and-again.markdown`，并分别用不同语言编写内容。然后用 front matter `ref` 来关联它们。只有 `language: en` 的文件会显示在首页，其他语言文件会隐藏。点击语言选择器时，才会显示其他语言文件的内容。

在 `_config.yml` 中添加如下代码，为不同语言文件设置 permalink 和 language：
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

`_includes/posts-all.html` 文件：
{% highlight html linenos %}{% raw %}
{% assign posts = site.posts | where:'language', site.lang %}
{% for post in posts %}
  {% include entry.html %}
{% endfor %}
{% endraw %}
{% endhighlight %}

然后，在文章页面右上角在 `_includes/masthead.html` 中添加一个 [语言选择器](https://github.com/HISGIT/hisgit.github.io/commit/7f828eed1fba6c40b5f2706070fbd3aef9ce50e1#diff-5ca4edb2e5a8b2d7e97c0e91357a897fa1f1432e5eab143198ec7e9b7c2b8325R19-R42)，如下所示：
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

样式文件 `_sass/basically-basic/_sidebar.scss`：
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

为避免同名文章重复显示问题，只有 `_posts/en` 文件夹中的文章保留 `tags`/`tag` 和 `categories`/`categorie` front matter。其他非英文文章移除这些 front matter。
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/multilingual_selector_post.png)
<p style="text-align: center; font-weight: bold;">文章内的多语言选择</p>
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/archives_page.png)
<p style="text-align: center; font-weight: bold;">归档页面</p>

## 内联代码背景色问题
应用新主题后，内联代码的背景色被破坏了。为解决此问题，在 `assets/stylesheets/main.scss` 文件中添加内联代码背景色，如下所示：
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

## 自动添加并生成友链页面
是时候为博客添加友链页面了。首先，在站点根目录添加新文件 `links.md`，并写入如下 front matter：
{% highlight json linenos %}{% raw %}
---
layout: blogroll
title: Links
permalink: /blogroll/
---
{% endraw %}
{% endhighlight %}

添加文件 `_layouts/blogroll.html` 作为内容页面。对于友链页面，我更倾向于每个友链选取最近 90 天内最新的 3 篇文章，按更新时间降序排列，全部自动生成，这个思路来自 *[automatic-blogroll](https://www.alexmolas.com/2023/07/20/automatic-blogroll.html)*。我改写了 Python 脚本 `build_blogroll.py` 并添加了记录友链的 `_data/websites.txt` 文件。然后运行脚本生成友链页面。
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/blogroll_python_script.png)
友链页面生成成功。
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/links_page.png)

## 将 Mastodon toot 作为评论
通常，为静态博客添加评论功能需要引入插件，但应该有不使用插件的办法。所以，我找到了一个通过 Mastodon API 和一些 JavaScript 代码在 [`comments.html`](https://github.com/HISGIT/hisgit.github.io/blob/main/_includes/comments.html) 文件中实现 *[将 Mastodon toot 作为评论](https://carlschwan.eu/2020/12/29/adding-comments-to-your-static-blog-with-mastodon/)* 的方法。

接下来，在文章布局文件 `_layouts/post.html` 中包含 `comments.html`，如下：
{% highlight html linenos %}{% raw %}
{% include comments.html %}
{% endraw %}{% endhighlight %}

现在，为了启用评论，在 front matter 中添加如下信息：
{% highlight json linenos %}{% raw %}
comments:
  host: wxw.moe
  username: ToT
  id: xxxxxxx
{% endraw %}
{% endhighlight %}
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/comments_frontmatter.png)

发布文章时，只需写一条 toot 包含你文章的链接。文章页面将显示一个“加载评论”按钮，而不是每次请求时都加载评论。
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/loaded_comments.png)
<p style="text-align: center; font-weight: bold;">已加载评论</p>

## 更改字体样式
在拜读 *[Revivance Blog](https://revivance.blog)* 后，我对它的排版字体风格印象深刻，决定在自己的博客中采用类似风格。

修改 SCSS 文件 *[_sass/basically-basic/_base.scss](https://github.com/HISGIT/hisgit.github.io/blob/main/_sass/basically-basic/_base.scss)* 中的 `body` 部分：
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

为更改标题字体样式，我更新了 `_sass/basically-basic/_variables.scss` 中的代码，将基础字体族从原来的：
{% highlight css linenos %}{% raw %}
$base-font-family: "Fira Sans", sans-serif !default;
{% endraw %}{% endhighlight %}
改为：
{% highlight css linenos %}{% raw %}
$base-font-family: "Freight Text W03 Book", "Noto Serif SC", georgia, "Songti SC", Simsun, serif;
{% endraw %}{% endhighlight %}
完成。

## 参考
1. *jekyll-theme-basically-basic*: `https://github.com/mmistakes/jekyll-theme-basically-basic`
2. *Basically Basic*: `https://github.com/jekyll/minima`
3. *automatic-blogroll*: `https://www.alexmolas.com/2023/07/20/automatic-blogroll.html`
4. *adding-comments-to-your-static-blog-with-mastodon*: `https://carlschwan.eu/2020/12/29/adding-comments-to-your-static-blog-with-mastodon/`
5. *revivance.blog*: `https://revivance.blog`
6. *multilingual-jekyll-websites*: `https://www.usecue.com/blog/multilingual-jekyll-websites/`
