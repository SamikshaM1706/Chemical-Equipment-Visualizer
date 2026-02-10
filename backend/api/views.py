from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd

@api_view(['POST'])
def upload_csv(request):
    csv_file = request.FILES.get('file')
    if not csv_file:
        return Response({"error": "No file uploaded"}, status=400)

    df = pd.read_csv(csv_file)

    total_count = len(df)
    avg_flowrate = df['Flowrate'].mean()
    avg_pressure = df['Pressure'].mean()
    avg_temperature = df['Temperature'].mean()
    type_distribution = df['Type'].value_counts().to_dict()

    summary = {
        "total_count": total_count,
        "avg_flowrate": avg_flowrate,
        "avg_pressure": avg_pressure,
        "avg_temperature": avg_temperature,
        "type_distribution": type_distribution
    }

    return Response({"summary": summary})
