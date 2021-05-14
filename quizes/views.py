from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Questao, Resposta
from results.models import Resultado

class QuizListView(ListView):
    model = Quiz
    template_name= "quiz/main.html"

def quiz_view(request, pk) :
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quiz/quiz.html', {'obj':quiz})

def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers  = []
        for a in q.get_answers():
            answers.append(a.texto)
        questions.append({str(q): answers})        
    return JsonResponse({
        'data': questions,
        'time': quiz.tempo,
    })

def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data=request.POST
        data_ = dict(data.lists())        
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Questao.objects.get(texto=k)
            questions.append(question)
        print (questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.numero_questoes
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.texto)
            if a_selected != "" :
                question_answers = Resposta.objects.filter(questao=q)
                
                for a in question_answers:
                    if a_selected == a.texto :
                        if a.correto :
                            score += 1
                            correct_answer = a.texto
                    else :
                        if a.correto:
                            correct_answer = a.texto

                results.append({str(q):{'correct_answer': correct_answer, 'answered': a_selected}})

            else :
                results.append({str(q):'not answered'})
        score_ = score * multiplier
        Resultado.objects.create(quiz=quiz, user=user, resultado= score_)

        if score_ >= quiz.porcentagem_necessaria :
            return JsonResponse({'passed': True, 'score' : score_, 'results' : results})
        else :            
            return JsonResponse({'passed': False, 'score' : score_, 'results' : results})     
             
