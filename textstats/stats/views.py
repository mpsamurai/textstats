#  MIT License
#
#  Copyright (c) 2020. Morning Project Samurai Inc. (MPS)
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import json
from django.shortcuts import render, redirect
from django import views
from django.core.paginator import Paginator
from . import forms
from . import models
from . import tasks


# Create your views here.
class ListView(views.View):
    def get(self, request):
        paginator = Paginator(models.Text.objects.all(), 10)
        page_obj = paginator.get_page(request.GET.get('p', 1))
        return render(request, 'stats/list.html', {'texts': page_obj})


class DetailView(views.View):
    def get(self, request, id):
        text = models.Text.objects.get(id=id)
        if text.nouns:
            nouns = json.loads(text.nouns)
            max_count = max(nouns.values())
            graph = {k: {'count': v, 'bar': '#' * (int(v * 50 / max_count) + 1)} for k, v in nouns.items()}
        else:
            graph = {}
        return render(request, 'stats/detail.html', {'text': text, 'graph': graph})


class UploadView(views.View):
    def get(self, request):
        form = forms.UploadForm()
        return render(request, 'stats/upload.html', {'form': form})

    def post(self, request):
        form = forms.UploadForm(request.POST)
        if not form.is_valid():
            return render(request, 'stats/upload.html', {'form': form})
        form.save()
        tasks.count_nouns.delay(form.instance.id, form.instance.body,
                                form.cleaned_data['min_length'], form.cleaned_data['top_k'])
        return redirect('stats:list')
