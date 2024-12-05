from django.db import models
from accounts.models import User
from .utils import convert_and_remove_images

class Question(models.Model):
    title = models.CharField(max_length=255)  
    question_latex = models.TextField(null = True, blank=True) 
    description = models.TextField(null=True)
    score = models.SmallIntegerField(null=True)



    DIFFICULTY_CHOICES = [
        ('easy', 'easy'),
        ('medium','medium'),
        ('hard', 'hard'),
    ]

    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, null=True)
    solved_count = models.PositiveIntegerField(default=0)


    
    def __str__(self):
        return f"{self.id} - {self.title}"
    
   
    
       
    


class Stage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='stages')
    stage_number = models.PositiveIntegerField()  

    option1_title = models.CharField(max_length=255, default="")
    option1_latex = models.TextField(blank=True, null=True)
    option1_descrption = models.TextField(blank=True, null= True)

    option2_title = models.CharField(max_length=255, default="")
    option2_latex = models.TextField(blank=True, null=True)
    option2_descrption = models.TextField(blank=True, null= True)

    option3_title = models.CharField(max_length=255, default="")
    option3_latex = models.TextField(blank=True, null=True)
    option3_descrption = models.TextField(blank=True, null= True)

    option4_title = models.CharField(max_length=255, default="")
    option4_latex = models.TextField(blank=True, null=True)
    option4_descrption = models.TextField(blank=True, null= True)

    correct_option = models.CharField(max_length=255, default='1')  

    def __str__(self):
        return f"Stage {self.stage_number} for {self.question.title}"

   



class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} - {self.question} - {self.score}'
    


class UserSolvedQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    solve = models.BooleanField(default=False)



