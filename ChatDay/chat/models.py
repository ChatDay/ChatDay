from django.db import models



class Topic(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Message(models.Model):
    user = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Topic 모델과의 관계 추가

    def __str__(self):
        return f"{self.user}: {self.content[:20]}"