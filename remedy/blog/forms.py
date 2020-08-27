from blog.models import Answer, Question
from django.forms import ModelForm


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ("question", "tags")


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ("answer",)
