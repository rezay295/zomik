from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import *
from hashlib import sha256
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def password_hasher(password):
    return sha256(password.encode('utf-8')).hexdigest()


def index(request):
    return HttpResponse("Hello, world. You're at the Panel index.")


def login(request):
    if request.method == "POST":
        password = request.POST.get("password")
        email = request.POST.get("email")

        try:
            u = Member.objects.get(email=email, password=password_hasher(password))
            request.session['member_id'] = u.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return HttpResponseRedirect("/panel/dashboard/")
        except Member.DoesNotExist:
            return render(request, "login.html", {"Error": "کاربر مورد نظر یافت نشد!"})

    else:
        return render(request, "login.html", {})


def dashboard(request):
    id = request.session["member_id"]
    if not id:
        return HttpResponseRedirect("/panel/login/")
    context = {}
    context.update({"Member": Member.objects.get(id=id)})

    return render(request, "dashboard.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/panel/login/")


def add_catergory(request):
    id = request.session["member_id"]
    if not id:
        return HttpResponseRedirect("/panel/login/")
    context = {}
    context.update({"Member": Member.objects.get(id=id)})

    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            c = Category(title=title)
            c.save()
            context.update({"Success": "با موفقیت ثبت شد!"})
            return render(request, "add-category.html", context)
        else:
            context.update({"Error": "لطفا عنوان را وارد کنید"})
            return render(request, "add-category.html", context)
    else:
        return render(request, "add-category.html", context)


def list_catergory(request):
    id = request.session["member_id"]
    if not id:
        return HttpResponseRedirect("/panel/login/")
    context = {}
    context.update({"Member": Member.objects.get(id=id)})
    if request.method == "POST":
        category_id = request.POST.get("id")
        if category_id:
            c = Category.objects.get(id=category_id)
            c.delete()
            context.update({"Success": "باموفقیت حذف شد!"})
        else:
            context.update({"Error": "دسته بندی یافت نشد"})
    context.update({"Category": Category.objects.all()})
    return render(request, "list-category.html", context)


@csrf_exempt
def ajax_delete_category(request):
    context = {}

    id = request.session["member_id"]
    if not id:
        context.update({"Status": "Error"})
        return JsonResponse(context)

    if request.method == "POST":
        category_id = request.POST.get("id")
        if category_id:
            c = Category.objects.get(id=category_id)
            c.delete()
            context.update({"Status": "Success"})
        else:
            context.update({"Status": "Error"})
    else:
        context.update({"Status": "Error"})

    return JsonResponse(context)


def add_member(request):
    id = request.session["member_id"]
    if not id:
        return HttpResponseRedirect("/panel/login/")
    context = {}
    context.update({"Member": Member.objects.get(id=id)})

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile = request.FILES.get("profile")
        if name and phone and email and password and profile:
            m = Member(name=name, phone=phone, email=email, profile=profile,
                       password=password_hasher(password))
            m.save()
            context.update({"Success": "با موفقیت ثبت شد!"})

        else:
            context.update({"Error": "لطفا همه ی فیلد ها را وارد کنید!"})
    return render(request, "add-member.html", context)


def list_member(request):
    id = request.session["member_id"]
    if not id:
        return HttpResponseRedirect("/panel/login/")
    context = {}
    context.update({"Member": Member.objects.get(id=id)})
    if request.method == "POST":
        member_id = request.POST.get("id")
        if member_id:
            m = Member.objects.get(id=member_id)
            m.delete()
            context.update({"Success": "باموفقیت حذف شد!"})
        else:
            context.update({"Error": "دسته بندی یافت نشد"})
    context.update({"Members": Member.objects.all()})
    return render(request, "list-members.html", context)


def add_news(request):
    id = request.session["member_id"]
    if not id:
        return HttpResponseRedirect("/panel/login/")
    context = {}
    context.update({"Member": Member.objects.get(id=id)})
    if request.method == "POST":
        title = request.POST.get("title")
        categ = request.POST.get("category")
        text = request.POST.get("news")
        if title and categ and text:
            n = News(title=title, text=text, category=Category.objects.get(id=categ), admin=Member.objects.get(id=id))
            n.save()
            context.update({"Success": "خبر با موفقیت درج شد!"})
        else:
            context.update({"Error": "همه مقادیر را بدرستی وارد کنید!"})

    context.update({"Title": "درج خبر"})
    context.update({"Category": Category.objects.all()})
    return render(request, "add-news.html", context)


def list_news(request):
    id = request.session["member_id"]
    if not id:
        return HttpResponseRedirect("/panel/login/")
    context = {}
    context.update({"Member": Member.objects.get(id=id)})
    context.update({"News": News.objects.all()})
    return render(request, "list-news.html", context)


def edit_news(request, news_id):
    id = request.session["member_id"]
    if not id:
        return HttpResponseRedirect("/panel/login/")
    context = {}
    context.update({"Member": Member.objects.get(id=id)})
    if request.method == "POST":
        title = request.POST.get("title")
        categ = request.POST.get("category")
        text = request.POST.get("news")
        if title and categ and text:
            n = News.objects.get(id=news_id)
            n.title = title
            n.text = text
            n.category = Category.objects.get(id=categ)
            n.save()
            context.update({"Success": "خبر با موفقیت درج شد!"})
        else:
            context.update({"Error": "همه مقادیر را بدرستی وارد کنید!"})

    context.update({"News": News.objects.get(id=news_id)})

    context.update({"Title": "ویرایش خبر"})
    context.update({"Category": Category.objects.all()})
    return render(request, "edit-news.html", context)
