

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from extraction import main  # Correct import statement
import json


def index(request):
    return render(request, 'index.html')


def classify(request, dynamic_string):
    # calling the function to get the result of classification
    result = main(dynamic_string)
    # result_json = json.dumps(result.tolist())     # instood of ndarray we passed direct string value no need for convertion
    return JsonResponse({"result": result})
