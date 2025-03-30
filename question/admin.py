from django import forms
from django.contrib import admin
from .models import Question, Stage, Roadmap, UserProgress,Category
from .forms import StageAdminForms





'''
class StageInlineForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = [
            'option1_title',  
    
            'option2_title',
        
            'correct_option'
        ]  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
     

class StageInline(admin.StackedInline):
    model = Stage
    form = StageInlineForm
    extra = 1
    fields = [
              'stage_number',

              'option1_title',
              'option1_latex',
              'option1_descrption',

              'option2_title',
              'option2_latex',
              'option2_descrption',

              'option3_title',
              'option3_latex',
              'option3_descrption',

              'option4_title',
              'option4_latex',
              'option4_descrption',

              'correct_option'] 
  
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(stage_number__gt=1)

class QuestionAdmin(admin.ModelAdmin):
    inlines = [StageInline]
    form = StageAdminForms
'''

class StageInline(admin.StackedInline):  # یا admin.StackedInline برای نمایش ستونی
    model = Stage
    extra = 1 


class QuestionAdmin(admin.ModelAdmin):
    model= Question
    fields=[
        'title',
        'question_latex',
        'description',
        'stage',
        'score',
        'difficulty',
                
    ]
    inlines = [StageInline]




#form in admin pannel for stage setting
class StageAdmin(admin.ModelAdmin):
    model= Stage

    fields = [
              'stage_number',

              'option1_latex',
              'option1_descrption',

              'option2_latex',
              'option2_descrption',

              'option3_latex',
              'option3_descrption',

              'option4_latex',
              'option4_descrption',

              'correct_option'] 



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('category_name',)

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'question', 'order')  # نمایش فیلدها در لیست
    list_filter = (('category', admin.RelatedOnlyFieldListFilter),) # امکان فیلتر بر اساس دسته‌بندی
    search_fields = ('name', 'question__title')  # امکان جستجو در نام و سوال

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'last_question', 'score')  # نمایش فیلدهای اصلی
    list_filter = ('category', 'user')  # امکان فیلتر بر اساس کاربر و دسته‌بندی
    search_fields = ('user__email', 'category__category_name')  # جستجو بر اساس ایمیل کاربر و نام دسته‌بندی
   
admin.site.register(Question,QuestionAdmin)
admin.site.register(Stage,StageAdmin)
