from django.shortcuts import render

from blackboard.forms import Answerform

# Create your views here.


def blackboard(request):
    context = {
        'answer_form': Answerform()

    }
    return render(request, 'blackboard.html', context=context)
