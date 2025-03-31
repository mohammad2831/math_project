from django.views import View
from .models import Question,Stage, UserProgress
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserStatusTableSerializer,QuestionSerializer ,GetAnswerSerializer,CorectOptionSerializer, StageSerializer,AllQuestionSerializer, SelectQuestionSerializer,QuestionFormSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core.cache import cache
import json
from rest_framework_simplejwt.authentication import JWTAuthentication



from django.shortcuts import render, get_object_or_404, redirect


class test(APIView):
    authentication_classes = [JWTAuthentication]  # احراز هویت با توکن JWT
    permission_classes = [IsAuthenticated]
    def get (self, request):
        print("test is okkkk")
        #return Response({"message":"ok"})
        user = request.user  # اطلاعات کاربر
        

        cache_key_user = f"user_status:{user.id}:{15}"


        cached_data = cache.get(cache_key_user)
        if cached_data:
            print("User status found in cache!")
            # تبدیل داده سریالایز شده به دیکشنری
            user_status = json.loads(cached_data)

            # افزودن مقدار جدید به لیست
            for i in range(1, 5):
                user_status['progress_list'].append(f"{i}")


            if 0 <= 2 < len(user_status['progress_list']):
            # برگرداندن مقدار موجود در ایندکس خاص
                value_at_index = user_status['progress_list'][2]
            print(f"Value at index {2}: {value_at_index}")
            # ذخیره داده جدید در کش
            cache.set(
                cache_key_user,
                json.dumps(user_status),  # تبدیل داده به JSON
                timeout=400
            )
            print("Value added to progress list and saved in Redis.")
            #return user_status
        else:
            print("User status not found in cache.")
            #return None
        return Response({"message":"ok"})




















        return Response({
            "user_id": user.id,
            "email": user.email,
            
           # "jwt_payload": token_payload  # اینجا محتوای کامل توکن را داری
        })

class AllQuestionView(APIView):

    def get(self, request):
        questions = Question.objects.all()

        serializer = AllQuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)

























class QuestionView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def get(self, request, id_q, id_s):
        question_cache_key = f"question_{id_q}" 
        cached_question_data = cache.get(question_cache_key)
        
        if cached_question_data:
            ser_data = cached_question_data
        else:
            question = get_object_or_404(Question, id=id_q)
            ser_data = QuestionFormSerializer(question).data
            ser_data_json = json.dumps(ser_data)
            cache.set(question_cache_key, ser_data_json, timeout=1200) 

           
            stages = Stage.objects.filter(question_id=id_q).order_by('stage_number')
            stages_data = StageSerializer(stages, many=True).data
            stages_cache_key = f"stages_{id_q}"
            cache.set(stages_cache_key, stages_data, timeout=1200)  
        
      
        stage_cache_key = f"stage_{id_q}_{id_s}" 
        cached_stage_data = cache.get(stage_cache_key)

        if cached_stage_data:
            stage_data = cached_stage_data
        else:
            stage = Stage.objects.get(question_id=id_q, stage_number=id_s)
            stage_data = StageSerializer(stage).data
            cache.set(stage_cache_key, stage_data, timeout=1200) 
        
        return Response({'stage': stage_data, 'form': ser_data})





    #check if answer is correct or not
    #and add it in user status table
    #key in redis is :1:user_status:user-id:question-is
    #and add it in progress list
    def post(self, request, id_q, id_s):
        user = request.user
        
        # answer user send it    
        answer = GetAnswerSerializer(data=request.data)
        if answer.is_valid():

            #fetch correct option list in redis with question id
            cache_key_correct_option = f"correct_option:{id_q}"
            cached_data_correct_option = cache.get(cache_key_correct_option)

            #fetch user status list in redis with question id
            cache_key_user = f"user_status:{user.id}:{15}"
            cached_data_user_status = cache.get(cache_key_user)
            
            if cached_data_user_status:
                if cached_data_correct_option:
                    try:
                        cached_data_user_status_load = json.loads(cached_data_user_status)
                        cached_data_correct_option_load = json.loads(cached_data_correct_option)
                    
                        #check if answer is correct or not
                        if cached_data_correct_option_load[id_s - 1] == answer.validated_data['answer']:

                            #add correct answer in user status table , progress list with 1
                            cached_data_user_status_load['progress_list'].append("1")
                            print("correct")
                            
                            cache.set(
                                        cache_key_user,
                                        json.dumps(cached_data_user_status_load),
                                        timeout=400
                                    )

                            return Response({"message": "correct"}, status=200)
                        
                        else:
                            #add incorrect answer in user status table , progress list with 0
                            cached_data_user_status_load['progress_list'].append("0")
                            print("incorrect")

                            cache.set(
                                        cache_key_user,
                                        json.dumps(cached_data_user_status_load),
                                        timeout=400
                                    )
                            
                            return Response({"message": "incorrect"}, status=200)
                        


                        

                    except json.JSONDecodeError:
                        return Response({"error": "Unable to decode cached data"}, status=400)
                else:
                    return Response({"error": "Data not found in cache"}, status=409)    
            else:
                return Response({"error": "Data not found in cache"}, status=408)





















class SelectQuestionView(APIView):
    def get(self, request, id_q):
        #first make and save user status table after save question

        # make user table and add userr info in redis
        self.user_status_table(request, id_q)

        # use for make corect option list and send question for flutter  
        return self.add_question_to_redis(id_q)


    #make user tatus table in redis
    #key in redis is :1:user_status:user-id:question-is
    def user_status_table(self, request, id_q):


        user_id = request.user.id
        cache_key_user = f"user_status:{user_id}:{id_q}"

        #check if user table is in redis
        cached_data = cache.get(cache_key_user)
        if cached_data:
            print("User status found in cache!")
            return json.loads(cached_data)

       
        #add empty list for save user status in other steps
        user_status_serialized = {
            "progress_list": [] 
        }

        #add user info in user status table and set it in redis
        cache.set(
            cache_key_user,
            json.dumps(user_status_serialized),
            timeout=400
        )
        print("User status added to Redis.")

        return user_status_serialized


    #fetch question from sql and add it in redis
    #with gzip format send it to flutter and set it in gzip_middleware.py file
    def add_question_to_redis(self, id_q):

        cache_key_question = f"question:{id_q}"

        #check if question is in redis
        cached_data = cache.get(cache_key_question)
        if cached_data:
            print("Question found in cache!")
            return Response(json.loads(cached_data))

        try:
            print("Fetching question from DB (SQL)")
            #fetch quseton from sql
            question = Question.objects.prefetch_related('stages').get(id=id_q)
            
            #serialize question and all stages
            serialized_data = QuestionSerializer(question).data

            #serialize all stages and get a list just with corect option any stage
            serialized_correct_option = CorectOptionSerializer(question.stages, many=True).data

            #save question in redis            
            cache.set(cache_key_question, json.dumps(serialized_data), timeout=400)

            #save corect option in redis
            cache.set(f"correct_option:{id_q}", json.dumps(serialized_correct_option), timeout=400)

            print("Question added to Redis.")
            return Response(serialized_data)

        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)
