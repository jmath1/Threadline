from django import template

register = template.Library()

@register.inclusion_tag('maps/init_map.html')
def init_map(latitude=40.7831, longitude=-73.9712, zoom=13):
    return {'latitude': latitude, 'longitude': longitude, 'zoom': zoom}
