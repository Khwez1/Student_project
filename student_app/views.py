# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, render
# from .models import Student, Subject

# def welcome(request):
#     return HttpResponse("Welcome to the Students App!")

# def student_marks(request):
#     student = Student.objects.first()

#     if student is None:
#         return HttpResponse("No students have been added yet.")

#     context = {
#         "student": student
#     }

#     return render(request, "marks.html", context)

# def list_students(request):
#     students = Student.objects.all()

#     context = {
#         'students': students
#     }

#     return render(request, 'students.html', context)

# def login_view(request):
#     if request.method =='POST':
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('student_marks')
#     else:
#         return render(request, 'accounts/login.html',)    

# def logout_view(request):
#     if request.method =='POST':
#         logout(request)
#         return redirect('signin')
#     else:
#         return render(request, 'accounts/logout.html')

# @login_required
# def add_student(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         mark = request.POST.get('marks')
#         student = Student.objects.create(name=name, mark=mark, class_group=None)
#         subject = Subject.objects.get(name="Python")
#         student.subjects.set([subject])
#         return redirect('student_list')
#     else:
#         return render(request, 'add_student.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
import requests
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Student

from .serializer import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    throttle_classes = [ScopedRateThrottle]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['mark', 'class_group']
    throttle_scope = None
    # permission_classes = [IsAuthenticated,]

    @action(detail=False, methods=['post'], throttle_scope='sync')
    def sync_external(self, request):
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        external_users = response.json()
        created = []
        errors = []
        for user in external_users:
            data = {'name': user['name'], 'mark': 75}
            serializer = StudentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                created.append(serializer.data)
            else:
                errors.append(serializer.errors)
        return Response({'created_count': len(created),
            'students': created, 'errors': errors}, status=status.HTTP_201_CREATED)

# class StudentListView(APIView):
#     def get(self, request):
#         students = Student.objects.all()
#         serializer = StudentSerializer(students, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):        
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TopStudentsView(APIView):
#     def get(self, request):
#         top_students = Student.objects.filter(mark__gte=80)
#         serializer = StudentSerializer(top_students, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         update_count = Student.objects.filter(mark__gte=80).update(is_top_performer=True)
#         return Response({"message": "Top students updated", "update_count": update_count}, status=status.HTTP_200_OK)
