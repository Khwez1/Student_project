from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validat_mark(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                "Mark must be between 0 and 100."
            )
        return value

    def validate(self, data):
        class_group = data.get('class_group')
        mark = data.get('mark')

        if class_group and class_group.name == 'Advanced' and mark < 50:
            raise serializers.ValidationError(
                "Advanced students need a mark of at least 50."
            )
        return data

    def validate_name(self, value):
        if Student.objects.filter(value).exists():
            raise serializers.ValidationError("This name is already taken.")
        return value