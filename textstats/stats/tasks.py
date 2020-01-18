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

from __future__ import absolute_import, unicode_literals
from collections import defaultdict
import json
from celery import shared_task
from janome import tokenizer
import pandas as pd
from . import models


@shared_task
def count_nouns(id, text, min_length, top_k):
    tt = models.Text.objects.get(id=id)
    tt.status = 'ANALYZING'
    tt.save()
    d = defaultdict(lambda: 0)
    t = tokenizer.Tokenizer()
    for token in t.tokenize(text):
        part_of_speech = token.part_of_speech.split(',')
        if part_of_speech[0] != '名詞' or part_of_speech[1] != '一般' or len(token.base_form) < min_length:
            continue
        d[token.base_form] += 1
    dd = pd.Series(d).sort_values(ascending=False)[:top_k]
    tt.nouns = json.dumps(dd.to_dict())
    tt.status = 'COMPLETED'
    tt.save()
