from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    COLOR_CHOICES = [
        ('#FFF5E6', 'Warm White - Neutral'),
        ('#F5F5F5', 'Off White - Work'),
        ('#FFE4E1', 'Misty Rose - Health'),
        ('#FFDAB9', 'Peach - Learning'),
        ('#F44336', 'Red - Urgent'),
        ('#E0E0E0', 'Gray - Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#FFF5E6')
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

class Tag(models.Model):
    TAG_COLOR_CHOICES = [
        ('#FFF5E6', 'Warm White'),
        ('#F5F5F5', 'Off White'),
        ('#FFE4E1', 'Misty Rose'),
        ('#FFDAB9', 'Peach'),
        ('#E0E0E0', 'Gray'),
        ('#F44336', 'Red'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, choices=TAG_COLOR_CHOICES, default='#FFF5E6')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_time = models.IntegerField(help_text="Estimated time in minutes", null=True, blank=True)
    is_break_task = models.BooleanField(default=False, help_text="Is this a break task?")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    recurring = models.BooleanField(default=False, help_text="Is this a recurring task?")
    recurrence_pattern = models.CharField(max_length=100, blank=True, help_text="Recurrence pattern (e.g., 'daily', 'weekly', 'monthly')")
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    color = models.CharField(max_length=7, default='#FFFFFF', help_text="Hex color code")

    def __str__(self):
        return self.title

class PomodoroSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes", default=25)
    is_completed = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Pomodoro Session - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    points_required = models.IntegerField(default=0)
    is_claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DailyQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=200, blank=True)
    date = models.DateField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Quote for {self.date}"

class BreathingExercise(models.Model):
    DIFFICULTY_CHOICES = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    steps = models.TextField(help_text="Step by step instructions")
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES, default='E')
    image_url = models.URLField(blank=True, help_text="URL to exercise image or video")
    

    def __str__(self):
        return self.name

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('1', '😊 Very Happy'),
        ('2', '🙂 Happy'),
        ('3', '😐 Neutral'),
        ('4', '😕 Sad'),
        ('5', '😢 Very Sad'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    mood = models.CharField(max_length=1, choices=MOOD_CHOICES)
    notes = models.TextField(blank=True, help_text="What influenced your mood today?")
    energy_level = models.IntegerField(
        help_text="Energy level from 1-10",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    sleep_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text="Hours of sleep last night",
        null=True,
        blank=True
    )
    activities = models.TextField(
        blank=True,
        help_text="Activities that might have affected your mood"
    )

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s mood on {self.date}: {self.get_mood_display()}"
