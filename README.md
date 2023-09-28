## JobRecruitment
项目配置前需在本地加上local_settings.py配置文件
格式如下
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jobrecruitment',  # 数据库名字
        'USER': 'root',             # 数据库用户ID
        'PASSWORD': 'your_passwd', # 数据库密码
        'HOST': '127.0.0.1',  # MySQL 在哪个 ip
        'PORT': '3306',  # 端口号
    }
}
```
## to do list
将手机号验证改为邮箱验证（这里要验证邮箱）