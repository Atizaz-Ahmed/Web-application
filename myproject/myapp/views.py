from django.shortcuts import render, redirect
from .models import login_info, Question, Results
from myapp.services.config import QuizConfig
from myapp.services.scoring_strategies import StandardScoring
from myapp.services.observers import EmailNotifier, Logger
from myapp.services.event_manager import QuizEventManager


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return render(request, 'myapp/login.html', {'error': 'Both fields are required.'})

        config = QuizConfig()
        config.load()

        user = login_info.objects.filter(username=username, password=password).first()

        if user:
            if not config.allow_retake and user.attempts >= config.max_attempts:
                return render(request, 'myapp/login.html', {
                    'error': f"You have reached the maximum number of attempts ({config.max_attempts})."
                })

            user.attempts += 1
            user.save()
        else:
            # First-time user
            login_info.objects.create(username=username, password=password, attempts=1)


        return redirect(f'/index/?username={username}&password={password}')

    return render(request, 'myapp/login.html')



def register_view(request):
    return render(request, 'myapp/register.html')


def index(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    if not username or not password:
        return redirect('login')

    config = QuizConfig()
    config.load()

    user = login_info.objects.filter(username=username, password=password).first()
    if not user:
        return redirect('login')

    # If user already reached max attempts, do NOT increment attempts, just show message
    if not config.allow_retake and user.attempts >= config.max_attempts:
        return render(request, 'myapp/attempts_finished.html', {
            'message': "Your attempts are finished. You cannot retake the quiz.",
            'username': username,
            'password': password,
        })

    # If attempts are still available, increment attempts
    if user.attempts < config.max_attempts:
        user.attempts += 1
        user.save()

    questions = Question.objects.all()
    for q in questions:
        if isinstance(q.options, str):
            q.options = q.options.split(',')

    context = {
    'questions': questions,
    'username': username,
    'password': password,
    'attempts': user.attempts,
    'max_attempts': config.max_attempts,
    }

    return render(request, 'myapp/index.html', context)

def result(request):
    if request.method != 'POST':
        return redirect('login')

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        return redirect('login')

    questions = Question.objects.all()

    # Strategy Pattern: use scoring strategy
    strategy = StandardScoring()
    score = strategy.calculate_score(questions, request.POST)

    # Build detailed results
    detailed_results = []
    for question in questions:
        selected = request.POST.get(f'question_{question.id}')
        is_correct = selected == question.correct_option
        detailed_results.append({
            'question_text': question.question_text,
            'selected_option': selected,
            'correct_option': question.correct_option,
            'is_correct': is_correct,
        })

    # Save result
    Results.objects.create(username=username, password=password, result=score)

    # Observer Pattern: notify services after quiz completion
    manager = QuizEventManager()
    logger = Logger()         # create logger instance
    manager.subscribe(logger) # subscribe logger
    manager.notify(username, score)

    total = questions.count()
    message = f"You scored {score} out of {total}."

    return render(request, 'myapp/result.html', {
        'score': score,
        'total': total,
        'message': message,
        'detailed_results': detailed_results,
        'username': username,
        'password': password,
        'log_message': logger.message,  # now logger.message is defined
    })

