from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from user.models import User
from user.forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    # 로그인 상태를 확인하여 사용명을 구분하여 출력할 수 있도록 처리한다.
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "AnonymousUser"

    return render(request, "index.html", {"username": username})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    error = None
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # User 인증. 자격 증명이 유효한 경우 User 객체를 그렇지 않을 경우 None 반환
            user = authenticate(request, username=username, password=password)

            # 사용자가 있을 경우 로그인 처리하고 없을 경우에는 오류 메시지를 생성한다.
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                error = "유저명 또는 비밀번호가 올바르지 않습니다."
        else:
            error = "잘못된 입력 형식입니다. 다시 입력하세요."
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form": form, "error": error})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요
    logout(request)
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
# 여기서는 index.html로 redirect하기 위해 login_required를 선언하지 않는다.
# @login_required
def user_list_view(request):
    # 사용자 로그인 상태가 아닌 경우 로그인 화면으로 이동한다.
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    
    # TODO: 7. /users 에 user 목록을 출력해주세요
    users = User.objects.all().order_by("-id")

    # TODO: 9. user 목록은 pagination이 되게 해주세요
    paginator = Paginator(users, 5)
    page = int(request.GET.get("page", 1))
    users = paginator.get_page(page)

    return render(request, "users.html", {"users": users})
