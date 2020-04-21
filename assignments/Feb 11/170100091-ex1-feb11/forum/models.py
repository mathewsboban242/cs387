from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)

class Topic(models.Model):
    title = models.CharField(max_length=200,blank=False,null=False)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)

class Comment(models.Model):
	topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE)
	subject = models.CharField(max_length=200,blank=False)
	message = models.CharField(max_length=1000)