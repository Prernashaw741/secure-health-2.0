from django.urls import path
from .views import UploadView, SaveView, ViewUploadsView, ViewTestsView

urlpatterns = [
    path("upload/",UploadView.as_view()),
    path("save/", SaveView.as_view()),
    path("view/", ViewUploadsView.as_view()),
    path("tests/", ViewTestsView.as_view())
]
