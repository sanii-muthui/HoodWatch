from django.db import models
from django.contrib.auth.models import User
from statistics import mean


# Create your models here.
class Profile(models.Model):
    profile = models.OneToOneField(User,on_delete=models.CASCADE, null = True)
    bio = models.CharField(max_length=100)
    photo = models.ImageField(upload_to = 'profile/',default='fbfba5feddcfae6c24fa528c7749eafc.jpg' ,blank = True)
    neighbourhood = models.ForeignKey('Neighbourhood', blank=True, null=True)
    pub_date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

class Neighbourhood(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='neighimage/', null=True)
    admin = models.ForeignKey(Profile, related_name='hoods', null=True)
    description = models.CharField(max_length = 100,default='hoodNation...')
    occupants = models.CharField(max_length=100, blank = True)
    content=models.PositiveIntegerField(choices=list(zip(range(1, 11), range(1, 11))), default=0)
    def __str__(self):
        return self.name
    def save_neighbourhood(self):
        self.save()
    def delete_neighbourhood(self):
        self.delete()

class Business(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=70,blank=True, null= True, unique= True)
    phone_number = models.CharField(max_length=10)
    image = models.ImageField(upload_to='bsimage/')
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='businesses')
    description = models.CharField(max_length = 100)
    profile = models.ForeignKey(Profile, related_name='profiles')
    def __str__(self):
        return self.name
    def save_business(self):
        self.save()
    def delete_business(self):
        self.delete()
    @classmethod
    def search_by_name(cls,search_term):
        business = cls.objects.filter(title__icontains=search_term)
        return business    

class Location(models.Model):
    name = models.CharField(max_length=30)

    def save_location(self):
        self.save()

    def delete_location(self):
        self.delete()

    def __str__(self):
        return self.name

class Review(models.Model):
    '''
    '''
    content=models.IntegerField(blank=True,default=0)
    neighbourhood=models.ForeignKey(Neighbourhood,on_delete=models.CASCADE)
    judge=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    average_review = models.IntegerField(blank=True, default=0)

    def save_review(self):
        self.save()
    def __str__(self):
        return f'{self.neighbourhood.title}:Review-{self.content}-{self.neighbourhood.id}'    
    @classmethod
    def get_all_reviews(cls,neighbourhood_id):
        content=round(mean(cls.objects.filter(neighbourhood_id=neighbourhood_id).values_list('content',flat=True)))
        average_review=content

        return  {

            'average_review':average_review
        }

class Post(models.Model):
    post = models.CharField(max_length=100)
    image = models.ImageField(upload_to='neighimage/', null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='posts')
    def __str__(self):
        return self.post
  
class Comment(models.Model):
  comment = models.TextField()
  post = models.ForeignKey(Post,on_delete=models.CASCADE)
  postername= models.ForeignKey(User, on_delete=models.CASCADE)
  pub_date = models.DateTimeField(auto_now_add=True)
  def __str__(self):
        return self.comment