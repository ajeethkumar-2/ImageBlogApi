from django.db import models

try:
    from ..users.models import User
except:
    from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/post_images", null=True)
    description = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return self.title

    objects = None
