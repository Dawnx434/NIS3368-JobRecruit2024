from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.conf import settings

from UserAuth.models import User
from .models import Topic, Post
from .forms import NewTopicForm

import re
import os


def get_matching_files(request):
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.PROFILE_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.jpeg')
    return matching_files[0]


# Create your views here.
def home(request):

    topics = Topic.objects.all()

    context = {
        'matching_files': get_matching_files(request),
        'topics': topics,
    }
    return render(request, 'Forum/home.html', context)


def new_topic(request):
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.starter = User.objects.get(pk=request.session['UserInfo'].get('id'))
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=topic.starter
            )
            return redirect('Forum:topic_posts', pk=topic.pk)

    else:
        form = NewTopicForm()

    context = {
        'form': form,
        'matching_files': get_matching_files(request),
    }
    return render(request, 'Forum/new_topic.html', context)


def topic_posts(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.views += 1
    topic.save()

    context = {
        'topic': topic,
        'matching_files': get_matching_files(request),
    }

    return render(request, 'Forum/topic_posts.html', context)
