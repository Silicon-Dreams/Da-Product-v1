from django import template

register = template.Library()

@register.filter
def stars(value):
    full_stars = int(value)
    half_stars = int(round(value - full_stars))
    empty_stars = 5 - full_stars - half_stars
    return '★' * full_stars + '☆' * half_stars + ' ' * empty_stars


@register.filter
def float(value):
    return float(value)

@register.filter
def average_rating(reviews):
    ratings = [review.rating for review in reviews]
    if len(ratings) > 0:
        return sum(ratings) / len(ratings)
    else:
        return 0