from django.shortcuts import render
from django.http import HttpResponse


def posts_list(request):
    n = ['User1', 'User2']
    return render(request, 'blog/index.html', context={'names': n})
