from django.shortcuts import render, redirect, reverse, HttpResponse
from crm import models
from crm.froms import PaymentRecordForm
from utils.pagination import Pagination
from django.views import View
from django.db.models import Q


# PaymentRecordList
class PaymentRecordList(View):
    def get(self, request, *args, **kwargs):

        q = self.search([])
        all_paymentrecord = models.PaymentRecord.objects.filter(q, customer__in=request.user_obj.customers.all())
        # all_paymentrecord = models.PaymentRecord.objects.all()
        page = Pagination(request.GET.get('page', 1), all_paymentrecord.count(), request.GET.copy(), 2)

        return render(request, 'consultant/paymentrecord_list.html', {
            'all_paymentrecord': all_paymentrecord[page.start:page.end],
            'page_html': page.page_html
        })

    def post(self,request,*args,**kwargs):

        action = request.POST.get('action')

        if hasattr(self,action):
            func = getattr(self,action)
            func()
        else:
            return HttpResponse('非法操作')

        return self.get(request,*args,**kwargs)

    def search(self,field_list):
        query = self.request.GET.get('query','')

        q = Q()
        q.connector = "OR"

        for field in field_list:
            if field == 'sex':
                if query == '男':
                    sex = 'male'
                elif query == '女':
                    sex = 'female'
                else:
                    sex = ''
                q.children.append(Q(sex=sex))

            q.children.append(Q(('{}__contains'.format(field),query)))

        return q

def paymentrecord_change(request, customer_id=None, paymentrecord_id=None):

    obj = models.PaymentRecord(customer_id=customer_id) if customer_id else models.PaymentRecord.objects.filter(
        pk=paymentrecord_id).first()
    title = '新增缴费' if customer_id else '编辑缴费'
    form_obj = PaymentRecordForm(instance=obj)
    if request.method == 'POST':

        form_obj = PaymentRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            return redirect(next)

    return render(request, 'form.html', {'form_obj': form_obj, "title": title})
