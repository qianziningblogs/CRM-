from django.shortcuts import render, redirect, reverse, HttpResponse
from crm import models
from crm.froms import ClassListForm,CourseRecordForm,StudyRecordForm
from utils.pagination import Pagination
from django.views import View
from django.db.models import Q

class ClassList(View):
    def get(self, request, *args, **kwargs):

        q = self.search([])

        all_classlist = models.ClassList.objects.filter(q,)
        page = Pagination(request.GET.get('page', 1), all_classlist.count(), request.GET.copy(), 2)

        return render(request, 'teacher/classlist_list.html', {
            'all_classlist': all_classlist[page.start:page.end],
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

def classlist_change(request, customer_id=None, classlist_id=None):

    obj = models.ClassList(customer_id=customer_id) if customer_id else models.ClassList.objects.filter(
        pk=classlist_id).first()
    title = '新增缴费' if customer_id else '编辑缴费'
    form_obj = ClassListForm(instance=obj)
    if request.method == 'POST':

        form_obj = ClassListForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            return redirect(next)

    return render(request, 'form.html', {'form_obj': form_obj, "title": title})
class CourseRecordList(View):
    def get(self,request,class_id,*args,**kwargs):

        q = self.search([])
        all_course_record = models.CourseRecord.objects.filter(q,re_class_id  =class_id)

        page = Pagination(request.GET.get('page',1),all_course_record.count(),request.GET.copy(),10)

        return render(request,'teacher/course_record_list.html',{
            'class_id':class_id,
            'all_course_record':all_course_record[page.start:page.end],
            'page_html':page.page_html

        })
    def post(self,request,*args,**kwargs):
        action = request.POST.get('action')

        if hasattr(self,action):
            func = getattr(self,action)
            response = func()
            if response:
                return response
        else:
            return HttpResponse('非法操作')

        return self.get(request,*args,**kwargs)

    def search(self,field_list):
        query = self.request.GET.get('query','')

        q = Q()
        q.connector = 'OR'
        for field in field_list:

            q.children.append(Q(('{}'.format(field),query)))

        return q


    def multi_init(self):
        course_record_ids = self.request.POST.getlist('ids')

        for course_record_id in course_record_ids:
            #给一个课程记录下所有学生添加学习记录
            #拿到所有学生
            course_record_obj = models.CourseRecord.objects.filter(pk=course_record_id).first()
            all_students = course_record_obj.re_class.customer_set.all().filter(status='studying')

            #批量插入
            study_record_list = []
            for student in all_students:
                if models.StudyRecord.objects.filter(student=student,course_record_id=course_record_id).exists():
                    continue

                obj = models.StudyRecord(student=student,course_record_id=course_record_id)
                study_record_list.append(obj)
            models.StudyRecord.objects.bulk_create(study_record_list)

def course_record_change(request,class_id=None,course_record_id=None):
    obj = models.CourseRecord(re_class_id = class_id,
                               teacher = request.user_obj) if class_id else models.CourseRecord.objects.filter(
        pk=course_record_id).first()

    form_obj = CourseRecordForm(instance=obj)

    if request.method == "POST":

        form_obj = CourseRecordForm(request.POST,instance = obj)
        if form_obj.is_valid():
            form_obj.save()

            next = request.GET.get('next')
            if not next:
                next = reverse('course_record_list',class_id)
            return redirect(next)

    title = '新增课程记录' if class_id else '编辑课程记录'

    return render(request,'form.html',{'form_obj':form_obj,'title':title})

from django.forms import modelformset_factory

def study_record_list(request,course_record_id):
    FormSet = modelformset_factory(models.StudyRecord,StudyRecordForm,extra=0)

    formset = FormSet(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id))

    if request.method == 'POST':
        formset = FormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('study_record_list',args=(course_record_id)))

    return render(request,'teacher/study_record_list.html',{'formset':formset})

