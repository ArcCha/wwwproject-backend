from django.db import models


class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User',
                              related_name='images',
                              on_delete=models.CASCADE)
    image = models.ImageField(max_length=255)

    class Meta:
        ordering = ('created',)


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User',
                              related_name='comments',
                              on_delete=models.CASCADE)
    image = models.ForeignKey('backend.Image',
                              related_name='comments')
    text = models.CharField(max_length=1000)

    class Meta:
        ordering = ('created',)
