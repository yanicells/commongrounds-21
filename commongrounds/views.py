import google.generativeai as genai
from django.shortcuts import render
from django.conf import settings
from .ai_utils import get_all_context


def chatbot_view(request):
    output = None
    query = None
    
    if request.method == "POST":
        query = request.POST.get("query")
        
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if api_key and query:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash-lite')
                
                system_context = get_all_context()
                full_prompt = f"{system_context}\n\nUser Question: {query}"
                
                response = model.generate_content(full_prompt)
                output = response.text
            except Exception as e:
                output = f"Error: {str(e)}"
    
    return render(request, 'chatbot.html', {
        'output': output,
        'query': query
    })
