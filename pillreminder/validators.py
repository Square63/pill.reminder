from django.core.exceptions import ValidationError

def validate_dosage(value):
    if value not in range(1, 1000):
        raise ValidationError('Dosage must be in between 1 to 1000', params={'value': value})
