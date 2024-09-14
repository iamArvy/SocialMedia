from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pfp = models.ImageField(upload_to='profile-pictures', blank=True, null=True)
    banner = models.ImageField(upload_to='banners', blank=True, null=True)
    followers = models.ManyToManyField('self', related_name='user_followers', blank=True, symmetrical=False)
    following = models.ManyToManyField('self', related_name='user_followings', blank=True, symmetrical=False)
    posts = models.ManyToManyField('Post', related_name='user_posts', blank=True)
    bio = models.TextField(blank=True, null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes')
    comments = models.ManyToManyField('Comment', related_name='comments')
    # liked = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.post} by {self.user.username}"
    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "creator": self.sender.user,
    #         "likes": [user for user in self.likes.all()],
    #         "post": self.post,
    #         "timestamp": self.created_at.strftime("%b %d %Y, %I:%M %p"),
    #     }
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='comment_likes')

    def __str__(self):
        return f"{self.user.username} comment on {self.post.post}"