## JobRecruitment



### 10.21 wjy更新
完成了私信逻辑的实现。前端界面还未优化。

新增网站首页和个人首页进入私信板块内容。
修复了私信板块选择超级用户而非普通用户的bug。
（私信首页和发送还暂时还有bug）

### 10.20 wjy更新
新增私信板块PrivateMessage，可通过http://127.0.0.1:8000/privatemessage/inbox访问。




### 快速启动

#### `local_settings.py`配置

由于项目中使用的一些配置均为敏感配置，因此建议您在`settings.py`的同级目录下新建文件`local_settings.py`文件用以存放这些配置。该文件中的配置会被导入并且覆盖`settings.py`中的配置。

#### 数据库迁移

在启动项目之前，你需要迁移数据库。此处以MySQL为例，在`JobRecruitment/local_settings.py`中配置你的数据库内容：

```python
# /JobRecruitment/local_settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jobrecruitment',  # 数据库名字
        'USER': '',  #用户名
        'PASSWORD': '', #用户密码
        'HOST': '127.0.0.1',  # MySQL 在哪个 ip
        'PORT': '3306',  # 端口号
    }
}
```

完成上述配置后，执行迁移数据库的操作：

```bash
python manage.py makemigrations
python manage.py migrate
```

为了便于操作数据库内容，你还可以创立超级用户来管理数据库内容：

```bash
python manage.py createsuperuser
```

#### 邮件通知配置

在`UserAuth`模块使用了邮箱验证码通知来完成新用户的注册校验，所以为了成功启动本项目，你需要在`local_settings.py`配置邮件通知。你需要生成邮箱服务授权码来授权Django以你的名义发送邮件。在QQ邮箱中，可以在`设置->账户`中生成授权码。

而后在`local_settings.py`中按如下说明配置：

```python
# 发送邮箱验证码
EMAIL_HOST = "smtp.qq.com"     # 服务器
EMAIL_PORT = 25                 # 一般情况下都为25
EMAIL_HOST_USER = "example@qq.com"     # 账号
EMAIL_HOST_PASSWORD = ""     # 您的授权码
EMAIL_USE_TLS = True       
EMAIL_FROM = "example@qq.com"      # 邮箱来自（这里是和账号一样的）
EMAIL_TITLE = '邮箱激活'	# 邮件标题
```

**请务必注意，为了隐私，不要将上述配置尤其是授权码放在`settings.py`传到git仓库中！**

完成上述配置后，即可启动服务（默认8000端口）：

```bash
python manage.py runserver
```

