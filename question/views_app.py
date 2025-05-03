from django.views import View
from .models import QuestionIntegral,QuestionDerivative,StageIntegral,StageDerivative, UserProgress
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CorectOptionDerivativeSerializer,QuestionDerivativeSerializer,StageDerivativeSerializer,UserStatusTableSerializer,QuestionIntegralSerializer ,GetAnswerSerializer,CorectOptionIntegralSerializer, StageIntegralSerializer,AllQuestionSerializer, SelectQuestionSerializer,QuestionDerivativeFormSerializer,QuestionIntegralFormSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core.cache import cache
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render, get_object_or_404, redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



def test_ws(request):
    return render(request, 'test_ws.html')


class testacount(APIView):
    authentication_classes = [JWTAuthentication]  # احراز هویت با توکن JWT
    permission_classes = [IsAuthenticated]
    def get (self, request):
        print("test is okkkk")
        #return Response({"message":"ok"})
        user = request.user  # اطلاعات کاربر
        print()
        return Response(user.user_id)
    

'''
class AllQuestionView(APIView):

    def get(self, request):
        questions = Question.objects.all()

        serializer = AllQuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)

'''





















###########################################################################################################################

class QuestionIntegralView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

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
        print("post")
        #self.calcute_score(request, id_q)
        user = request.user
        
        # answer user send it    
        answer = GetAnswerSerializer(data=request.data)
        if answer.is_valid():

            #fetch correct option list in redis with question id
            cache_key_correct_option = f"correct_option_integral:{id_q}"
            cached_data_correct_option = cache.get(cache_key_correct_option)

            #fetch user status list in redis with question id
            cache_key_user = f"user_status_integral:{user.id}:{id_q}"
            cached_data_user_status = cache.get(cache_key_user)
            
            if cached_data_user_status:
                if cached_data_correct_option:
                    try:
                        cached_data_user_status_load = json.loads(cached_data_user_status)
                        cached_data_correct_option_load = json.loads(cached_data_correct_option)
                    
                        #check if answer is correct or not
                        if cached_data_correct_option_load[id_s - 1] == answer.validated_data['answer']:

                            #check if all question is solved and add score
                            if id_s == len(cached_data_correct_option_load):
                                result =self.calculate_score(request, id_q) 
                                print("test calculate")
                                cache.delete(cache_key_user)
                                UserProgress.objects.filter(user=user).update(score=result["score"])
                                return Response({"score": result["score"],"mistake":result["mistake"],"message":result["message"]}, status=200)

                            if id_s >= len(cached_data_correct_option_load):
                                return Response({"message": "the stage is finished"}, status=405)

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
                    return Response({"error": "problem in correct option"}, status=409)    
            else:
                return Response({"error": "problem in user status table"}, status=408)
            

    #claculte score for user when all question is solved
    




    def calculate_score(self, request, id_q):
        user=request.user
        #fetch user status list in redis with user id
        cache_key_user = f"user_status_integral:{user.id}:{id_q}"
        cached_data_user_status = cache.get(cache_key_user)
        cached_data_user_status_load = json.loads(cached_data_user_status)
        print(cached_data_user_status_load['progress_list'])

        #fetch question in redis with question id for get question score
        cashe_key_question = f"question_integral:{id_q}"
        cached_data_question = cache.get(cashe_key_question)
        cached_data_question_load = json.loads(cached_data_question)
        print("total-score",cached_data_question_load['score'])
        
        mistake = cached_data_user_status_load['progress_list'].count("0")
        print("mistake:",mistake)
        total_score = cached_data_question_load['score'] - mistake
        #update user score in sql
        user.progress.filter(user=user).update(score=(cached_data_question_load['score'] - mistake))      


        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "send_score",
                "score": total_score,
                "mistake": mistake
            }
        )

        return {
            'score':total_score,
            'mistake':mistake,
            'message':"score is updated"
        }
        #return Response({"message": "score is updated"}, status=200)
        








class QuestionDerivativeView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    #show queston
    def get(self, request, id_q, id_s):
        #check cashe key from redis
        question_cache_key = f"question_derivative{id_q}" 
        cached_question_data = cache.get(question_cache_key)
        
        if cached_question_data:
            ser_data = cached_question_data

        #if cache is not exist then fetch from sql
        #and set it in redis
        else:
            question = get_object_or_404(QuestionDerivative, id=id_q)
            ser_data = QuestionDerivativeFormSerializer(question).data
            ser_data_json = json.dumps(ser_data)
            cache.set(question_cache_key, ser_data_json, timeout=1200) 

           
            stages = StageDerivative.objects.filter(question_id=id_q).order_by('stage_number')
            stages_data = StageDerivativeSerializer(stages, many=True).data
            stages_cache_key = f"stages_{id_q}"
            cache.set(stages_cache_key, stages_data, timeout=1200)  
        
      
        stage_cache_key = f"stage_derivative{id_q}_{id_s}" 
        cached_stage_data = cache.get(stage_cache_key)

        if cached_stage_data:
            stage_data = cached_stage_data
        else:
            stage = StageDerivative.objects.get(question_id=id_q, stage_number=id_s)
            stage_data = StageDerivativeSerializer(stage).data
            cache.set(stage_cache_key, stage_data, timeout=1200) 
        
        return Response({'stage': stage_data, 'form': ser_data})



    #check if answer is correct or not
    #and add it in user status table
    #key in redis is :1:user_status:user-id:question-is
    #and add it in progress list
    def post(self, request, id_q, id_s):
        print("post")
        #self.calcute_score(request, id_q)
        user = request.user
        
        # answer user send it    
        answer = GetAnswerSerializer(data=request.data)
        if answer.is_valid():

            #fetch correct option list in redis with question id
            cache_key_correct_option = f"correct_option_derivative:{id_q}"
            cached_data_correct_option = cache.get(cache_key_correct_option)

            #fetch user status list in redis with question id
            cache_key_user = f"user_status_derivative:{user.id}:{id_q}"
            cached_data_user_status = cache.get(cache_key_user)
            
            if cached_data_user_status:
                if cached_data_correct_option:
                    try:
                        cached_data_user_status_load = json.loads(cached_data_user_status)
                        cached_data_correct_option_load = json.loads(cached_data_correct_option)
                    
                        #check if answer is correct or not
                        if cached_data_correct_option_load[id_s - 1] == answer.validated_data['answer']:

                            #check if all question is solved and add score
                            if id_s == len(cached_data_correct_option_load):
                                result =self.calculate_score(request, id_q) 
                                print("test calculate")
                                
                                cache.delete(cache_key_user)
                                UserProgress.objects.filter(user=user).update(score=result["score"])



                                return Response({"score": result["score"],"mistake":result["mistake"],"message":result["message"]}, status=200)

                            if id_s >= len(cached_data_correct_option_load):
                                return Response({"message": "the stage is finished"}, status=405)

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
                    return Response({"error": "problem in correct option"}, status=409)    
            else:
                return Response({"error": "problem in user status table"}, status=408)
            

    #claculte score for user when all question is solved
    




    def calculate_score(self, request, id_q):
        user=request.user
        print("hi")
        print(f"user_{user.id}")
        #fetch user status list in redis with user id
        cache_key_user = f"user_status_derivative:{user.id}:{id_q}"
        cached_data_user_status = cache.get(cache_key_user)
        cached_data_user_status_load = json.loads(cached_data_user_status)
        print(cached_data_user_status_load['progress_list'])

        #fetch question in redis with question id for get question score
        cashe_key_question = f"question_derivative:{id_q}"
        cached_data_question = cache.get(cashe_key_question)
        cached_data_question_load = json.loads(cached_data_question)
        print("total-score",cached_data_question_load['score'])
        
        mistake = cached_data_user_status_load['progress_list'].count("0")
        print("mistake:",mistake)
        total_score = cached_data_question_load['score'] - mistake
        #update user score in sql
        user.progress.filter(user=user).update(score=(cached_data_question_load['score'] - mistake))      


        channel_layer = get_channel_layer()
        print("hi")
        print(f"user_{user.id}")
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "send_score",
                "score": total_score,
                "mistake": mistake
            }
        )

        return {
            'score':total_score,
            'mistake':mistake,
            'message':"score is updated"
        }
        #return Response({"message": "score is updated"}, status=200)
        










###############################################################################################################################3
class SelectQuestionIntegralView(APIView):
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
        print(user_id)
        cache_key_user = f"user_status_integral:{user_id}:{id_q}"

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



class SelectQuestionDerivativeView(APIView):
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
        print(user_id)
        cache_key_user = f"user_status_derivative:{user_id}:{id_q}"

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

        cache_key_question = f"question_derivative:{id_q}"

        #check if question is in redis
        cached_data = cache.get(cache_key_question)
        if cached_data:
            print("Question found in cache!")
            return Response(json.loads(cached_data))

        try:
            print("Fetching question from DB (SQL)")
            #fetch quseton from sql
            question = QuestionDerivative.objects.prefetch_related('stages').get(id=id_q)
            
            #serialize question and all stages
            serialized_data = QuestionDerivativeSerializer(question).data

            #serialize all stages and get a list just with corect option any stage
            serialized_correct_option = CorectOptionDerivativeSerializer(question.stages, many=True).data

            #save question in redis            
            cache.set(cache_key_question, json.dumps(serialized_data), timeout=400)

            #save corect option in redis
            cache.set(f"correct_option_derivative:{id_q}", json.dumps(serialized_correct_option), timeout=400)

            print("Question added to Redis.")
            return Response(serialized_data)

        except QuestionDerivative.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)
