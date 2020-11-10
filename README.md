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

# 更换国内镜像

```
# windows系统使用cmd快速设置
pip install pip -U    # 升级pip到最新版本
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

# 安装依赖

```cmd
pip install -r requirements.txt
```



# 项目部署注意事项

## 图片中的中文乱码问题

打开python的安装路径，找到“F:\Install\python3.7\Lib\site-packages\matplotlib\mpl-data”路径下的matplotlibrc文件，

将#font.sans-serif : DejaVu Sans, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif这一行注释去掉，并且在冒号后面加“SimHei,”

将#axes.unicode_minus  : True这一行注释去掉，将true改成false

https://jingyan.baidu.com/article/908080223cd201fd91c80fd5.html