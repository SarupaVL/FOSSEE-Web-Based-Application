from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import pandas as pd
from .models import UploadSummary
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_api(request):
    return Response({"message": "API is working"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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

    # Save to database
    UploadSummary.objects.create(
        total_equipment=total_equipment,
        average_flowrate=avg_flowrate,
        average_pressure=avg_pressure,
        average_temperature=avg_temperature,
        type_distribution=type_distribution
    )

    # Keep only last 5 uploads
    if UploadSummary.objects.count() > 5:
        oldest = UploadSummary.objects.order_by('created_at').first()
        oldest.delete()

    return Response(summary)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upload_history(request):
    uploads = UploadSummary.objects.order_by('-created_at')[:5]

    data = []
    for upload in uploads:
        data.append({
            "id": upload.id,
            "created_at": upload.created_at,
            "total_equipment": upload.total_equipment,
            "average_flowrate": upload.average_flowrate,
            "average_pressure": upload.average_pressure,
            "average_temperature": upload.average_temperature,
            "type_distribution": upload.type_distribution,
        })

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_report(request, upload_id):
    try:
        upload = UploadSummary.objects.get(id=upload_id)
    except UploadSummary.DoesNotExist:
        return Response({"error": "Upload not found"}, status=404)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Equipment Report - Upload ID {upload.id}")
    
    # Metadata
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Date: {upload.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    # Summary Statistics
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 120, "Summary Statistics")
    
    p.setFont("Helvetica", 12)
    y = height - 150
    p.drawString(50, y, f"Total Equipment: {upload.total_equipment}")
    p.drawString(50, y - 20, f"Average Flowrate: {upload.average_flowrate:.2f}")
    p.drawString(50, y - 40, f"Average Pressure: {upload.average_pressure:.2f}")
    p.drawString(50, y - 60, f"Average Temperature: {upload.average_temperature:.2f}")

    # Type Distribution
    p.setFont("Helvetica-Bold", 14)
    y -= 100
    p.drawString(50, y, "Equipment Type Distribution")
    
    p.setFont("Helvetica", 12)
    y -= 30
    for type_name, count in upload.type_distribution.items():
        p.drawString(50, y, f"{type_name}: {count}")
        y -= 20

    p.showPage()
    p.save()
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"report_{upload.id}.pdf")
