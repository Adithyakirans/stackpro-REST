from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Questions(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image",null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def question_answer(self):
        return self.answers_set.all()


class Answers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer = models.CharField(max_length=250)
    upvote = models.ManyToManyField(User,related_name="upvote")
    
    def __str__(self):
        return self.answer
    
    # upvote count
    @property
    def upvote_count(self):
        return self.upvote.all().count()