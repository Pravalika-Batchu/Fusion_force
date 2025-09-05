from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('CITIZEN', 'Citizen'),
        ('ADMIN', 'Admin'),
        ('DEPARTMENT_OFFICER', 'Department Officer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

class Issue(models.Model):
    CATEGORY_CHOICES = [
        ('HYGIENE', 'Hygiene & Sanitation'),
        ('ROADS', 'Road & Transport'),
        ('ELECTRICITY', 'Streetlights & Electricity'),
        ('WATER', 'Water Supply & Drainage'),
        ('SAFETY', 'Safety & Emergency Hazards'),
        ('INFRA', 'Public Infrastructure'),
        ('OTHER', 'Other (Unclassified)'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_issues")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="OTHER")
    custom_category = models.CharField(max_length=255, blank=True, null=True)  # For "None of the Above"
    
    photo = models.ImageField(upload_to="issues/photos/", blank=True, null=True)
    video = models.FileField(upload_to="issues/videos/", blank=True, null=True)

    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    resolved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="resolved_issues")
    resolution_description = models.TextField(blank=True, null=True)
    resolution_proof = models.FileField(upload_to="issues/resolution_proofs/", null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    resolver_points_awarded = models.BooleanField(default=False)

    def __str__(self):
        return f"Issue: {self.title} ({self.status})"


class StatusLog(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="status_logs")
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue {self.issue.id} changed from {self.old_status} → {self.new_status}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"
