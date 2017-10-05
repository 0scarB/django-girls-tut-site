from django.utils import timezone
from django.db import models


class Maze(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)

    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    horizontal_spacing = models.PositiveSmallIntegerField(default=10)
    vertical_spacing = models.PositiveSmallIntegerField(default=10)

    horizontal_path_width = models.DecimalField(
        max_digits=17, decimal_places=4, default=0.5)
    vertical_path_width = models.DecimalField(
        max_digits=17, decimal_places=4, default=0.5)

    path_r = models.PositiveSmallIntegerField(default=255)
    path_g = models.PositiveSmallIntegerField(default=255)
    path_b = models.PositiveSmallIntegerField(default=255)

    wall_r = models.PositiveSmallIntegerField(default=0)
    wall_g = models.PositiveSmallIntegerField(default=0)
    wall_b = models.PositiveSmallIntegerField(default=0)

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
