from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Topic, Question


def home(request):
    return render(request, "quiz/home.html")


def topics(request):
    search = request.GET.get("search")

    if search:
        topic_list = Topic.objects.filter(name__icontains=search)
    else:
        topic_list = Topic.objects.all()

    paginator = Paginator(topic_list, 1)
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

    if request.method == "POST":
        total = questions.count()
        correct = 0
        wrong = 0

        for q in questions:
            selected_answer = request.POST.get(f"question_{q.id}")

            if selected_answer and selected_answer.strip().upper() == q.correct_answer.strip().upper():
                correct += 1
            else:
                wrong += 1

        score = int((correct / total) * 100) if total > 0 else 0

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
            "topic_id": topic_id
        })

    return render(request, "quiz/quiz.html", {
        "questions": questions
    })


def package_view(request, topic_id):
    return render(request, "quiz/package.html")