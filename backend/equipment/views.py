from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer
import pandas as pd

class UploadCSV(APIView):
    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        
        dataset = EquipmentDataset(name=file.name, csv_file=file)
        dataset.save()

        
        if EquipmentDataset.objects.count() > 5:
            oldest = EquipmentDataset.objects.order_by('uploaded_at').first()
            oldest.delete()

        # Read CSV and compute summary
        df = pd.read_csv(dataset.csv_file.path)
        total_count = len(df)
        avg_flowrate = df['Flowrate'].mean()
        avg_pressure = df['Pressure'].mean()
        avg_temperature = df['Temperature'].mean()
        type_distribution = df['Type'].value_counts().to_dict()

        summary = {
            'total_count': total_count,
            'avg_flowrate': avg_flowrate,
            'avg_pressure': avg_pressure,
            'avg_temperature': avg_temperature,
            'type_distribution': type_distribution
        }

        serializer = EquipmentDatasetSerializer(dataset)
        return Response({'dataset': serializer.data, 'summary': summary})

