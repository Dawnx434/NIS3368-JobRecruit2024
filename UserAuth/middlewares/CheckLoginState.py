from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class CheckLoginStateMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(request.path_info)
        # 如果访问验证模块UserAuth下的URL，理应都应该允许
        if '/auth/' in request.path_info:
            return None

        # 均不满足访问控制条件，则要求登录
        return redirect('/auth/login/')

    def respond_request(self, request, response):
        return response
