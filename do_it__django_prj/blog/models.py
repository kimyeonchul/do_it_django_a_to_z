from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField()
    # author

    def __str__(self):
        # return self.title
        return f'[{self.pk}]{self.title}'