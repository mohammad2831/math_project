from django.db import models
from django.db import models
from accounts.models import User
from question.models import Question




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='pcomments')
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%Y-%m-%d')} to {self.question.title}"