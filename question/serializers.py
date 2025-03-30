from rest_framework import serializers
from .models import Question, Stage

class QuestionFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_latex']

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = [
             'stage_number', 
            'option1_title', 'option1_latex', 'option1_descrption',
            'option2_title', 'option2_latex', 'option2_descrption',
            'option3_title', 'option3_latex', 'option3_descrption',
            'option4_title', 'option4_latex', 'option4_descrption',
            'correct_option'
        ]

class QuestionSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'id', 'title', 'question_latex', 'description', 
            'stage', 'score', 'difficulty', 'stages'
        ]
    



class CorectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = [
            'correct_option'
        ]
    def to_representation(self, instance):
        # تبدیل خروجی به یک لیست از مقادیر صحیح
        return int(instance.correct_option) 
    





class SelectQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'difficulty', 'score', 'question_latex', 'description']




class AllQuestionSerializer(serializers.ModelSerializer):
    is_solved = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'difficulty', 'question_latex']
