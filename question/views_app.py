from django.views import View
from .models import Question,Stage
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer , StageSerializer,AllQuestionSerializer, SelectQuestionSerializer,QuestionFormSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core.cache import cache
import json


from django.shortcuts import render, get_object_or_404, redirect


class test(APIView):
    pass

class AllQuestionView(APIView):

    def get(self, request):
        questions = Question.objects.all()

        serializer = AllQuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)


class QuestionView(APIView):
    #authentication_classes = [TokenAuthentication] 
    #permission_classes = [IsAuthenticated]
    def get(self, request, id_q, id_s):
        question_cache_key = f"question_{id_q}" 
        cached_question_data = cache.get(question_cache_key)
        
        if cached_question_data:
            ser_data = cached_question_data
        else:
            question = get_object_or_404(Question, id=id_q)
            ser_data = QuestionFormSerializer(question).data
            ser_data_json = json.dumps(ser_data)
            cache.set(question_cache_key, ser_data_json, timeout=1200)  # ذخیره داده‌های سؤال در کش

            # ذخیره تمامی مراحل مربوط به این سؤال
            stages = Stage.objects.filter(question_id=id_q).order_by('stage_number')
            stages_data = StageSerializer(stages, many=True).data
            stages_cache_key = f"stages_{id_q}"
            cache.set(stages_cache_key, stages_data, timeout=1200)  # ذخیره تمامی مراحل در کش
        
        # کلید کش برای داده‌های مرحله خاص
        stage_cache_key = f"stage_{id_q}_{id_s}" 
        cached_stage_data = cache.get(stage_cache_key)

        if cached_stage_data:
            stage_data = cached_stage_data
        else:
            stage = Stage.objects.get(question_id=id_q, stage_number=id_s)
            stage_data = StageSerializer(stage).data
            cache.set(stage_cache_key, stage_data, timeout=1200)  # ذخیره داده‌های مرحله خاص در کش
        
        return Response({'stage': stage_data, 'form': ser_data})


    '''
    def get(self, request, id_q, id_s):
        cache_key = f"{id_q}" 
        cached_data = cache.get(cache_key)  

        if cached_data:
            ser_data = cached_data

        else:
            question = get_object_or_404(Question, id=id_q)
            ser_data = QuestionFormSerializer(question).data            
            ser_data_json = json.dumps(ser_data)  
            cache.set(cache_key, ser_data_json, timeout=1200)  


        stage = cache.get(cache_key, id_s=1)
        start_stage = StageSerializer(stage).data
        return Response({'stage': start_stage, 'form':ser_data})

    '''

    def post(self, request, id_q, id_s):


        '''
        question = get_object_or_404(Question, id=id_q)
        #add to redis after for all logic use reddis
        ser_data = QuestionFormSerializer(question)
        '''


        
        cache_key = f"question_{id_q}"  # کلید یکتا برای ذخیره در Redis
        cached_data = cache.get(cache_key)  # تلاش برای گرفتن داده از کش

        

        # اگر داده در کش نبود، از دیتابیس بگیر و ذخیره کن
        question = get_object_or_404(Question, id=id_q)
        ser_data = QuestionFormSerializer(question).data
        
        cache.set(cache_key, ser_data, timeout=1200)






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
          
                return Response({'message': message}, status=status.HTTP_200_OK)
        
        else:
            message = "Incorrect answer, please try again."
            #get description of stage and serializer it and send with request
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        
            #add logic score option
            #chalnge for any user calcute the score for any stage
            #add score logic on redis
              


'''
class SelectQuestionView(APIView):
    def get(self,request, id_q):
        cache_key = f"{id_q}" 
        cached_data = cache.get(cache_key)
        
        if cached_data:
            ser_data = cached_data
        else:
            question = get_object_or_404(Question, id=id_q)
            ser_data = SelectQuestionSerializer(question).data
            cache.set(cache_key, ser_data, timeout=1200)  
            print(ser_data)
        
       
        return Response(ser_data)
'''

class SelectQuestionView(APIView):
    def get(self, request, id_q):
        cache_key = f"{id_q}"
        cached_data = cache.get(cache_key)

        if cached_data:
            print("get data from REDIS")
            return Response(json.loads(cached_data))

        try:
            print("get data from SQL")
            question = Question.objects.prefetch_related('stages').get(id=id_q)
            serialized_data = QuestionSerializer(question).data

            #add to Redis
            cache.set(
                key=cache_key,
                value=json.dumps(serialized_data),
                timeout=3600
            )
            
            return Response(serialized_data)
            
        except Question.DoesNotExist:
            return Response(
                {"error": "question not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )


