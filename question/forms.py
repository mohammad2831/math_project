from django import forms
from . models import Question, Stage

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'title',
            'question_latex'
            ]

    def clean_profile_picture(self):
        profile_picture = self.files.get('profile_picture')
        if profile_picture:
            import base64
            from io import BytesIO
            from PIL import Image

            image = Image.open(profile_picture)
            buffered = BytesIO()
            image.save(buffered, format=image.format)
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return img_base64
        return None


class StageAdminForms(forms.ModelForm):
    model = Stage
    fields = [
            'option1_title',  
            'option1_latex',

            'option2_title',
            'option2_latex',
                  
            'option3_title',
            'option3_latex',
                  
            'option4_title',
            'option4_latex'
            ]
