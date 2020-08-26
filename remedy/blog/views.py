from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from .forms import AnswerForm, QuestionForm
from .models import Answer, Question


# Create your views here.
class AuthorRequiredMixin(View):
    """Mixin to validate than the loggedin user is the creator of the object
    to be edited or updated."""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


@method_decorator([login_required], name="dispatch")
class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "exp/question.html"

    def form_valid(self, form):

        question = form.save(commit=False)
        question.author = self.request.user
        question.save()
        return super(QuestionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("blog:home")


@method_decorator([login_required], name="dispatch")
class AnswerCreateView(CreateView):
    model = Answer
    template_name = "exp/answer.html"
    form_class = AnswerForm

    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.author = self.request.user
        question = Question.objects.get(slug=self.request.path.split("/")[2])
        answer.question = question
        return super(AnswerCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("blog:home")


@method_decorator([login_required], name="dispatch")
class QuestionUpdateView(AuthorRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "exp/question.html"

    def get_success_url(self):
        return reverse("blog:home")


@method_decorator([login_required], name="dispatch")
class AnswerUpdateView(AuthorRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = "exp/answer.html"

    def get_success_url(self):
        return reverse("blog:home")


class QuestionListView(ListView):
    model = Question
    paginate_by = 20
    template_name = "exp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Question.objects.all()
        return context


class QuestionDetailView(DetailView):
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "exp/detail.html"
    model = Question

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = self.object.answer_set.all()
        return context


@login_required
def add_like(request):
    id = request.GET.get("id", None)
    state = request.GET.get("state", None)
    answer = Answer.objects.get(id=id)
    answer.likes += int(state)
    state = int(state) + 1
    if state:
        value = True
    else:
        value = False
    answer.votes.update_or_create(
        user=request.user, defaults={"value": value},
    )
    answer.question.count -= 1
    answer.save()
    data = {
        "likes": answer.likes,
        "id": answer.id,
    }
    return JsonResponse(data)


def update_votes(obj, user, value):

    obj.votes.update_or_create(
        user=user, defaults={"value": value},
    )
    obj.count_votes()


# class QuestionDeleteView(DeleteView):
#     model = Question
#     template_name = ".html"

#     def get_success_url(self):
#         return reverse('blog:home')


# class AnswerDeleteView(DeleteView):
#     model = Answer
#     template_name = ".html"

#     def get_success_url(self):
#         return reverse('blog:home')


class SearchView(ListView):
    model = Question
    template_name = "exp/search_result.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", None)
        or_lookup = []
        if query is not None:
            or_lookup = Q(question__icontains=query)

        result = Question.objects.filter(or_lookup)
        return result
