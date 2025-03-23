from django.db import models
from accounts.models import User
#from .utils import convert_and_remove_images


#add category for any question

#The score value is automatically assigned based on the difficulty level and the number of stages.

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('integral', 'integral'),
        ('derivative','derivative'),
    ]
    category_name = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True)
    def __str__(self):
        return self.get_category_name_display()
    

class Question(models.Model):
    title = models.CharField(max_length=255)  
    question_latex = models.TextField(null = True, blank=True) 
    description = models.TextField(null=True)
    stage = models.SmallIntegerField(null=True)
    score = models.SmallIntegerField(null=True, blank=True)

    DIFFICULTY_CHOICES = [
        ('easy', 'easy'),
        ('medium','medium'),
        ('hard', 'hard'),
    ]

    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, null=True)
    
    def save(self, *args, **kwargs):
   
        is_new = self.pk is None
    
        super().save(*args, **kwargs) 
    
        if is_new:
            num_stages = self.stages.count()
        
            if self.difficulty == 'easy':
                self.score = num_stages + 3
            elif self.difficulty == 'medium':
                self.score = num_stages + 6
            elif self.difficulty == 'hard':
                self.score = num_stages + 9

            super().save(update_fields=['score'])  


    def __str__(self):
        return f"{self.id} - {self.title} - {self.score}"

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

   

#show the roadmap for answer the category question
class Roadmap(models.Model):

    name = models.CharField(max_length=15) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()  

    def __str__(self):
        return f'{self.category} - {self.name}'
    


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ذخیره پیشرفت در هر 
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE,null=True, blank=True)
    last_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)  # آخرین سوال حل شده
    completed_questions = models.ManyToManyField(Question, related_name='completed_by_users', blank=True)  # سوالات حل شده
    score = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user} - {self.category} - {self.last_question} - {self.score}'


