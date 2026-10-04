from django.urls import path

# from .views import StudentListView, TopStudentsView

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import StudentViewSet

router = DefaultRouter()

router.register('students', StudentViewSet)

# urlpatterns = router.urls

urlpatterns = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += router.urls

# urlpatterns = [
#     path("api/students/", StudentListView.as_view(), name='student_list'),
#     path("api/students/top_performers/", TopStudentsView.as_view(), name='top_students'),
#     path("", views.welcome, name="welcome"),
#     path("marks/", views.student_marks, name="student_marks"),
#     path("add_student/", views.add_student, name="add_students"),
#     path("students/", views.list_students, name='student_list'),
#     path("login/", views.login_view, name='signin'),
#     path("logout/", views.logout_view, name='signout')
# ]

# The marks/ page needed its own path() entry because Django
#  must know which view function should handle that specific URL.
# The empty path already points to welcome, while marks/ points 
# to the separate student_marks view.