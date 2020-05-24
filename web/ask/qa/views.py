from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect

from .forms import AskForm, AnswerForm
from .models import Question, Answer


def test(request, *args, **kwargs):
    tmpl = "<p>%s</p>"
    resp = "<h3>request.path</h3>" + tmpl % request.path

    resp += "<h3>Http GET parameters (query string)</h3>"
    get = request.GET
    for key in get:
        resp += tmpl % (key + ": " + str(get.getlist(key)))

    resp += "<h3>request.META</h3>"
    meta = request.META
    for key in meta:
        resp += tmpl % (key + ': ' + str(meta[key]))
    return HttpResponse("<html><body><h1>view.test</h1>%s</body></html>" % resp)


def questions_paginator(request, paginator_type):
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:  # 'page' is not a number
        raise Http404

    if paginator_type == 'default':
        questions = Question.objects.new()
        paginator_url = "/?page="
    elif paginator_type == 'popular':
        questions = Question.objects.popular()
        paginator_url = "/popular/?page="
    else:
        return HttpResponseServerError

    limit = 10
    paginator = Paginator(questions, limit)
    paginator.url = paginator_url
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'questions_paginator.html', {
        'paginator': paginator,
        'paginator_type': paginator_type,
        'page': page,
        'questions_list': page.object_list,
    })


def question_page(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        new_answer_form = AnswerForm(request.POST)
        if new_answer_form.is_valid():
            new_answer_form.save()
            return HttpResponseRedirect(question.get_url())
    else:
        new_answer_form = AnswerForm(initial={"question": question.id})

    answers = Answer.objects.filter(question_id=question_id)

    return render(request, 'question.html', {
        'question': question,
        'answers': answers,
        'new_answer_form': new_answer_form,
    })


def add_question(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(question.get_url())

    else:
        form = AskForm()

    return render(request, 'ask_question.html', {'form': form})
