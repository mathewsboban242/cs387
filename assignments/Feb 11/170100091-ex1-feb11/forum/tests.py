from django.test import TestCase
from forum.models import User, Topic, Comment

class ForumTestCase(TestCase):
	def setUp(self):
		self.u1=User.objects.create(name="santa")
		self.u1.save()
		self.u2=User.objects.create(name="banta")
		self.u2.save()
		self.t1=Topic.objects.create(title="politics",created_by=self.u1)
		self.t1.save()
		self.t2=Topic.objects.create(title="eggs",created_by=self.u2)
		self.t2.save()
		self.c1=Comment.objects.create(topic=self.t1,created_by=self.u1,subject="politics1",message="Keep America Great")
		self.c1.save()
		self.c2=Comment.objects.create(topic=self.t2,created_by=self.u2,subject="eggs1",message="Egg came first")
		self.c2.save()        

	def test_topic_search(self):
		q1=Topic.objects.filter(title='politics')
		d1=q1.all()
		print(d1)
		for x in d1:
			self.assertEqual(x.title,'politics')

	def test_comments_per_topic(self):
		q2=Comment.objects.filter(topic=self.t2)
		d2=q2.all()
		for x in q2:
			self.assertEqual(x,self.c2)

	def test_comments_by_selected_users(self):
		q3=Comment.objects.filter(created_by__name__contains='nta')
		d3=q3.all()
		list3=[x for x in d3]
		set3=set(list3)
		set1={self.c1,self.c2}
		self.assertSetEqual(set3, set1)