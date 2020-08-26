from blog.models import Answer, Question
from django.contrib import admin

# Register your models here.

# class QuestionAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("question",)}

admin.site.register(Question)
admin.site.register(Answer)
