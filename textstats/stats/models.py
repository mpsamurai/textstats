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

from django.shortcuts import reverse
from django.db import models


# Create your models here.
class Text(models.Model):
    body = models.TextField()
    nouns = models.TextField(null=True, blank=True)

    STATUS_CHOICES = (('UPLOADED', 'アップロード完了'),
                      ('ANALYZING', '分析中'),
                      ('COMPLETED', '分析完了'),)
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default='UPLOADED')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created', )

    def get_absolute_url(self):
        return reverse('stats:detail', args=(self.id, ))

    def __str__(self):
        return self.body[:20]