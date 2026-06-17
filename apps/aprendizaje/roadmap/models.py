from django.conf import settings
from django.db import models
import re


class RoadmapStage(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Fácil'),
        ('medium', 'Medio'),
        ('hard', 'Difícil'),
    ]

    title       = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order       = models.PositiveIntegerField(default=0)
    icon        = models.CharField(max_length=10, default='⭐')


    difficulty  = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy'
    )

    class Meta:
        ordering  = ['order']
        app_label = 'roadmap'

    def __str__(self):
        return f'{self.order}. {self.title}'


class RoadmapLesson(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Fácil'),
        ('medium', 'Medio'),
        ('hard', 'Difícil'),
    ]

    STATUS_CHOICES = [
        ('locked',    'Bloqueado'),
        ('available', 'Disponible'),
        ('completed', 'Completado'),
    ]
    stage     = models.ForeignKey(RoadmapStage, on_delete=models.CASCADE, related_name='lessons')
    title     = models.CharField(max_length=100)
    order     = models.PositiveIntegerField(default=0)
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='locked')
    xp_reward = models.PositiveIntegerField(default=10)

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy'
    )

    class Meta:
        ordering  = ['order']
        app_label = 'roadmap'

    def __str__(self):
        return f'{self.stage.title} → {self.title}'
  

class RoadmapExercise(models.Model):
    TYPE_CHOICES = [
        ('code', 'Código Python'),
        ('fill', 'Completar blancos'),
        ('quiz', 'Opción múltiple'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy',   'Fácil'),
        ('medium', 'Medio'),
        ('hard',   'Difícil'),
    ]

    lesson          = models.ForeignKey(RoadmapLesson, on_delete=models.CASCADE, related_name='exercises')
    title           = models.CharField(max_length=200)
    description     = models.TextField()
    hint            = models.TextField(blank=True)
    exercise_type   = models.CharField(max_length=10, choices=TYPE_CHOICES, default='code')
    starter_code    = models.TextField(default='# Escribe tu solución aquí\n', blank=True)
    fill_template   = models.TextField(blank=True)
    fill_answers    = models.TextField(blank=True, help_text='Separadas por |')
    time_limit_secs = models.PositiveIntegerField(default=300)
    max_attempts    = models.PositiveIntegerField(default=3)
    xp_reward       = models.PositiveIntegerField(default=25)
    difficulty      = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    order           = models.PositiveIntegerField(default=0)

    class Meta:
        ordering  = ['order']
        app_label = 'roadmap'

    def get_fill_answers_list(self):
        return [a.strip() for a in self.fill_answers.split('|')] if self.fill_answers else []

    def get_fill_parts(self):
        if not self.fill_template:
            return []
        parts   = re.split(r'(___)', self.fill_template)
        result  = []
        blank_i = 0
        for part in parts:
            if part == '___':
                result.append({'type': 'blank', 'index': blank_i})
                blank_i += 1
            else:
                result.append({'type': 'text', 'content': part})
        return result

    def count_blanks(self):
        return self.fill_template.count('___') if self.fill_template else 0

    def __str__(self):
        return f'[{self.get_exercise_type_display()}] {self.title}'


class RoadmapQuizQuestion(models.Model):
    exercise    = models.ForeignKey(RoadmapExercise, on_delete=models.CASCADE, related_name='quiz_questions')
    question    = models.TextField()
    options     = models.TextField(help_text='Separadas por |')
    correct_idx = models.PositiveIntegerField()
    explanation = models.TextField(blank=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering  = ['order']
        app_label = 'roadmap'

    def get_options_list(self):
        return [o.strip() for o in self.options.split('|')]

    def __str__(self):
        return f'{self.exercise.title} — Q{self.order + 1}'


class RoadmapTestCase(models.Model):
    exercise    = models.ForeignKey(RoadmapExercise, on_delete=models.CASCADE, related_name='test_cases')
    description = models.CharField(max_length=200)
    input_data  = models.TextField()
    expected    = models.TextField()
    is_hidden   = models.BooleanField(default=False)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering  = ['order']
        app_label = 'roadmap'

    def __str__(self):
        return self.description


class RoadmapUserProgress(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise   = models.ForeignKey(RoadmapExercise, on_delete=models.CASCADE)
    attempts   = models.PositiveIntegerField(default=0)
    solved     = models.BooleanField(default=False)
    xp_earned  = models.PositiveIntegerField(default=0)
    time_spent = models.PositiveIntegerField(default=0)
    last_code  = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'exercise')
        app_label       = 'roadmap'

    def __str__(self):
        return f'{self.user} — {self.exercise.title}'


class RoadmapUserXP(models.Model):
    user        = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='roadmap_xp',
    )
    total_xp    = models.PositiveIntegerField(default=0)
    streak_days = models.PositiveIntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    class Meta:
        app_label = 'roadmap'

    def __str__(self):
        return f'{self.user} — {self.total_xp} XP'
    

#from django.db import models
#from django.contrib.auth.models import User

class RoadmapLessonProgress(models.Model):

    STATUS_CHOICES = [
        ('locked',    'Bloqueado'),
        ('available', 'Disponible'),
        ('completed', 'Completado'),
    ]    

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )    

    lesson = models.ForeignKey(
        'RoadmapLesson',
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='locked'
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        unique_together = (
            'user',
            'lesson'
        )