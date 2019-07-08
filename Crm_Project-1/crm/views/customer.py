from django.shortcuts import render, redirect, reverse, HttpResponse
from crm import models
from crm.froms import CustomerForm
from utils.pagination import Pagination
from django.conf import settings
from django.db import transaction
#展示客户列表
def customer_list(request):
    if request.path_info == reverse('customer_list'):

        all_customer = models.Customer.objects.filter(consultant__isnull=True)
    else:
        all_customer = models.Customer.objects.filter(consultant=request.user_obj)

    page = Pagination(request.GET.get('page', 1), all_customer.count(), )

    return render(request, 'consultant/customer_list.html', {
        'all_customer': all_customer[page.start:page.end],
        'page_html': page.page_html
    })


from django.views import View
from django.db.models import Q
from django.http.request import QueryDict
#展示客户列表 CBV
class CustomerList(View):
    def get(self, request, *args, **kwargs):
        q = self.search(['qq','name',])
        if request.path_info == reverse('customer_list'):

            all_customer = models.Customer.objects.filter(q,consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q,consultant=request.user_obj)

        page = Pagination(request.GET.get('page', 1), all_customer.count(),request.GET.copy(),4)

        return render(request, 'consultant/customer_list.html', {
            'all_customer': all_customer[page.start:page.end],
            'page_html': page.page_html
        })
    def post(self,request,*args,**kwargs):
        action = request.POST.get('action')
        if hasattr(self,action):
            func = getattr(self,action)
            response = func()
            if response:
                return response
        else:
            return HttpResponse("非法")
        return self.get(request,*args,**kwargs)

    def multi_apply(self):
        ids = self.request.POST.getlist('ids')

        #把提交的客户的ID都变成当前用户的私户
        #原来的用户量 + 要申请的数量
        if self.request.user_obj.customers.all().count() + len(ids) > settings.MAX_CUSTOMER_NUM:
            return HttpResponse('贪心不足蛇吞象!!!')


        with transaction.atomic():
            queryset = models.Customer.objects.filter(pk__in=ids,consultant__isnull=True).select_for_update()

            if len(ids) == queryset.count():
                queryset.update(consultant = self.request.user_obj)
            else:
                return HttpResponse('手速太慢,别被人搞走了')

        # models.Customer.objects.filter(pk__in=ids).update(consultant=self.request.user_obj)


    def multi_pub(self):
        ids = self.request.POST.getlist('ids')

        models.Customer.objects.filter(pk__in=ids).update(consultant=None)


    def search(self,field_list):
        query = self.request.GET.get('query','')
        q = Q()
        q.connector = "OR"

        for field in field_list:
            if field == "sex":
                if query == '男':
                    sex = 'male'
                elif query == '女':
                    sex = 'female'
                else:
                    sex = ''
                q.children.append(Q(sex=sex))
            q.children.append(Q(('{}__contains'.format(field),query)))
        return q

#添加用户
def customer_add(request):
    form_obj = CustomerForm()
    if request.method=="POST":
        form_obj = CustomerForm(request.POST)

        if form_obj.is_valid():
            form_obj.save()

            return redirect(reverse('customer_list'))
    return render(request, 'consultant/customer_add.html', {'form_obj':form_obj})

def customer_edit(request, edit_id):
    obj = models.Customer.objects.filter(pk=edit_id).first()

    # 处理POST
    if request.method == 'POST':
        # 包含提交的数据 原始数据
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()  # 保存修改
            # 跳转到展示页面
            return redirect(reverse('customer_list'))
    else:
        # 包含原始数据的form表单
        form_obj = CustomerForm(instance=obj)

    return render(request, 'consultant/customer_edit.html', {'form_obj': form_obj})


def customer_change(request,edit_id = None):
    obj = models.Customer.objects.filter(pk=edit_id).first()

    if request.method == "POST":
        form_obj = CustomerForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            # print(next)
            return redirect(next)
    else:
        form_obj = CustomerForm(instance=obj)

    title = "编辑客户" if edit_id else "添加客户"

    return render(request, 'consultant/customer_change.html', {'title':title, 'form_obj':form_obj})
