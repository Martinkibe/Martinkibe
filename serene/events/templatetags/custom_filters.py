from django import template

register = template.Library()

@register.filter
def format_duration(value):
    try:
        # Convert datetime.timedelta to seconds
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        formatted_duration = f"{int(hours)}hrs {int(minutes)}min"
        return formatted_duration
    except (ValueError, TypeError):
        return value  # Return the original value if it cannot be converted

@register.filter
def instanceof(obj, class_name):
    return obj.__class__.__name__ == class_name

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})