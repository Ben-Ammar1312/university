from django.contrib import admin
from .models import Classes,Subject,Teacher,Student,Student_Subject,User
    
admin.site.register(Classes)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Student_Subject)
admin.site.register(User)

