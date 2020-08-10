# spss
多元回归分析网页版

# 更新当前项目为最新项目

cmd进入manage.py的目录

```cmd
git fetch origin master
git reset --hard
git merge origin/master
```

三句命令的意义是：下载最新代码，放弃本地版本，合并远端和本地仓库



如果执行 git fetch origin master出现下面：

```cmd
fatal: HttpRequestException encountered.
   发送请求时出错。
Username for 'https://github.com':
```

此时输入github账号和密码，此处的Username是github账号的邮箱。