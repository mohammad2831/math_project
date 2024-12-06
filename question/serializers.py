from rest_framework import serializers
from . models import Question , Stage, UserSolvedQuestion
from rest_framework import serializers

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['stage_number', 
                  'option1_title', 

                  'option2_title', 

                  'option3_title', 

                  'option4_title', 
                  
                  'correct_option']



class QuestionSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'stages']






class SelectQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'difficulty','score','description']




class AllQuestionSerializer(serializers.ModelSerializer):
    is_solved = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id','title', 'difficulty','is_solved']

    def get_is_solved(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserSolvedQuestion.objects.filter(user=user, question=obj).exists()
        return False 

