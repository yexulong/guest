from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.views.decorators.http import require_POST

from sign.models.event import Event
from sign.models.guest import Guest


def index(request):
    print('request.GET:', request.GET)
    print('request.POST:', request.POST)
    # return HttpResponse('hello django!')
    return render(request, 'index.html')


@require_POST
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # response.set_cookie('user', username, 3600)         # 添加浏览器cookie
            request.session['user'] = username  # 将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')

            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


@login_required
def event_manage(request):

    event_list = Event.objects.all
    # username = request.COOKIES.get('user', '')                  # 读取浏览器cookie
    username = request.session.get('user', '')  # 读取浏览器session
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name_parm = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name_parm)
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all().order_by('id')
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': username,
                                                 'guests': contacts})


# 手机号搜索
@login_required
# @permission_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone_parm = request.GET.get('phone', '')
    guest_list = Guest.objects.filter(phone__contains=search_phone_parm)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': username,
                                                 'guests': contacts})


# 签到
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


# 签到动作
@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    guest_data = str(len(guest_list))
    sign_data = 0
    for guest in guest_list:
        if guest.sign:
            sign_data += 1

    phone = request.POST.get('phone', '')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html',
                      {'event': event, 'hint': 'phone error.', 'guest': guest_data, 'sign': sign_data})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html',
                      {'event': event, 'hint': 'event id or phone error.', 'guest': guest_data, 'sign': sign_data})

    result = Guest.objects.get(event_id=event_id, phone=phone)

    if result.sign:
        return render(request, 'sign_index.html',
                      {'event': event, 'hint': "user has sign in.", 'guest': guest_data, 'sign': sign_data})
    else:
        Guest.objects.filter(event_id=event_id, phone=phone).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success!',
                                                   'user': result,
                                                   'guest': guest_data,
                                                   'sign': str(int(sign_data) + 1)
                                                   })


# 注销
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response
