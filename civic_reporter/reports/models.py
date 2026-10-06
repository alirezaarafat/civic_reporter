"""
App2_reports models.

Only Area and Category are defined here for now -- Report,
ReportStatusHistory, Verification, Comment, Upvote and Notification
will be added in the next step, once accounts/login is confirmed working.
"""

from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Areas"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
