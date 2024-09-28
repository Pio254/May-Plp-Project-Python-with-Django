import pandas as pd
print(pd.__version__)

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

def graphs(request):
    return render(request, 'graphs.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'register.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Load data from CSV or Excel
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            messages.error(request, 'Unsupported file type. Please upload a CSV or Excel file.')
            return redirect('upload')
        # Check if required columns exist
        if 'Time' not in df.columns or 'Moisture' not in df.columns:
            messages.error(request, 'The uploaded file must contain "Time" and "Moisture" columns.')
            return redirect('upload')


        # Process the data and store it
        request.session['graph_data'] = {
            'labels': df['Time'].tolist(),  # Replace 'Time' with your column name for x-axis
            'values': df['Moisture'].tolist()  # Replace 'Moisture' with your column name for y-axis
        }

        messages.success(request, 'File uploaded and processed successfully!')
        return redirect('graphs')  # Redirect to the graphs page

    return render(request, 'upload.html')

def get_graph_data(request):
    # Retrieve data from the session
    graph_data = request.session.get('graph_data', {
        'labels': [],
        'values': []
    })
    return JsonResponse(graph_data)
