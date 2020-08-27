from django.urls import path

from .views import (
    AnswerCreateView,
    AnswerDeleteView,
    AnswerUpdateView,
    QuestionCreateView,
    QuestionDeleteView,
    QuestionDetailView,
    QuestionListView,
    QuestionUpdateView,
    SearchView,
    add_like,
)

app_name = "blog"
urlpatterns = [
    path("", view=QuestionListView.as_view(), name="home"),
    path("search/", SearchView.as_view(), name="search_results"),
    path("posts/create/", view=QuestionCreateView.as_view(), name="question-create"),
    path(
        "posts/<slug:slug>/", view=QuestionDetailView.as_view(), name="question-detail"
    ),
    path(
        "posts/<slug:slug>/delete/",
        view=QuestionDeleteView.as_view(),
        name="question-delete",
    ),
    path(
        "posts/<slug:slug>/edit",
        view=QuestionUpdateView.as_view(),
        name="question-edit",
    ),
    path(
        "posts/<slug:slug>/answer/",
        view=AnswerCreateView.as_view(),
        name="answer-create",
    ),
    path(
        "posts/answers/<int:pk>/delete/",
        view=AnswerDeleteView.as_view(),
        name="answer-delete",
    ),
    path(
        "posts/answers/<int:pk>/edit/",
        view=AnswerUpdateView.as_view(),
        name="answer-edit",
    ),
    path("ajax/add_like/", add_like, name="add_like"),
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
]
