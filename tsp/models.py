from django.db import models
from django.core.exceptions import ValidationError

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    x_coord = models.FloatField(help_text="X coordinate for visualization")
    y_coord = models.FloatField(help_text="Y coordinate for visualization")
    
    def __str__(self):
        return self.name
    
    def clean(self):
        # Validate that coordinates are within reasonable bounds
        if abs(self.x_coord) > 1000 or abs(self.y_coord) > 1000:
            raise ValidationError("Coordinates must be between -1000 and 1000")
    
    class Meta:
        verbose_name_plural = "Cities"

class Distance(models.Model):
    city1 = models.ForeignKey(City, on_delete=models.CASCADE, related_name='distances_from')
    city2 = models.ForeignKey(City, on_delete=models.CASCADE, related_name='distances_to')
    distance = models.FloatField(help_text="Distance between cities")
    
    def clean(self):
        # Validate that distance is positive and reasonable
        if self.distance <= 0:
            raise ValidationError("Distance must be positive")
        if self.distance > 10000:  # Arbitrary large value
            raise ValidationError("Distance seems unreasonably large")
        
        # Validate that cities are different
        if self.city1 == self.city2:
            raise ValidationError("Cannot set distance from a city to itself")
        
        # Check if reverse distance exists and matches
        reverse_distance = Distance.objects.filter(city1=self.city2, city2=self.city1).first()
        if reverse_distance and reverse_distance.distance != self.distance:
            raise ValidationError("Distance must be the same in both directions")
        
        # Check if this distance already exists
        existing = Distance.objects.filter(city1=self.city1, city2=self.city2).first()
        if existing and existing.id != self.id:  # Allow updating existing distance
            raise ValidationError("Distance between these cities already exists")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
        # Ensure symmetric distance exists
        reverse_distance, created = Distance.objects.get_or_create(
            city1=self.city2,
            city2=self.city1,
            defaults={'distance': self.distance}
        )
        if not created and reverse_distance.distance != self.distance:
            reverse_distance.distance = self.distance
            reverse_distance.save()
    
    class Meta:
        unique_together = ['city1', 'city2']
        verbose_name_plural = "Distances"
        ordering = ['city1__name', 'city2__name']  # Order by city names
    
    def __str__(self):
        return f"{self.city1.name} to {self.city2.name}: {self.distance}"
