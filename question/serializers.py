from rest_framework import serializers
from .models import QuestionIntegral, StageIntegral, QuestionDerivative,StageDerivative

class QuestionIntegralFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionIntegral
        fields = ['question_latex']


class QuestionDerivativeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionDerivative
        fields = ['question_latex']

####################################################################

class StageIntegralSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageIntegral
        fields = [
            'stage_number', 
            'option1_title', 'option1_latex', 'option1_descrption',
            'option2_title', 'option2_latex', 'option2_descrption',
            'option3_title', 'option3_latex', 'option3_descrption',
            'option4_title', 'option4_latex', 'option4_descrption',
            'correct_option'
        ]

class StageDerivativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageDerivative
        fields = [
            'stage_number', 
            'option1_title', 'option1_latex', 'option1_descrption',
            'option2_title', 'option2_latex', 'option2_descrption',
            'option3_title', 'option3_latex', 'option3_descrption',
            'option4_title', 'option4_latex', 'option4_descrption',
            'correct_option'
        ]

###############################################################################
class QuestionIntegralSerializer(serializers.ModelSerializer):
    stages = StageIntegralSerializer(many=True)
    class Meta:
        model = QuestionIntegral
        fields = [
            'id', 'title', 'question_latex', 'description', 
            'stage', 'score', 'difficulty', 'stages'
        ]
    
class QuestionDerivativeSerializer(serializers.ModelSerializer):
    stages = StageDerivativeSerializer(many=True)
    class Meta:
        model = QuestionDerivative
        fields = [
            'id', 'title', 'question_latex', 'description', 
            'stage', 'score', 'difficulty', 'stages'
        ]









####################################################################

class CorectOptionIntegralSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageIntegral
        fields = [
            'correct_option'
        ]
    def to_representation(self, instance):
        #make a list from corecr option
        return int(instance.correct_option) 

class CorectOptionDerivativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageDerivative
        fields = [
            'correct_option'
        ]
    def to_representation(self, instance):
        #make a list from corecr option
        return int(instance.correct_option) 
    
################################################################33


class SelectQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionIntegral
        fields = ['title', 'difficulty', 'score', 'question_latex', 'description']

class SelectQDerivativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionDerivative
        fields = ['title', 'difficulty', 'score', 'question_latex', 'description']
######################################################################################

class AllQuestionSerializer(serializers.ModelSerializer):
    is_solved = serializers.SerializerMethodField()

    class Meta:
        model = QuestionIntegral
        fields = ['id', 'title', 'difficulty', 'question_latex']


class GetAnswerSerializer(serializers.Serializer):
    answer = serializers.IntegerField() 


class UserStatusTableSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name =serializers.CharField()
    id_q =serializers.IntegerField() 