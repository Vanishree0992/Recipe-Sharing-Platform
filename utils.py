def convert_measure(amount, from_unit, to_unit):
    factors = {
        ('g','oz'): 0.0353, ('oz','g'): 28.3495,
        ('g','cup'): 0.004226, ('cup','g'): 236.588
    }
    return amount * factors.get((from_unit, to_unit), 1)

def estimate_nutrition(ingredients):
    # sum calories estimate for each ingredient via static lookup or API
    total = sum(item.get('calories',0) for item in ingredients)
    return {'calories': total}
