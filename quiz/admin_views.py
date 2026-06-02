from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import Topic, Question, QuizResult, QuizAttempt


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

admin_required = user_passes_test(is_admin, login_url='/login/')


@login_required
@admin_required
def admin_dashboard(request):
    total_users   = User.objects.count()
    total_topics  = Topic.objects.count()
    total_quizzes = QuizResult.objects.count()
    avg_score     = QuizResult.objects.aggregate(avg=Avg('score'))['avg'] or 0

    today = timezone.now().date()
    days_tr = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
    weekly_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = QuizResult.objects.filter(date__date=day).count()
        weekly_data.append({'label': days_tr[day.weekday()], 'count': count})

    max_count = max((d['count'] for d in weekly_data), default=1) or 1
    recent_users   = User.objects.order_by('-date_joined')[:5]
    recent_quizzes = QuizResult.objects.select_related('user', 'topic').order_by('-date')[:5]

    context = {
        'total_users':    total_users,
        'active_topics':  total_topics,
        'total_quizzes':  total_quizzes,
        'avg_score':      round(avg_score, 1),
        'weekly_data':    weekly_data,
        'max_count':      max_count,
        'recent_users':   recent_users,
        'recent_quizzes': recent_quizzes,
    }
    return render(request, 'quiz/admin_dashboard.html', context)


@login_required
@admin_required
def admin_users(request):
    q        = request.GET.get('q', '')
    role     = request.GET.get('role', '')
    users_qs = User.objects.annotate(quiz_count=Count('quizresult')).order_by('-date_joined')

    if q:
        users_qs = users_qs.filter(Q(username__icontains=q) | Q(email__icontains=q))
    if role == 'admin':
        users_qs = users_qs.filter(is_staff=True)
    elif role == 'user':
        users_qs = users_qs.filter(is_staff=False)

    return render(request, 'quiz/admin_users.html', {'users': users_qs, 'q': q, 'role': role})


@login_required
@admin_required
def admin_user_toggle(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        if user != request.user:
            user.is_active = not user.is_active
            user.save()
            status = 'aktif' if user.is_active else 'pasif'
            messages.success(request, f'{user.username} {status} yapıldı.')
    return redirect('admin_users')


@login_required
@admin_required
def admin_user_delete(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        if user != request.user:
            username = user.username
            user.delete()
            messages.success(request, f'{username} silindi.')
    return redirect('admin_users')


@login_required
@admin_required
def admin_user_make_staff(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.is_staff = not user.is_staff
        user.save()
        role = 'admin' if user.is_staff else 'kullanıcı'
        messages.success(request, f'{user.username} artık {role}.')
    return redirect('admin_users')


@login_required
@admin_required
def admin_content(request):
    topics = Topic.objects.annotate(question_count=Count('question')).order_by('id')
    return render(request, 'quiz/admin_content.html', {'topics': topics})


@login_required
@admin_required
def admin_topic_toggle(request, topic_id):
    return redirect('admin_content')


@login_required
@admin_required
def admin_topic_delete(request, topic_id):
    if request.method == 'POST':
        topic = get_object_or_404(Topic, pk=topic_id)
        topic.delete()
        messages.success(request, f'"{topic.name}" silindi.')
    return redirect('admin_content')

