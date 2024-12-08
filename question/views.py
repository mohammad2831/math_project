from django.shortcuts import render
from django.views import View
from .models import Question,Stage, UserScore,UserSolvedQuestion
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer , StageSerializer,AllQuestionSerializer, SelectQuestionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import render, get_object_or_404, redirect


class AllQuestionView(APIView):
    def get(self, request):
        questions = Question.objects.all()

        serializer = AllQuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)

class QuestionView(APIView):
    #authentication_classes = [TokenAuthentication] 
    #permission_classes = [IsAuthenticated]
    def get(self, request, id_q, id_s):
        question = get_object_or_404(Question, id=id_q)
        stage = Stage.objects.get(question=question, stage_number=1)
        start_stage=StageSerializer(stage)
        return Response({'stage': start_stage.data})






    def post(self, request, id_q, id_s):
       # user = User.objects.get(user=request.user)
        question = get_object_or_404(Question, id=id_q)
        stage = Stage.objects.filter(question=question, stage_number=id_s).first()

        if not stage:
            return Response({'error': 'Stage not found'}, status=status.HTTP_404_NOT_FOUND)

        selected_option = request.data.get('option')
        correct_option = str(stage.correct_option)

        if selected_option == correct_option:
            message = "Correct option"
            next_stage = Stage.objects.filter(question=question, stage_number=id_s + 1).first()


            if next_stage:
                next_stage_serializer = StageSerializer(next_stage)
                return Response({'message': message,'stage': next_stage_serializer.data}, status=status.HTTP_200_OK)
            

            else:
                message = "Finished all stages of this question."
          
               # question.solved_count += 1
               # question.save()

               # user_solved_question, created = UserSolvedQuestion.objects.get_or_create(
              #  user=user, 
               # question=question
               # )


               # user_solved_question.solve = True
               # user_solved_question.save()

               # user_score, created = UserScore.objects.get_or_create(
              #  user=user, 
               # question=question
               # )

  
                #user_score.score += question.score if question.score else 0
                #user_score.save()




                return Response({'message': message}, status=status.HTTP_200_OK)
        
        else:
            message = "Incorrect answer, please try again."
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        

'''
    def get(self, request, id_q, id_s):
        question = get_object_or_404(Question, id=id_q)
        stage = Stage.objects.filter(question=question, stage_number=id_s).first()

        if not stage:
            return Response({'error': 'Stage not found'}, status=status.HTTP_404_NOT_FOUND)

        question_serializer = QuestionSerializer(question)
        stage_serializer = StageSerializer(stage)

        return Response({
            'question': question_serializer.data,
            'stage': stage_serializer.data,
        })
    '''

class SelectQuestionView(APIView):
    def get(self,request, id_q):
        question = get_object_or_404(Question, id=id_q)


        ser_data = SelectQuestionSerializer(question)
        return Response(ser_data.data)























'''
class QuestionView(View):
    def get(self, request, id_q, id_s):
        question = get_object_or_404(Question, id=id_q)
        stage = Stage.objects.filter(question=question, stage_number=id_s).first()

        return render(request, 'question/question.html', {
            'question': question,
            'stage': stage,
        })

    def post(self, request, id_q, id_s):
        question = get_object_or_404(Question, id=id_q)
        stage = Stage.objects.filter(question=question, stage_number=id_s).first()



        selected_option = request.POST.get('option')
        correct_option = str(stage.correct_option)
        
        if selected_option == correct_option:
            
            message = "correct option"
            next_stage = Stage.objects.filter(question=question, stage_number=id_s + 1).first()
            
            if next_stage:
                return redirect('question:question_view', id_q=id_q, id_s=next_stage.stage_number)
            else:
                message = " finish the all stage og this question."
        
        else:
            message = "incorrect answer ridi dadash try again."
        
        return render(request, 'question/question.html', {
            'question': question,
            'stage': stage,
            'message': message
        })

'''
        