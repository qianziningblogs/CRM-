from django.conf.urls import url
# from crm import views
from crm.views import auth,customer,consult,enrollment,paymentrecord,teacher
urlpatterns = [
    url(r'^login/$',auth.login,name='login'),
    url(r'^reg/$',auth.reg,name='reg'),
    url(r'^index/$',auth.index,name='index'),

    url(r'customer_list/$',customer.CustomerList.as_view(),name='customer_list'),
    url(r'my_customer/$',customer.CustomerList.as_view(),name='my_customer'),
    url(r'customer_add/$', customer.customer_change, name='customer_add'),
    url(r'customer_edit/(\d+)/$', customer.customer_change, name='customer_edit'),


    # 展示跟进 ConsultRecord
    url(r'^consult_list/$', consult.ConsultList.as_view(), name='consult_list'),
    # 展示某个客户的跟进
    url(r'^consult_list/(?P<customer_id>\d+)/$', consult.ConsultList.as_view(), name='one_consult_list'),
    # 添加跟进
    url(r'^consult_add/$', consult.consult_add, name='consult_add'),
    # 编辑跟进
    url(r'^consult_edit/(\d+)/$', consult.consult_edit, name='consult_edit'),


    #展示报名表
    url(r'^enrollment_list/$', enrollment.EnrollmentList.as_view(), name='enrollment_list'),
   # 添加报名表
    url(r'^enrollment_add/(?P<customer_id>\d+)/$', enrollment.enrollment_change, name='enrollment_add'),
    # 编辑报名表
    url(r'^enrollment_edit/(?P<enrollment_id>\d+)/$', enrollment.enrollment_change, name='enrollment_edit'),


    #缴费表PaymentRecord
    url(r'^paymentrecord_list/$', paymentrecord.PaymentRecordList.as_view(), name='paymentrecord_list'),
    # 添加报名表
    url(r'^paymentrecord_add/(?P<customer_id>\d+)/$', paymentrecord.paymentrecord_change, name='paymentrecord_add'),
    # 编辑报名表
    url(r'^paymentrecord_edit/(?P<paymentrecord_id>\d+)/$', paymentrecord.paymentrecord_change, name='paymentrecord_edit'),



    #班级表ClassList
    url(r'^classlist_list/$', teacher.ClassList.as_view(), name='classlist_list'),
    # 添加报名表
    url(r'^classlist_add/$', teacher.classlist_change, name='classlist_add'),
    # 编辑报名表
    url(r'^classlist_edit/(?P<classlist_id>\d+)/$', teacher.classlist_change,
        name='classlist_edit'),

    #展示课程记录CourseRecord
    url(r'^course_record_list/(?P<class_id>\d+)$', teacher.CourseRecordList.as_view(), name='course_record_list'),
    url(r'^course_record_add/(?P<class_id>\d+)$', teacher.course_record_change, name='course_record_add'),
    url(r'^course_record_edit/(?P<course_record_id>\d+)$', teacher.course_record_change, name='course_record_edit'),

    #展示学习记录
    url(r'^study_record_list/(?P<course_record_id>\d+)$', teacher.study_record_list, name='study_record_list'),

]
