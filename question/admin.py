from django import forms
from django.contrib import admin
from .models import QuestionIntegral, StageIntegral, UserProgress,Category, QuestionDerivative,StageDerivative
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

class StageIntegralInline(admin.StackedInline):  
    model = StageIntegral
    extra = 1 

class StageDerivativeInline(admin.StackedInline):  
    model = StageDerivative
    extra = 1 
class QuestionIntegralAdmin(admin.ModelAdmin):
    model= QuestionIntegral
    fields=[
        'title',
        'question_latex',
        'description',
        'stage',
        'score',
        'difficulty',
                
    ]
    inlines = [StageIntegralInline]

class QuestionDeivativeAdmin(admin.ModelAdmin):
    model= QuestionDerivative
    fields=[
        'title',
        'question_latex',
        'description',
        'stage',
        'score',
        'difficulty',
                
    ]
    inlines = [StageDerivativeInline]


#form in admin pannel for stage setting
class StageIntegralAdmin(admin.ModelAdmin):
    model= StageIntegral

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

class StageDerivativeAdmin(admin.ModelAdmin):
    model= StageDerivative

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


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_question_derivative', 'last_question_integral', 'score')  # نمایش فیلدهای اصلی
    list_filter = ('score', 'user')  # امکان فیلتر بر اساس کاربر و دسته‌بندی
    search_fields = ('user__email', 'category__category_name')  # جستجو بر اساس ایمیل کاربر و نام دسته‌بندی
   
admin.site.register(QuestionIntegral,QuestionIntegralAdmin)
admin.site.register(QuestionDerivative,QuestionDeivativeAdmin)


admin.site.register(StageIntegral,StageIntegralAdmin)
admin.site.register(StageDerivative,StageDerivativeAdmin)

