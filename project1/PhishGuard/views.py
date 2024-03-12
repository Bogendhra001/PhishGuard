

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from extraction import main  # Correct import statement
import json
import pandas as pd



def index(request):
    return render(request, 'index.html')


def classify(request, dynamic_string):
    # calling the function to get the result of classification
    result = main(dynamic_string)
    phishing=result[0]
    phishing_dict = phishing.to_dict(orient='records')
    # result_json = json.dumps(phishing.values.tolist()) # instood of ndarray we passed direct string value no need for convertion
    return JsonResponse({"result": result[1],"features":phishing_dict})
