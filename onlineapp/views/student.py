from django.views import View
from django.urls import resolve
from onlineapp.form.students import *
from django.shortcuts import render,redirect
from onlineapp.models import *
from django.contrib.auth.mixins import PermissionRequiredMixin

class AddStudentView(PermissionRequiredMixin,View):
    permission_required = ('onlineapp.add_student', 'onlineapp.edit_student', 'onlineapp.delete_student')
    def get(self,request,*args,**kwargs):
        if resolve(request.path_info).url_name == 'addstudent':
            stdform = Studentform()
            mockform = Mockform()
            return render(
                request,
                template_name='student_form.html',
                context={
                    'stdform': stdform,
                    'mockform': mockform,
                    'user_permissions': request.user.get_all_permissions(),
                }
            )
        elif resolve(request.path_info).url_name == 'editstudent':
            std = Student.objects.get(id=kwargs.get('student_id'))
            mock=MockTest1.objects.get(student=std)
            stdform = Studentform(instance=std)
            mockform = Mockform(instance=mock)
            return render(
                request,
                template_name='student_form.html',
                context={
                    'stdform': stdform,
                    'mockform': mockform,
                    'user_permissions': request.user.get_all_permissions(),
                }
            )
        else:
            Student.objects.get(id=kwargs.get('student_id')).delete()
            return redirect('/colleges/' + str(kwargs.get('college_id')) + '/')

    def post(self,request,*args,**kwargs):
        if resolve(request.path_info).url_name=='editstudent':
            std = Student.objects.get(id=kwargs.get('student_id'))
            mock=MockTest1.objects.get(student=std)
            stdform = Studentform(request.POST,instance=std)
            mockform = Mockform(request.POST,instance=mock)
        else:
            stdform = Studentform(request.POST)
            mockform = Mockform(request.POST)
        if stdform.is_valid():
            s = stdform.save(commit=False)
            if resolve(request.path_info).url_name != 'editstudent':
                s.college = College.objects.get(id=kwargs['college_id'])
            s.save()
            m = mockform.save(commit=False)
            m.total = m.problem1 + m.problem2 + m.problem3 + m.problem4
            m.student = s
            m.save()
        return redirect('/colleges/' + str(kwargs.get('college_id')) + '/')