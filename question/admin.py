from django import forms
from django.contrib import admin
from .models import Question, Stage
from .forms import StageAdminForms

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
      #  if self.instance and self.instance.pk:
       #     self.fields['question'].queryset = Question.objects.filter(id=self.instance.question.id)




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


class StageAdmin(admin.ModelAdmin):
    model= Stage

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


admin.site.register(Question,QuestionAdmin)
admin.site.register(Stage,StageAdmin)
