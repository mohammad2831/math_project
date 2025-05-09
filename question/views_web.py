from django.shortcuts import render
from django.views import View
from .models import QuestionIntegral,QuestionDerivative,StageIntegral,StageDerivative
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StageIntegralSerializer,QuestionIntegralFormSerializer,QuestionIntegralSerializer , StageIntegralSerializer,AllQuestionSerializer, SelectQuestionSerializer,QuestionIntegralFormSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import render, get_object_or_404, redirect





''''''
class AllQuestionView(APIView):
    def get(self, request):
        questions = QuestionIntegral.objects.all()[:20]

        serializer = AllQuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)

class QuestionView(APIView):
    #authentication_classes = [TokenAuthentication] 
    #permission_classes = [IsAuthenticated]
    def get(self, request, id_q, id_s):
        if id_q >=20:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            question = get_object_or_404(QuestionIntegral, id=id_q)
            ser_data = QuestionIntegralSerializer(question)
            stage = StageIntegral.objects.get(question=question, stage_number=id_s)
            start_stage=StageIntegralSerializer(stage)
            return Response({'stage': start_stage.data, 'form':ser_data.data})
        
        




    def post(self, request, id_q, id_s):
        if id_q >=20:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
        # user = User.objects.get(user=request.user)
            question = get_object_or_404(QuestionIntegral, id=id_q)
            ser_data = QuestionIntegralFormSerializer(question)

            stage = StageIntegral.objects.filter(question=question, stage_number=id_s).first()

            if not stage:
                return Response({'error': 'Stage not found'}, status=status.HTTP_404_NOT_FOUND)

            selected_option = request.data.get('option')
            correct_option = str(stage.correct_option)

            if selected_option == correct_option:
                message = "Correct option"
                next_stage = StageIntegral.objects.filter(question=question, stage_number=id_s + 1).first()


                if next_stage:
                    next_stage_serializer = StageIntegralSerializer(next_stage)
                    return Response({'message': message,'stage': next_stage_serializer.data}, status=status.HTTP_200_OK)
                

                else:
                    message = "Finished all stages of this question."
            
                



                    return Response({'message': message}, status=status.HTTP_200_OK)
            
            else:
                message = "Incorrect answer, please try again."
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
            



class SelectQuestionView(APIView):
    def get(self,request, id_q):
        if id_q >=20:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            question = get_object_or_404(QuestionIntegral, id=id_q)


            ser_data = SelectQuestionSerializer(question)
            return Response(ser_data.data)
















