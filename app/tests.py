from django.test import TestCase

# Create your tests here.

from django.shortcuts import HttpResponse

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World"