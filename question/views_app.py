from django.views import View
from .models import Question,Stage, UserProgress
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer ,GetAnswerSerializer,CorectOptionSerializer, StageSerializer,AllQuestionSerializer, SelectQuestionSerializer,QuestionFormSerializer
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
        token_payload = request.auth  # اطلاعات کامل JWT
        #get data for integral category
        integral = UserProgress.objects.filter(user=request.user, category=1).first()
        #get data for derivative category
        derivative= UserProgress.objects.filter(user=request.user, category=2).first()
        

        print("progress", integral)
        print("progress", derivative)

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



    def post(self, request, id_q, id_s):
        answer = GetAnswerSerializer(data=request.data)
        if answer.is_valid():
            cache_key = f"{id_q}:correct"
            cached_data = cache.get(cache_key)
            
            if cached_data:
                try:
                    cached_data = json.loads(cached_data)
                
                    print(cached_data[1])  

                    print(cached_data)
                    if cached_data[id_s - 1] == answer.validated_data['answer']:
                        print("correct")
                        return Response({"message": "correct"}, status=200)
                    else:
                        print("incorrect")
                        return Response({"message": "incorrect"}, status=200)
                    


                    

                except json.JSONDecodeError:
                    return Response({"error": "Unable to decode cached data"}, status=400)
            else:
                return Response({"error": "Data not found in cache"}, status=404)

























class SelectQuestionView(APIView):
# authentication_classes = [JWTAuthentication]
#    permission_classes = [IsAuthenticated]

    def get(self, request, id_q):
        print(f"User ID: {request.user.id}")

        def add_qustion_to_redis():
            cache_key = f"{id_q}:question"
            cached_data = cache.get(cache_key)

            if cached_data:
                print("REDIS")
                return Response(json.loads(cached_data))
            
            try:
                print("(SQL)")

                
                question = Question.objects.prefetch_related('stages').get(id=id_q)
                serialized_data = QuestionSerializer(question).data


                serialized_corect_option = CorectOptionSerializer(question.stages, many=True).data
                print(serialized_corect_option)

                # ذخیره در REDIS
                cache.set(
                    key=cache_key,
                    value=json.dumps(serialized_data),
                    timeout=400
                )

                cache_key = f"{id_q}:correct"
    
    # ذخیره لیست به عنوان یک رشته JSON
                cache.set(
                    cache_key,
                    json.dumps(serialized_corect_option), 
                    timeout=400
                    )

                # ذخیره داده برای کاربر خاص
               

                return Response(serialized_data)

            except Question.DoesNotExist:
                return Response(
                    {"error": "question not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        
    
       
        
        # سپس داده از Redis/SQL دریافت شود
        return add_qustion_to_redis()