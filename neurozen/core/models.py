from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    COLOR_CHOICES = [
        ('#FFF5E6', 'Warm White - Joy'),
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
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    
    def __str__(self):
        return self.title

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
