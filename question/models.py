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
    order = models.PositiveIntegerField()  #ترتیب سوال در road map

    def __str__(self):
        return f'{self.category} - {self.name}'
    


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ذخیره پیشرفت در هر دسته‌بندی
    last_question = models.PositiveIntegerField(null=True, blank=True)  # شماره آخرین سوال حل شده
    completed_question_orders = models.JSONField(default=list)  # لیستی از شماره سؤالات حل‌شده
    score = models.PositiveIntegerField(default=0)

    def add_completed_question(self, question):
        """افزودن شماره‌ی سوال حل‌شده به لیست"""
        roadmap_entry = Roadmap.objects.filter(question=question, category=self.category).first()
        if roadmap_entry:
            # به‌روزرسانی مقدار `last_question_order`
            self.last_question_order = roadmap_entry.order
            
            # اضافه کردن شماره سوال به لیست اگر از قبل وجود نداشته باشد
            if roadmap_entry.order not in self.completed_question_orders:
                self.completed_question_orders.append(roadmap_entry.order)

            self.save(update_fields=['last_question_order', 'completed_question_orders'])

    def __str__(self):
        return f'{self.user} - {self.category} - Last Q: {self.last_question_order} - Score: {self.score}'
