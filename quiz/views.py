from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Avg, Count
from .models import Topic, Question, QuizAttempt


def home(request):
    return render(request, "quiz/home.html")


def topics(request):
    search = request.GET.get("search")

    if search:
        topic_list = Topic.objects.filter(name__icontains=search)
    else:
        topic_list = Topic.objects.all()

    paginator = Paginator(topic_list.order_by("id"), 1)
    page_number = request.GET.get("page")
    topics = paginator.get_page(page_number)

    return render(request, "quiz/topics.html", {
        "topics": topics,
        "search": search
    })


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()

    return render(request, "quiz/register.html", {
        "form": form
    })


def quiz_view(request, topic_id):
    questions = Question.objects.filter(topic_id=topic_id)
    topic = Topic.objects.get(id=topic_id)

    if request.method == "POST":
        total = questions.count()
        correct = 0
        wrong = 0
        wrong_questions = []

        for q in questions:
            selected_answer = request.POST.get(f"question_{q.id}")

            if selected_answer and selected_answer.strip().upper() == q.correct_answer.strip().upper():
                correct += 1
            else:
                wrong += 1
                wrong_questions.append({
                    "question": q.text,
                    "selected": selected_answer if selected_answer else "No answer",
                    "correct": q.correct_answer
                })

        score = int((correct / total) * 100) if total > 0 else 0

        if request.user.is_authenticated:
            QuizAttempt.objects.create(
                user=request.user,
                topic=topic,
                total=total,
                correct=correct,
                wrong=wrong,
                score=score
            )

        if correct >= 8:
            message = "You're doing great! 🔥"
            show_package = False
        else:
            message = "You have weaknesses in these topics. We recommend a study package 📚"
            show_package = True

        return render(request, "quiz/result.html", {
            "total": total,
            "correct": correct,
            "wrong": wrong,
            "score": score,
            "message": message,
            "show_package": show_package,
            "topic_id": topic_id,
            "wrong_questions": wrong_questions,
        })

    return render(request, "quiz/quiz.html", {
        "questions": questions,
        "topic": topic
    })


def package_view(request, topic_id):
    return render(request, "quiz/package.html")


def leaderboard_view(request):
    attempts = QuizAttempt.objects.select_related("user", "topic").order_by("-score", "-created_at")

    return render(request, "quiz/leaderboard.html", {
        "attempts": attempts
    })

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    attempts = QuizAttempt.objects.filter(user=request.user).order_by("-created_at")

    total_quizzes = attempts.count()
    average_score = 0

    if total_quizzes > 0:
        average_score = int(sum(a.score for a in attempts) / total_quizzes)

    if average_score >= 80:
        level = "Advanced"
        level_message = "Your level is increasing. Great job! 🚀"
    elif average_score >= 50:
        level = "Intermediate"
        level_message = "You are improving. Keep practicing! 🔥"
    else:
        level = "Beginner"
        level_message = "Your level needs improvement. Keep solving quizzes! 📚"

    return render(request, "quiz/profile.html", {
        "attempts": attempts,
        "total_quizzes": total_quizzes,
        "average_score": average_score,
        "level": level,
        "level_message": level_message,
    })
