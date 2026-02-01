---
layout: post
title:  "Build a Jekyll blog"
alt_title: "建一个Jekyll博客"
sub_title: "不会ruby和javascript也没关系"
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
    **从0开始构建一个通过GitHub Pages部署的静态网页blog**。
---

## 目录
1. 为什么选Jekyll
2. 本地部署测试
3. Github构建自动部署
4. 自定义域名配置
5. 后话～markdown问题和个性化义主题
6. 后后话～在多语言版本功能编码之后

## 为什么选Jekyll
1. 静态页面，部署简单
2. 支持Markdown格式编写
3. 简单但不简陋，通过插件能逐步完善功能

最终选定了Jekyll。
## 本地部署测试
按照[官方文档- > Jekyll on macOS](https://jeky llrb.com/docs/installation/macos/)，需要 先安装Ruby，稍微在这步费了点时间(博主网速比较慢)。
{% highlight shell linenos %}{% raw %}
# Use curl to fetch the Ruby installation bootstrap script and execute it with bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install chruby ruby-install
ruby-install ruby 3.4.1

# Write Ruby configuration into the shell config file ~/.zshrc 
# Or other shell configuration file  like ~/.bashrc depends on your system
echo "source $(brew --prefix)/opt/chruby/share/chruby/chruby.sh" >> ~/.zshrc
echo "source $(brew --prefix)/opt/chruby/share/chruby/auto.sh" >> ~/.zshrc
echo "chruby ruby-3.4.1" >> ~/.zshrc # run 'chruby' to see actual version

# Open a new terminal
ruby -v
{% endraw %}
{% endhighlight %}
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/check_ruby_version.png)
执行到这一步，如果显示出来的ruby 版本和执行 `echo "chruby ruby-3.x.x"` 命令后显示的版本一致，说明安装成功。

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
看到运行成功后提示的服务地址：`Server address: http://127.0.0.1:4000/`，访问这个地址就能看到自己的blog内容。平时也是通过这个方式进行调试和预览文章最终效果。

## Github自动构建部署

首先要在gitbug上新建一个代码仓库。
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/creat_new_repository.png)

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/creat_new_repository_1.png)

本地运行成功后，需要上传GitHub仓库，然后再通过GitHub Pages部署我们的代码，也可以说是发布我们的博文啦，震撼首发！
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
这一步完成后接着就在GitHub上操作修改配置。

在GitHub的仓库页面，在`setting->code and automation->Pages`修改 `Build and deployment`设置：
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_repository_setting.png)

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_actions_create0.png)
这里为改为 `Github Aciton`。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/jekyll_workflowfile_edit_01.png)

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/jekyll_workflowfile_edit_02.png)
这里我们直接提交，GitHub会自动进行构建并发布。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_building_01.png)
在`Action`页面查看构建的详细过程，检查是否有报错。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_building_02.png)
发现报红了，构建失败。点进去看到有重要提示：
{% highlight shell linenos %}{% raw %}
Please run `bundle lock --normalize-platforms` and commit the resulting lockfile.
Alternatively, you may run `bundle lock --add-platform <list-of-platforms-that-you-want-to-support>`
public_suffix-7.0.2 requires ruby version >= 3.2, which is incompatible with the
current version, 3.1.6
Error: The process '/opt/hostedtoolcache/Ruby/3.1.6/x64/bin/bundle' failed with exit code 5
{% endraw %}
{% endhighlight %}
很明显构建过程中使用的ruby版本太低，需要回头修改下前面的Workflow file：jekyll.yml.
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_change_rubyersion-01.png)

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_change_rubyersion-02.png)
修改 `ruby-version` 为最新的 `3.4.1` 后重新提交到GitHub仓库。

再进`Action`里查看，看到已经构建并发布成功。
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/action_build_sucessful_01.png)

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/action_build_sucessful_02.png)

然后访问deploy信息里的blog网站地址： http://blog.contextmode.xyz/myblog/ 即可。
正常应该是类似 [your GitHub username].github.io之类的，比如：http://hisgit.github.io。
之所以出来的不是GitHub的子域名，因为在我的仓库已经启用了自定义域名，所以自动从GitHub的子域名
跳转到自定义域名了。

## 自定义域名配置
GitHub Pages 使用自定义域名，需要分别在DNS服务商和GitHub账号设置里增加域名设置。
### GitHub域名认证
以子域名 `blog.contextmode.xyz` 为例，
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_01.png)

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_02.png)

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_03.png)
复制这里给出的两个值，需要在DNS服务商那里作为配置使用。

### DNS配置
在DNS服务（托管）商，比如cloudflare中，添加TXT记录。

进入Domains管理，点击相应的域名。
在里面找到DNS配置，增加一条recodes，type为TXT记录，将刚才复制出来的值分别放到Name和Content
中。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_04.png)
点击保存，然后等待生效。

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_05.png)
在这里能看到是否验证成功，绿色的Verified 和 红色Unverified。有时DNS生效需要些时间，请耐心等待。

### 增加CNAME指向GitHub Pages
如下图，在DNS管理中增加CNAME指向刚才发布成功后提示的[your GitHub username].github.io地址。
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/cname_to_github_pages.png)

全部配置完成后，不管在访问[your GitHub username].github.io 还是 自定义域名 时，最终都是访问 自定义域名。本质上就是通过配置实现了访问GitHub Pages时自动跳转到自己的域名。
## 后话～markdown和个性化义主题
后续将会对
1. Jekyll中的markdown使用
2. 高亮和代码块显示
3. 主题设置和修改

这三部分的内容详细说道。

## 后后话～实现多语言切换功能
完成。