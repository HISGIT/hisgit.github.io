---
layout: post #default,post,page,home,categories,tags,collection,category,tag
title:  "Feel Free to Customize the Theme Code"
# alt_title: "Basically Basic"
sub_title: "Theme customisation leads to code the theme by yourself"
date:   2026-03-14 21:50:00 +0900
categories: Jekyll
read_time: true
ref: apply-to-new-theme
comments:
  host: wxw.moe
  username: ToT
  id: 116227599453343515
introduction: |
    **Basically Basic** is a Jekyll theme meant to be a substitute for the default --- *[Minima](https://github.com/jekyll/minima)*. Conventions and features found in Minima are fully supported by **Basically Basic**.
---
## Contents Table
1. Basic theme
2. Install *jekyll-theme-basically-basic* theme in different ways
3. Implement multilingual feature partly
4. Inline code background color problem
5. Add and generate Links page automatically
6. Make Mastodon toots as comments
7. Change font style
8. Reference

## Basic Theme
The Minima theme is the default theme for Jekyll. It is simple, clean, and easy to use. We can find the configuration code in `_config.yml` file like below:
{% highlight json linenos %}
# Build settings
theme: minima
plugins:
  - jekyll-feed
{% endhighlight %}
Also in `Gemfile`:
{% highlight json linenos %}
# This is the default theme for new Jekyll sites. You may change this to anything you like.
gem "minima", "~> 2.5"
{% endhighlight %}

However, it is too basic to meet my needs. As a regular user (not a developer), I wanted a theme similar to Minima but with more features and customization options. So I found a theme called *[Basically Basic](https://github.com/jekyll/minima)*.
## install theme in different ways
Install by Ruby gem or using Git follow the README of the github repository.

Install by Ruby gem is the easiest way. Just change the code in `_config.yml` and `Gemfile` like below. 
Add this line to your Jekyll site's `Gemfile`:
{% highlight json linenos %}
gem "jekyll-theme-basically-basic"
{% endhighlight %}
Add this line to your Jekyll site's `_config.yml` file:
{% highlight json linenos %}
theme: jekyll-theme-basically-basic
{% endhighlight %}
Then run the `bundle` command to install the theme gem and dependencies:
{% highlight js linenos %}
bundle install
{% endhighlight %}
After running the install command, you may see output like this:
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/Screenshot 2026-02-06 at 23.28.49.png)
run the `bundle exec jekyll serve` command, you can see the new theme applied to your Jekyll site at `http://localhost:4000`.

Finally, let's explore the manual installation method. First, download the original code from the GitHub repository *[jekyll-theme-basically-basic](https://github.com/mmistakes/jekyll-theme-basically-basic)*, and look at the file structure:
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
Then copy the files in the downloaded folder to your Jekyll site folder:
{% highlight js linenos %}
cp -a jekyll-theme-basically-basic/{_layouts,_includes,assets,_sass,_data,_config.yml} path/to/myblog
{% endhighlight %}
And as done before, change the `Gemfile` and `_config.yml` file to use the theme:
{% highlight js linenos %}
# Gemfile
gem "jekyll-theme-basically-basic"

# _config.yml
theme: jekyll-theme-basically-basic
{% endhighlight %}
finally theme is applied to your Jekyll site and can change the theme code anytime as you like.
## Implement multilingual feature partly
Multilingual feature is not supported by the theme, beacause jekyll is a static site generator. But we can use some workarounds to achieve this goal.
As long as I search google for "jekyll multilingual", I can find some solutions like *[jekyll-multiple-languages-plugin](https://github.com/Anthony-Gaudino/jekyll-multiple-languages-plugin)*.

it's possible that there exists another wey to implement multilingual feature. After exploring *[multilingual-jekyll-websites](https://www.usecue.com/blog/multilingual-jekyll-websites/)* and experimenting attempts with serveral times git hard-reset, finally find a way to implement multilingual feature: seperate the content in different language files, and use front-matter `ref` to related the same content in different language files, place language-selector on the top-right corner. 

For example, create two files `_posts/en/2026-01-16-this-way-we-make-it-and-again.markdown` and `_posts/zh/2026-01-16-this-way-we-make-it-and-again.markdown` in the `_posts` folder, and write the content in different languages in these two files. Then use the front matter `ref` to link them. Only the `language: en` file is shown on the home page, and the others are hiddened. When clicking the language selector, the content in the other language file is shown.

In `_config.yml`, add some code like below to set the permalink and language for different language files:
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

`_includes/posts-all.html` file:
{% highlight html linenos %}{% raw %}
{% assign posts = site.posts | where:'language', site.lang %}
{% for post in posts %}
  {% include entry.html %}
{% endfor %}
{% endraw %}
{% endhighlight %}

Then, at the top-right corner of the post page, add a [language selector](https://github.com/HISGIT/hisgit.github.io/commit/7f828eed1fba6c40b5f2706070fbd3aef9ce50e1#diff-5ca4edb2e5a8b2d7e97c0e91357a897fa1f1432e5eab143198ec7e9b7c2b8325R19-R42) in `_includes/masthead.html` like below:
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

Style file `_sass/basically-basic/_sidebar.scss`:
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

To avoid the problem of duplicated same-title posts, only the post in the `_posts/en` folder has `tags`/`tag` and `categories`/`categorie` front matter. Remove these front matter in the other non-English posts.
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/multilingual_selector_post.png)
<p style="text-align: center; font-weight: bold;">Multilingual selector in post</p>
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/archives_page.png)
<p style="text-align: center; font-weight: bold;">Archives page</p>

## Inline Code Background Color Problem
After applying the new theme, the background color of inline code was broken. To fix this, add some the background color of inline code in the `assets/stylesheets/main.scss` file as follows:
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

## Add and Generate Links Page Automatically
It's time to add a Links page to the blog. First, add a new file `links.md` in the root folder of the Jekyll site, and write the front matter like below:
{% highlight json linenos %}{% raw %}
---
layout: blogroll
title: Links
permalink: /blogroll/
---
{% endraw %}
{% endhighlight %}

Add the file `_layouts/blogroll.html` as a content file. For the links page, I prefer 3 latest posts in the last 90 days per friend's link, ordered by the update time of post descending, and all generated automatically, inspired by *[automatic-blogroll](https://www.alexmolas.com/2023/07/20/automatic-blogroll.html)*. Twisted the Python script `build_blogroll.py` and added the `_data/websites.txt` file that store friends' blog URLs. Then, I ran the script to generate the links page.
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/blogroll_python_script.png)
The links page was generated successfully.
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/links_page.png)

## Make Mastodon Toots as Comments
Typically, adding comments to a static blog requires importing a plugin, but there should be a way to do it without one. Instead, I found a way to *[make Mastodon toots as comments](https://carlschwan.eu/2020/12/29/adding-comments-to-your-static-blog-with-mastodon/)* by using the Mastodon API and some JavaScript code in the [`comments.html`](https://github.com/HISGIT/hisgit.github.io/blob/main/_includes/comments.html) file.

Next, include `comments.html` in the post layout file `_layouts/post.html` like below:
{% highlight html linenos %}{% raw %}
{% include comments.html %}
{% endraw %}{% endhighlight %}

Now, add the following information to the front matter to enable comments:
{% highlight json linenos %}{% raw %}
comments:
  host: wxw.moe
  username: ToT
  id: xxxxxxx
{% endraw %}
{% endhighlight %}
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/comments_frontmatter.png)
When publishing a post, simply write a toot linking to your article. The post page will display a button to load comments instead of loading them for every request.
![Screenshot](/assets/post_images/2026-01-11-apply-to-new-theme/loaded_comments.png)
<p style="text-align: center; font-weight: bold;">Loaded comments</p>

## Change Font Style
After exploring the *[Revivance Blog](https://revivance.blog)*, I was impressed by its ***typography*** font style and decided to adopt a similar font style for my blog.

Change the SCSS file *[_sass/basically-basic/_base.scss](https://github.com/HISGIT/hisgit.github.io/blob/main/_sass/basically-basic/_base.scss)* in the `body` section:
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

To alter the title font style, I updated the code in `_sass/basically-basic/_variables.scss`, configured the base font family from the original:
{% highlight css linenos %}{% raw %}
$base-font-family: "Fira Sans", sans-serif !default;
{% endraw %}{% endhighlight %}
To:
{% highlight css linenos %}{% raw %}
$base-font-family: "Freight Text W03 Book", "Noto Serif SC", georgia, "Songti SC", Simsun, serif;
{% endraw %}{% endhighlight %}
done.

## Reference
1. *jekyll-theme-basically-basic*: `https://github.com/mmistakes/jekyll-theme-basically-basic`
2. *Basically Basic*: `https://github.com/jekyll/minima`
3. *automatic-blogroll*: `https://www.alexmolas.com/2023/07/20/automatic-blogroll.html`
4. *adding-comments-to-your-static-blog-with-mastodon*: `https://carlschwan.eu/2020/12/29/adding-comments-to-your-static-blog-with-mastodon/`
5. *revivance.blog*: `https://revivance.blog`
6. *multilingual-jekyll-websites*: `https://www.usecue.com/blog/multilingual-jekyll-websites/`