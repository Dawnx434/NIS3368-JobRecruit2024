# UserAuth用户验证模块

## 支持的访问路径

```python
path("login/", views.login),
path("register/", views.register),
path("gencode/", views.generate_verification_code),
path("state/", views.check_login_state),
path("logout/", views.logout)
```
`login/`和`register/`提供登录注册页面，`gencode/`支持生成验证码，`state/`验证登录状态，`logout/`提供登出功能。


