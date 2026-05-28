from django.contrib import admin
from .models import (
    RoadmapStage, RoadmapLesson, RoadmapExercise,
    RoadmapTestCase, RoadmapQuizQuestion,
    RoadmapUserProgress, RoadmapUserXP,
)


class LessonInline(admin.TabularInline):
    model  = RoadmapLesson
    extra  = 1
    fields = ['title', 'status', 'xp_reward', 'order']


class ExerciseInline(admin.TabularInline):
    model  = RoadmapExercise
    extra  = 1
    fields = ['title', 'exercise_type', 'difficulty', 'xp_reward', 'order']


class TestCaseInline(admin.TabularInline):
    model  = RoadmapTestCase
    extra  = 2
    fields = ['description', 'input_data', 'expected', 'is_hidden', 'order']


class QuizQuestionInline(admin.TabularInline):
    model  = RoadmapQuizQuestion
    extra  = 2
    fields = ['question', 'options', 'correct_idx', 'explanation', 'order']


@admin.register(RoadmapStage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'icon']
    inlines      = [LessonInline]


@admin.register(RoadmapLesson)
class LessonAdmin(admin.ModelAdmin):
    list_display  = ['title', 'stage', 'status', 'xp_reward', 'order']
    list_editable = ['status', 'order']
    list_filter   = ['stage', 'status']
    inlines       = [ExerciseInline]


@admin.register(RoadmapExercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'exercise_type', 'difficulty', 'xp_reward']
    list_filter  = ['exercise_type', 'difficulty', 'lesson__stage']

    def get_inlines(self, request, obj=None):
        if obj and obj.exercise_type == 'quiz':
            return [QuizQuestionInline]
        return [TestCaseInline]


@admin.register(RoadmapUserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display    = ['user', 'exercise', 'attempts', 'solved', 'xp_earned']
    list_filter     = ['solved']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RoadmapUserXP)
class UserXPAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_xp', 'streak_days', 'last_active']