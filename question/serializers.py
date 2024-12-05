from rest_framework import serializers
from . models import Question , Stage, UserSolvedQuestion
from rest_framework import serializers

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['stage_number', 
                  'option1_title', 'option1_image_base64',

                  'option2_title', 'option2_image_base64',

                  'option3_title', 'option3_image_base64',

                  'option4_title', 'option4_image_base64',
                  
                  'correct_option']



class QuestionSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'img_base64', 'stages']






class SelectQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'img_base64', 'difficulty','score','description']






























class AllQuestionSerializer(serializers.ModelSerializer):
    is_solved = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['title', 'img_base64', 'difficulty','is_solved']

    def get_is_solved(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserSolvedQuestion.objects.filter(user=user, question=obj).exists()
        return False 

