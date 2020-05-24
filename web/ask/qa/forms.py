from django import forms
from .models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = Question()

    '''
    def __init__(self, q, **kwargs):
        self.question = question
        super(AnswerForm, self).__init__(**kwargs)
    '''

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def clean_question(self):
        question = self.cleaned_data['question']
        return question

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.question = Question.objects.get(id=self.question_id)
        answer.save()
        return answer
