from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # special field for an e mail
    mail_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name()
    

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def tag_caption(self):
        return f"{self.caption}"
    
    def __str__(self):
        return self.tag_caption()

class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts", null=True ) # allow null values
    # automatically set whenever we save this model (date model)
    date = models.DateField(auto_now=True)
    # unique=true to ensure that we create a unique slug. db_index=True for db optimization 
    slug = models.SlugField(unique=True, db_index=True)
    # minimun text length of 10 characters
    content = models.TextField(validators=[MinLengthValidator(10)])
    # relationships
    tags = models.ManyToManyField(Tag)
    # on_delete=models.SET_NULL . set the author model to null if we delete a related author. null=True allow null values
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")

    # load an url that should represent and load the data for this specific model
    def get_absolute_url(self):
        return reverse('post-detail-page', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def full_post(self):
        return f"Title: {self.title} Excerpt: {self.excerpt} Tag: {self.tags} Author: {self.author} Content: {self.content}"
    
    def __str__(self):
        return self.full_post()
    
class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    # _("") used for translation
    user_email = models.EmailField(max_length=254)
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
