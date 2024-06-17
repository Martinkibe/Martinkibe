from django import template

register = template.Library()

@register.filter
def format_duration(value):
    try:
        # Convert datetime.timedelta to seconds
        total_seconds = value.total_seconds()
        hours, seconds = divmod(total_seconds, 3600)
        minutes = seconds // 60
        formatted_duration = f"{int(hours)}h {int(minutes)}m"
        return formatted_duration
    except (ValueError, TypeError):
        return value  # Return the original value if it cannot be converted

@register.filter
def instanceof(obj, class_name):
    return obj.__class__.__name__ == class_name