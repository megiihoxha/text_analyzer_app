import spacy
import requests
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.core.cache import cache

from analyzer.serializer import TextSerializer, UserSerializer, AnalysisLogSerializer
from .models import AnalysisLog

DEEPL_API_KEY = 'e6cf8d9d-44cb-4c3a-be98-351ddfec7422:fx'

class AnalyzeTextView(APIView):
    def post(self, request):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']

            # Load spaCy model
            nlp = spacy.load('es_core_news_sm')
            doc = nlp(text)

            # Part of Speech tagging and additional features
            pos_tags = [(token.text, token.lemma_, token.pos_, token.dep_, str(token.morph)) for token in doc]


            # Translation using DeepL
            translations = []
            for token in doc:
                translation = cache.get(token.text)
                if not translation:
                    response = requests.post(
                        'https://api-free.deepl.com/v2/translate',
                        data={
                            'auth_key': DEEPL_API_KEY,
                            'text': token.text,
                            'source_lang': 'ES',
                            'target_lang': 'EN'
                        }
                    )
                    translation = response.json()['translations'][0]['text']
                    cache.set(token.text, translation, timeout=60*60)  # Cache for 1 hour
                translations.append(translation)

            results = [{
                'word': word,
                'lemma': lemma,
                'pos': pos,
                'dep': dep,
                'morph': morph,
                'translation': translation,
            } for (word, lemma, pos, dep, morph), translation in zip(pos_tags, translations)]


            # Log the analysis result
            AnalysisLog.objects.create(user=request.user, input_text=text, result=results)

            return Response(results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# analyzer/views.py

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class AnalysisLogListView(generics.ListAPIView):
    serializer_class = AnalysisLogSerializer

    def get_queryset(self):
        return AnalysisLog.objects.filter(user=self.request.user)
