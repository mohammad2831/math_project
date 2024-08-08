from django.shortcuts import render
from django.views import View
from .models import QuestionIntegral,QuestionDerivative,StageIntegral,StageDerivative
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GetAnswerSerializer,CorectOptionIntegralSerializer,StageIntegralSerializer,QuestionIntegralFormSerializer,QuestionIntegralSerializer , StageIntegralSerializer,AllQuestionSerializer, SelectQuestionSerializer,QuestionIntegralFormSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core.cache import cache
import json

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
    def get(self, request, id_q):
        #first make and save user status table after save question
        if id_q >=20:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        
        else :
        # use for make corect option list and send question for flutter  
            return self.add_question_to_redis(id_q)


    #fetch question from sql and add it in redis
    #with gzip format send it to flutter and set it in gzip_middleware.py file
    def add_question_to_redis(self, id_q):

        cache_key_question = f"question_integral:{id_q}"

        #check if question is in redis
        cached_data = cache.get(cache_key_question)
        if cached_data:
            print("Question found in cache!")
            return Response(json.loads(cached_data))

        try:
            print("Fetching question from DB (SQL)")
            #fetch quseton from sql
            question = QuestionIntegral.objects.prefetch_related('stages').get(id=id_q)
            
            #serialize question and all stages
            serialized_data = QuestionIntegralSerializer(question).data

            #serialize all stages and get a list just with corect option any stage
            serialized_correct_option = CorectOptionIntegralSerializer(question.stages, many=True).data

            #save question in redis            
            cache.set(cache_key_question, json.dumps(serialized_data), timeout=400)

            #save corect option in redis
            cache.set(f"correct_option_integral:{id_q}", json.dumps(serialized_correct_option), timeout=400)

            print("Question added to Redis.")
            return Response(serialized_data)

        except QuestionIntegral.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)




class QuestionView(APIView):

    #show queston
    def get(self, request, id_q, id_s):
        #check cashe key from redis
        question_cache_key = f"question_integral{id_q}" 
        cached_question_data = cache.get(question_cache_key)
        
        if cached_question_data:
            ser_data = cached_question_data

        #if cache is not exist then fetch from sql
        #and set it in redis
        else:
            question = get_object_or_404(QuestionIntegral, id=id_q)
            ser_data = QuestionIntegralFormSerializer(question).data
            ser_data_json = json.dumps(ser_data)
            cache.set(question_cache_key, ser_data_json, timeout=1200) 

           
            stages = StageIntegral.objects.filter(question_id=id_q).order_by('stage_number')
            stages_data = StageIntegralSerializer(stages, many=True).data
            stages_cache_key = f"stages_integral_{id_q}"
            cache.set(stages_cache_key, stages_data, timeout=1200)  
        
      
        stage_cache_key = f"stage_integral_{id_q}_{id_s}" 
        cached_stage_data = cache.get(stage_cache_key)

        if cached_stage_data:
            stage_data = cached_stage_data
        else:
            stage = StageIntegral.objects.get(question_id=id_q, stage_number=id_s)
            stage_data = StageIntegralSerializer(stage).data
            cache.set(stage_cache_key, stage_data, timeout=1200) 
        
        return Response({'stage': stage_data, 'form': ser_data})



    #check if answer is correct or not
    #and add it in user status table
    #key in redis is :1:user_status:user-id:question-is
    #and add it in progress list
    def post(self, request, id_q, id_s):
      
        # answer user send it    
        answer = GetAnswerSerializer(data=request.data)
        if answer.is_valid():

            #fetch correct option list in redis with question id
            cache_key_correct_option = f"correct_option_integral:{id_q}"
            cached_data_correct_option = cache.get(cache_key_correct_option)

        
            
          
            if cached_data_correct_option:
                try:
                    cached_data_correct_option_load = json.loads(cached_data_correct_option)
                    
                    if 0 <= id_s - 1 < len(cached_data_correct_option_load):

                        if cached_data_correct_option_load[id_s - 1] == answer.validated_data['answer']:

                            if id_s == len(cached_data_correct_option_load):
                                return Response({"message": "final-corect"}, status=201)

                            return Response({"message": "correct"}, status=200)

                        else:
                            return Response({"message": "incorrect"}, status=200)

                    else:
                        return Response({"error": "Question index out of range"}, status=400)

                except json.JSONDecodeError:
                    return Response({"error": "Unable to decode cached data"}, status=400)
            else:
                return Response({"error": "Problem in correct option"}, status=409)   
 
            

  
    







