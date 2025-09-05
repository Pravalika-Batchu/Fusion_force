from rest_framework import serializers
from .models import Issue, Department, User


class IssueSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    resolution_proof_url = serializers.SerializerMethodField()
    citizen_username = serializers.CharField(source='citizen.username', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None

    def get_resolution_proof_url(self, obj):
        request = self.context.get('request')
        if obj.resolution_proof and request:
            return request.build_absolute_uri(obj.resolution_proof.url)
        return None

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['citizen', 'status', 'resolved_by', 'resolved_at', 'is_approved']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'department_name']
