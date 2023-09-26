# example/views.py
from datetime import datetime

from django.http import HttpResponse


def index(request):
    now = datetime.now()
    html = f"""
    <html>
        <body>
            <h1>Neobak API</h1>
            <p><a href="https://neobank-delta.vercel.app/redoc/">Neobank API</a></p>
            <p>The current time is { now }.</p>
        </body>
    </html>
    """
    return HttpResponse(html)
