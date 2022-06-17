from django.shortcuts import render

# Create your views here.
def index(request):
    text = 'Hello Tailwind'
    context = {
        'context_text': text,
    }
    return render(request, 'mtaaniapp/index.html', context)
