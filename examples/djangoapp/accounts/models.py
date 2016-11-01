from django.db import models


class User(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    email = models.EmailField()
    registered_at = models.DateTimeField()
    last_logged_in_at = models.DateTimeField(null=True)
    last_logged_out_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.email
