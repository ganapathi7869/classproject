from django.views import View
from onlineapp.models import *
from django.shortcuts import render,redirect
from onlineapp.form.colleges import *
from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

class CollegeView(LoginRequiredMixin,PermissionRequiredMixin,View):
    login_url = '/login/'
    permission_required = ('onlineapp.add_college','onlineapp.edit_college','onlineapp.delete_college')
    def get(self,request,*args,**kwargs):
        if kwargs:
            college = College.objects.get(**kwargs)
            students = list(college.student_set.order_by("-mocktest1__total"))
            #student = Student.objects.filter(**kwargs)
            #colleges = College.objects.all()
            return render(
                request,
                #template_name="colleges.html",
                template_name="college_details.html",
                context= {
                    'college':college,
                    'students':students,
                    'title' : 'Student from {} | Mentor App'.format(college.name)
                }
            )
        else:
            colleges = College.objects.all()
            return render(
                request,
                template_name="colleges.html",
                context= {
                    'colleges': colleges
                }
            )

class AddCollegeView(PermissionRequiredMixin,View):
    permission_required = ('onlineapp.add_student', 'onlineapp.edit_student', 'onlineapp.delete_student')
    def get(self,request,*args,**kwargs):
        form = AddCollege()

        if kwargs:
            if resolve(request.path_info).url_name == "deleteCollege":
                College.objects.get(pk=kwargs.get('pk')).delete()
                return redirect('/colleges/')
            college = College.objects.get(**kwargs)
            form = AddCollege(instance=college)

        return render(
            request,
            template_name="addCollege.html",
            context={
                'form': form,
            }
        )
    def post(self,request,*args,**kwargs):

        if resolve(request.path_info).url_name == "deleteCollege":
            College.objects.get(pk=kwargs.get('pk')).delete()
            return redirect('/colleges/')

        if resolve(request.path_info).url_name == "editCollege":
            college = College.objects.get(pk=kwargs.get('pk'))
            form = AddCollege(request.POST,instance=college)

            if form.is_valid():
                form.save()
                return redirect('/colleges/')
        else:

            form = AddCollege(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/colleges/')
            return render(
                request,
                template_name="addCollege.html",
                context={
                    'form': form,
                }
            )



