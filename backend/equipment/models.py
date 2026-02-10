from django.db import models


class UploadSummary(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    total_equipment = models.IntegerField()
    average_flowrate = models.FloatField()
    average_pressure = models.FloatField()
    average_temperature = models.FloatField()

    type_distribution = models.JSONField()

    def __str__(self):
        return f"Upload at {self.created_at}"
