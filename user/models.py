# Create your models here.
from django.db import models
from django.contrib.auth.models import User
#from ckeditor.fields import RichTextField
#from ckeditor_uploader.fields import RichTextUploadingField
#from taggit.managers import TaggableManager

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images", default="/user.png")
    twitter = models.CharField(max_length=200,null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    balance = models.CharField(max_length=30, blank=True)



class City(models.Model):
    pname = models.CharField(max_length=255)
    lstate = models.CharField(max_length=255)

    def __str__(self):
        return self.pname

class Data(models.Model):
	cname = models.CharField(max_length=200, blank=True, null=True)
	lname = models.CharField(max_length=200, blank=True, null=True)
	dsalary = models.CharField(max_length=200, blank=True, null=True)


	def __str__(self):
		name = str(self.cname)
		if self.cname:
			name += ' ' + str(self.lname)
		return name


class Jobs(models.Model):
    jname = models.CharField(max_length=300)
    jnumber = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=300, blank=True)
    description = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=300,  blank=True)
    job_type = models.CharField( max_length=100,  blank=True)
    salary = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300,  blank=True)
    company_description = models.CharField(max_length=100, blank=True)

    url = models.URLField(max_length=200,blank=True)
    #last_date = models.DateField(max_length=30 , blank=True)
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.jname




    

    
class Post(models.Model):
    jobtitle = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=300, blank=True)
    qualification = models.TextField( null=True ,blank=True)
    location = models.CharField(max_length=300,  blank=True)
    salary = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300,  blank=True)

    def __str__(self):
        return self.jobtitle

 
class Tag(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name
