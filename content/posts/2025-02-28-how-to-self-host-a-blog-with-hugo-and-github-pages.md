---
title: "How to self-host a blog with Hugo and GitHub Pages"
date: 2025-02-28
draft: false
toc: true
tags: ["Self", "Host", "Blog", "Hugo", "Github"]
categories: ["Infrastructure", "Self-Hosting"]
summary: "A comprehensive guide on How to self-host a blog with Hugo and GitHub Pages."
---

# How to self-host a blog with Hugo and GitHub Pages

Self-hosting a blog has never been easier with the advent of static site generators like Hugo and hosting services like GitHub Pages. This tutorial will guide you through setting up a blog using Hugo and publishing it to GitHub Pages, providing a cost-effective, scalable, and fast solution for sharing your content online.

## Prerequisites

Before diving into the process, ensure you have the following prerequisites:

1. **Basic Knowledge of Git**: Familiarity with Git basics is necessary as we'll use GitHub for version control and deployment.
2. **GitHub Account**: Create a GitHub account if you don't have one already.
3. **Git Installed**: Ensure Git is installed on your local machine. You can download it from [Git's official website](https://git-scm.com/).
4. **Hugo Installed**: Install Hugo by following the instructions on [Hugo's official website](https://gohugo.io/getting-started/installing/).
5. **Text Editor**: Use a text editor like VSCode, Atom, or Sublime Text for editing files.

## Step-by-step Guide

### Step 1: Install Hugo

First, we need to install Hugo on your system. If you haven't done so, follow the detailed instructions on the [Hugo installation page](https://gohugo.io/getting-started/installing/). For most systems, you can use a package manager:

- **macOS**: Use Homebrew.
  ```bash
  brew install hugo
  ```
- **Windows**: Use Chocolatey.
  ```bash
  choco install hugo -confirm
  ```
- **Linux**: Use package managers like APT or DNF depending on your distribution.

### Step 2: Create a New Hugo Site

Create a new Hugo site by executing the following command in your terminal:

```bash
hugo new site myblog
```

This creates a new directory named `myblog` with the necessary structure for a Hugo site.

### Step 3: Add a Theme

Navigate to your new site directory and add a theme. You can find a list of themes on [Hugo Themes](https://themes.gohugo.io/). For this tutorial, we'll use the "Ananke" theme.

```bash
cd myblog
git init
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
```

Next, update your `config.toml` to use the Ananke theme:

```toml
baseURL = "http://example.org/"
languageCode = "en-us"
title = "My Blog"
theme = "ananke"
```

### Step 4: Create Content

Create your first post using Hugo's built-in command:

```bash
hugo new posts/my-first-post.md
```

Edit the newly created file in `content/posts/my-first-post.md` and add your content using Markdown syntax. Here's a simple example:

```markdown
---
title: "My First Post"
date: 2023-10-01T12:00:00Z
draft: false
---

Welcome to my first blog post using Hugo and GitHub Pages!
```

### Step 5: Build the Site

Generate the static files by running:

```bash
hugo
```

This command creates the `public` directory containing your site's static files.

### Step 6: Deploy to GitHub Pages

#### Create a GitHub Repository

1. Go to GitHub and create a new repository named `username.github.io`, replacing `username` with your GitHub username. This naming convention is crucial for personal GitHub Pages.

#### Push Your Site to GitHub

1. Initialize a new Git repository in the `public` directory.

```bash
cd public
git init
```

2. Add the remote repository.

```bash
git remote add origin https://github.com/username/username.github.io.git
```

3. Add and commit your files.

```bash
git add .
git commit -m "Initial commit"
```

4. Push your changes to GitHub.

```bash
git push -u origin master
```

Your site should be live at `https://username.github.io`.

### Step 7: Automate Deployment

To automate the deployment process, we can use a GitHub Action. First, create a `.github/workflows/gh-pages.yml` file in your main `myblog` directory with the following content:

```yaml
name: Deploy Hugo site to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v2
      with:
        submodules: true  # Fetch Hugo themes (submodules)

    - name: Setup Hugo
      uses: peaceiris/actions-hugo@v2
      with:
        hugo-version: 'latest'

    - name: Build
      run: hugo --minify

    - name: Deploy
      uses: peaceiris/actions-gh-pages@v3
      with:
        personal_token: ${{ secrets.GITHUB_TOKEN }}
        external_repository: username/username.github.io
        publish_dir: ./public
```

Ensure your main branch is named `main` or update the YAML file accordingly.

## Security Considerations

1. **Personal Access Token**: If you need to use a personal access token for deployment, ensure it has the least permissions necessary and store it securely in GitHub Secrets.
2. **Sensitive Information**: Avoid including sensitive information in your repository, such as API keys or passwords.
3. **Repository Visibility**: Consider whether your repository should be public or private, depending on the content you are hosting.

## Troubleshooting

- **Site Not Updating**: Ensure you have committed and pushed changes to the correct branch. Check GitHub Actions logs for any build errors.
- **Custom Domain Issues**: If using a custom domain, ensure your DNS settings are correctly configured and that a `CNAME` file exists in your repository.
- **Hugo Errors**: Run `hugo server` locally to debug any build issues before deploying.

## Conclusion

Congratulations! You've successfully set up a blog using Hugo and GitHub Pages. This combination provides a lightweight, fast, and free way to host personal or professional blogs. As you explore further, consider customizing your theme, integrating third-party services, or even writing custom shortcodes and templates to enhance your site.

By following this guide, you now have the foundation to publish content effortlessly and make your voice heard in the digital world. Happy blogging!