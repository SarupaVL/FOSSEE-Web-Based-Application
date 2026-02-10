from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd


@api_view(['GET'])
def test_api(request):
    return Response({"message": "API is working"})


@api_view(['POST'])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response(
            {"error": "No file uploaded"},
            status=400
        )

    csv_file = request.FILES['file']

    try:
        df = pd.read_csv(csv_file)
    except Exception:
        return Response(
            {"error": "Invalid CSV file"},
            status=400
        )

    total_equipment = len(df)

    avg_flowrate = df["Flowrate"].mean()
    avg_pressure = df["Pressure"].mean()
    avg_temperature = df["Temperature"].mean()

    type_distribution = df["Type"].value_counts().to_dict()

    summary = {
        "total_equipment": total_equipment,
        "average_flowrate": avg_flowrate,
        "average_pressure": avg_pressure,
        "average_temperature": avg_temperature,
        "type_distribution": type_distribution
    }

    return Response(summary)
