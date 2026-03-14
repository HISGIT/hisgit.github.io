---
layout: post #default,post,page,home,categories,tags,collection,category,tag
title:  "手軽にテーマコードを変更しよう"
# alt_title: "Basically Basic"
sub_title: "テーマのカスタマイズは自分でコードを書く道に導く"
date:   2026-02-03 22:00:00 +0900
categories: Jekyll
read_time: true
# ref: apply-to-new-theme
introduction: |
    Basically Basic は Jekyll デフォルトテーマの代わりものとしている --- [Minima](https://github.com/jekyll/minima). Minimaにある全ての便利性と機能も整っていて、**Basically Basic**である。
---

## 目次
1. 基本のテーマ
2. [jekyll-theme-basically-basic](https://github.com/mmistakes/jekyll-theme-basically-basic) テーマを適用するのやり方
3. 不完全な多言語機能を実装する
4. インラインコードの背景色の問題
5. Links page を自動的に追加・生成する <!-- https://github.com/alexmolas/alexmolas.github.io/tree/master -->
6. マストドンのトートをコメントにする <!-- https://carlschwan.eu/2020/12/29/adding-comments-to-your-static-blog-with-mastodon/ -->
7. フォントスタイルを変える　<!-- https://revivance.blog -->

## 基本のテーマ
Minima と言うテーマは Jekyll の基本テーマである。シンプルで使いやすい。 `_config.yml` ファイルに以下の設定コードがある:
{% highlight shell linenos %}
# Build settings
theme: minima
plugins:
  - jekyll-feed
{% endhighlight %}
`Gemfile`ファイルにも:
{% highlight shell linenos %}
# This is the default theme for new Jekyll sites. You may change this to anything you like.
gem "minima", "~> 2.5"
{% endhighlight %}

But it is too simple to meet my needs. As a normal but not hacker user, I want to find a theme which is similar to Minima but has more features and customisation options.
So I found a theme called [Basically Basic](https://github.com/jekyll/minima)

## Basic theme in different ways
Install by Ruby gem or using Git Follow the README of the github repository.

Install by Ruby gem is the easiest way. Just change the code in `_config.yml` and `Gemfile` like below:
Add this line to your Jekyll site's `Gemfile`:
{% highlight shell linenos %}
gem "jekyll-theme-basically-basic"
{% endhighlight %}
Add this line to your Jekyll site's `_config.yml` file:
{% highlight shell linenos %}
theme: jekyll-theme-basically-basic
{% endhighlight %}
Then run Bundler to install the theme gem and dependencies:
{% highlight shell linenos %}
bundle install
{% endhighlight %}
After running the install command, you may see output like this:
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/Screenshot 2026-02-06 at 23.28.49.png)
Finally there we are the Manually way.
let's
{% highlight shell linenos %}

{% endhighlight %}

## reference
1. [alexmolas.github.io](https://github.com/alexmolas/alexmolas.github.io/tree/master)
2. [adding-comments-to-your-static-blog-with-mastodon](https://carlschwan.eu/2020/12/29/adding-comments-to-your-static-blog-with-mastodon/)
3. [revivance.blog](https://revivance.blog)