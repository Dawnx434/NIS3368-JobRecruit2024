from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class CheckLoginStateMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(request.path_info)
        # 访问管理员页面，也应允许
        if '/admin/' in request.path_info:
            return None

        # 如果访问验证模块UserAuth下的URL，理应都应该允许
        if '/auth/' in request.path_info:
            return None

        # 均不满足访问控制条件，则检查是否是登录状态
        user_info = request.session.get("UserInfo")
        if not user_info:
            return redirect('/auth/login')
        return None

    def respond_request(self, request, response):
        return response
