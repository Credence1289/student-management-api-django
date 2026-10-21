
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Students


#Get all students and create students
@api_view(["GET", "POST"])
def student_list(request):

    if request.method == "GET":
        students = Students.objects.all()

        data = []

        for student in students:
            data.append({
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "age": student.age,
                "course": student.course,
                "teacher": student.teacher
            })

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        name = request.data.get("name")
        email = request.data.get("email")
        age = request.data.get("age")
        course = request.data.get("course")
        teacher = request.data.get("teacher")

        # Check required fields
        if not all([name, email, age, course, teacher]):
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check age
        try:
            age = int(age)
        except (ValueError, TypeError):
            return Response(
                {"error": "Age must be a number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if age <= 0:
            return Response(
                {"error": "Age must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check email
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Invalid email address"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Students.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create student
        student = Students.objects.create(
            name=name,
            email=email,
            age=age,
            course=course,
            teacher=teacher
        )

        return Response(
            {
                "message": "Student created successfully",
                "id": student.id
            },
            status=status.HTTP_201_CREATED
        )


# Get/update/delete student by ID and 
@api_view(["GET", "PUT", "DELETE"])
def student_detail(request, pk):

    try:
        student = Students.objects.get(pk=pk)
    except Students.DoesNotExist:
        return Response(
            {"error": "Student not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        return Response({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "age": student.age,
            "course": student.course,
            "teacher": student.teacher
        }, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        name = request.data.get("name")
        email = request.data.get("email")
        age = request.data.get("age")
        course = request.data.get("course")
        teacher = request.data.get("teacher")

        if not all([name, email, age, course, teacher]):
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            age = int(age)  #Validate age 
        except (ValueError, TypeError):
            return Response(
                {"error": "Age must be a number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if age <= 0:
            return Response(
                {"error": "Age must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)  #Validate email 
        except ValidationError:
            return Response(
                {"error": "Invalid email address"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Students.objects.filter(email=email).exclude(pk=pk).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update student
        student.name = name
        student.email = email
        student.age = age
        student.course = course
        student.teacher = teacher

        student.save()

        return Response(
            {"message": "Student updated successfully"},
            status=status.HTTP_200_OK
        )

    elif request.method == "DELETE":
        student.delete()

        return Response(
            {"message": "Student deleted successfully"},
            status=status.HTTP_200_OK
        )
