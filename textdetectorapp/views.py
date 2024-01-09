from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
import transformers
from pathlib import Path

class Detector(View):
    def get(self, request):
        return render(request, 'textdetectorapp/detector.html')
    
class DetectorAPI(APIView):
    def get(self, request):
        return Response()
    def post(self, request):
        text = request.data['content']
        method = request.data['method']

        # some parameters
        DEVICE = "cpu"
        path = Path.cwd()
        model = path/'textdetectorapp'/'update_results'/'gpt2-medium-t5-base'/'Essay-ChatGPT'/method
        print(model)
        num_labels = 2
        pos_bit = 1

        # load model
        detector = transformers.AutoModelForSequenceClassification.from_pretrained(
            model,
            num_labels=num_labels,
            ignore_mismatched_sizes=True
        ).to(DEVICE)

        # load tokenizer
        tokenizer = transformers.AutoTokenizer.from_pretrained(model)

        # tokenize provided text
        encoded_text = tokenizer(
            [text], 
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        ).to(DEVICE)

        # make prediction => output is the probability that the provided text is generated by ChatGPT
        predictions = detector(**encoded_text).logits.softmax(-1)[:, pos_bit].tolist()
        print(predictions)
        return Response(predictions)