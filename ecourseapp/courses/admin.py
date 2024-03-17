from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe

from .models import Category, Course, Lesson, Tag
from django.contrib.auth.models import Permission


class EcourseAppAdminSite(admin.AdminSite):
    site_header = 'HỆ THỐNG KHÓA HỌC TRỰC TUYẾN'

    def get_urls(self):
        return [path('course-stats/', self.stats_view)] + super().get_urls()

    def stats_view(self, request):
        course_count = Course.objects.filter(active=True).count()
        course_stats = Course.objects.annotate(lesson_count=Count('lesson__id')).values('id', 'name', 'lesson_count')
        return TemplateResponse(request, 'admin/course_stats.html', {
            'course_count': course_count,
            'course_stats': course_stats
        })


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['id', 'name']
    search_fields = ['name']


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class CourseTagInlineAdmin(admin.TabularInline):
    model = Course.tags.through


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_filter = ['id', 'name']
    search_fields = ['name']
    readonly_fields = ['img']
    form = CourseForm
    inlines = [CourseTagInlineAdmin]

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }

    @staticmethod
    def img(obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />'.format(url=obj.image.name)
            )


class LessonForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_filter = ['id', 'name']
    search_fields = ['name']
    readonly_fields = ['img']
    form = LessonForm

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }

    @staticmethod
    def img(obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />'.format(url=obj.image.name)
            )


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['id', 'name']
    search_fields = ['name']


admin_site = EcourseAppAdminSite(name='myapp')

# Register your models here.
admin_site.register(Category, CategoryAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(Permission)
