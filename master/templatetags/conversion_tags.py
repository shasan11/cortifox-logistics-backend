from django import template
from master.models import UnitofMeasurement, UnitofMeasurementLength

register = template.Library()

@register.simple_tag
def get_conversion_factor(unit_id, unit_type='mass'):
    """
    Template tag to get the conversion factor for a given unit ID.
    
    :param unit_id: The ID of the unit of measurement
    :param unit_type: The type of unit, 'mass' for UnitofMeasurement or 'length' for UnitofMeasurementLength
    :return: The conversion factor based on unit type (mass -> kg, length -> cm)
    """
    if unit_type == 'mass':
        try:
            unit = UnitofMeasurement.objects.get(id=unit_id)
            return unit.conversion_to_kg
        except UnitofMeasurement.DoesNotExist:
            return "Invalid Unit ID"
    elif unit_type == 'length':
        try:
            unit = UnitofMeasurementLength.objects.get(id=unit_id)
            return unit.conversion_to_cm
        except UnitofMeasurementLength.DoesNotExist:
            return "Invalid Unit ID"
    return "Invalid Unit Type"
