from datetime import datetime

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager


class Question(models.Model):
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    rating = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    count = models.IntegerField(default=0)
    date = models.DateField(default=datetime.now, blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Vote(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    value = models.BooleanField(default=True)
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="votes_on",
        on_delete=models.CASCADE,
    )
    object_id = models.CharField(max_length=50, blank=True, null=True)
    vote = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        index_together = ("content_type", "object_id")
        unique_together = ("user", "content_type", "object_id")


class Answer(models.Model):
    question = models.ForeignKey("blog.Question", on_delete=models.CASCADE)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    answer = models.TextField()
    likes = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    date = models.DateField(default=datetime.now, blank=True)
    votes = GenericRelation(Vote)

    def save(self, *args, **kwargs):
        print(self.question.count)
        self.question.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.question.count -= 1
        self.question.save()
        super().delete(*args, **kwargs)

    def get_upvoters(self):
        return [vote.user for vote in self.votes.filter(value=True)]

    def __str__(self):
        return self.answer

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Answer"
        verbose_name_plural = "Answers"


class Comment(models.Model):
    answer = models.ForeignKey("blog.Answer", on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)

    def __str__(self):
        pass

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Vote(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    value = models.BooleanField(default=True)
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="votes_on",
        on_delete=models.CASCADE,
    )
    object_id = models.CharField(max_length=50, blank=True, null=True)
    vote = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        index_together = ("content_type", "object_id")
        unique_together = ("user", "content_type", "object_id")
