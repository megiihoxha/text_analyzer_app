from django.urls import path
from .views import AnalyzeTextView, RegisterView, LoginView, AnalysisLogListView

urlpatterns = [
    path('analyze/', AnalyzeTextView.as_view(), name='analyze-text'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('history/', AnalysisLogListView.as_view(), name='analysis-history'),

]

