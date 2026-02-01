---
layout: post
title:  "Build a Jekyll blog"
sub_title: "even if not understanding ruby or javascrip"
tags: Jekyll
ref: build-a-jekyll-blog
# actions:
#   - label: "Learn More"
#     icon: github  # references name of svg icon, see full list below
#     url: "http://url-goes-here.com"
#   - label: "Download"
#     icon: download  # references name of svg icon, see full list below
#     url: "http://url-goes-here.com"
date: 2026-01-20 22:35:00 +0900
categories: Jekyll
read_time: true
introduction: |
    **Build a static blog from scratch and deploy it via GitHub Pages**.
---

## Table of Contents
1. Why choose Jekyll
2. Local deployment and testing
3. GitHub automatic build and deployment
4. Custom domain configuration
5. Afterword — Markdown issues and theme customization
6. After-afterword — After implementing multilingual support

## Why choose Jekyll
1. Static pages, easy to deploy
2. Markdown Supports
3. Simple, but not simplistic; functionality can be gradually improved through plugins

In the end, pick on Jekyll.

## Local deployment and testing
According to the [official documentation -> Jekyll on macOS](https://jeky llrb.com/docs/installation/macos/),  
First you need to install Ruby. I spent a bit of more time on this step due to slowl internet speed.

{% highlight shell linenos %}{% raw %}
# Use curl to fetch the Ruby installation script and execute it with bash
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

At this step, if the displayed Ruby version matches the version shown after running  
`echo "chruby ruby-3.x.x"`, the installation was successful.

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

After seeing the successful startup message with the service address  
`Server address: http://127.0.0.1:4000/`,  
you can visit this address to see your blog content.  
This is also the usual way to debug and preview the final appearance of posts.

## GitHub automatic build and deployment

First, create a new repository on GitHub use your GitHub account.

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/creat_new_repository.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/creat_new_repository_1.png)

After the local run succeeds, upload the project to GitHub, then deploy it via GitHub Pages.  
You could also say this is the official publication of your blog posts — a shocking first release!

{% highlight shell linenos %}{% raw %}
# Initialize a local Git repository
git init
# Add the remote Git repository address
# https://github.com/HISGIT/myblog.git is the remote repository address; please change it to your own.
git remote add origin https://github.com/HISGIT/myblog.git
# Rename the main branch
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

After completing this step, continue configuring things on GitHub.

On the GitHub repository page, go to  
`setting -> code and automation -> Pages`  
and modify the `Build and deployment` settings:

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_repository_setting.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_actions_create0.png)

Change this to `Github Action`.

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/jekyll_workflowfile_edit_01.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/jekyll_workflowfile_edit_02.png)

Here we directly submit it, and GitHub will automatically build and deploy the site.

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_building_01.png)

Check the build process detailes in the `Action` page to see if there are any errors.

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_building_02.png)

It turned red — the build failed.  
Click red mark and it reveals an important message:

{% highlight shell linenos %}{% raw %}
Please run `bundle lock --normalize-platforms` and commit the resulting lockfile.
Alternatively, you may run `bundle lock --add-platform <list-of-platforms-that-you-want-to-support>`
public_suffix-7.0.2 requires ruby version >= 3.2, which is incompatible with the
current version, 3.1.6
Error: The process '/opt/hostedtoolcache/Ruby/3.1.6/x64/bin/bundle' failed with exit code 5
{% endraw %}
{% endhighlight %}

Obviously, the Ruby version used during the build is too old.  
We need to go back and modify the Workflow file: `jekyll.yml`.

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_change_rubyersion-01.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/workflow_actions_change_rubyersion-02.png)

After changing `ruby-version` to the latest `3.4.1`, submit and push it to the GitHub repository again.

Check `Action` again and you should see that the build and deployment are now successful.

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/action_build_sucessful_01.png)

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/action_build_sucessful_02.png)

Then visit the blog site URL shown in the deploy information:  
http://blog.contextmode.xyz/myblog/

Mostly it should look like  [your GitHub username].github.io,
for example: http://hisgit.github.io.

Because a custom domain has already been enabled in my repository, it’s not a GitHub subdomain here.  
it automatically redirects from the GitHub subdomain to the custom domain.

## Custom domain configuration
To use a custom domain with GitHub Pages, you need to add domain settings  
both at your DNS provider and in your GitHub account settings.

### GitHub domain verification
Using the subdomain `blog.contextmode.xyz` as an example:

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_01.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_02.png)
![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_03.png)

Copy the two values provided here; they will be used in the DNS provider configuration.

### DNS configuration
At your DNS (hosting) provider, such as Cloudflare, add a TXT record.

Go to domain management, select the relevant domain,  
find the DNS settings, and add a record with type TXT.  
Paste the copied values into the Name and Content fields separately.

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_04.png)

Click save and wait for it to take effect.

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/github_account_domain_varification_05.png)

Here you can see whether verification succeeded — green for Verified, red for Unverified.  
Sometimes DNS propagation takes a little more time, so please be patient.

### Add a CNAME pointing to GitHub Pages
As shown below, add a CNAME record in DNS management  
pointing to the [your GitHub username].github.io address shown after deploy successfully.

![screenshot](/assets/2026-01-11-Build-a-Jekyll-blog/cname_to_github_pages.png)

After all configurations are complete, whether you access  
[your GitHub username].github.io or the custom domain,  
you will reach the custom domain at last.  
Essentially, this setup redirects GitHub Pages traffic to your own domain.

## Afterword — Markdown and theme customization
In follow-up posts, the following topics will be discussed in detail:
1. Using Markdown in Jekyll
2. Syntax highlighting and code block display
3. Theme setup and customization

## After-afterword — Implementing multilingual support
done.