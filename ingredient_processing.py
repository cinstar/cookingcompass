import re

def clean_ingredient_text(raw_text):
    # Lists of words/phrases to remove
    filler_words = {
        'and', 'thinly', 'thickly', 'finely', 'roughly', 'chopped', 'diced', 
        'sliced', 'minced', 'grated', 'fresh', 'large', 'small', 'medium',
        'organic', 'peeled', 'optional', 'divided', 'room temperature', 'to', 'taste'
    }

    measurements = {
        "cups", "cup", "tbsp", "tablespoons", "tablespoon", "tsp", "teaspoons", "teaspoon",
        "oz", "ounces", "ounce", "pounds", "pound", "lbs", "lb", "grams", "gram", "kg", "kilograms", "kilogram",
        "ml", "milliliters", "milliliter", "liters", "liter", "quarts", "quart", "pints", "pint", "gallons", "gallon"
    }

    fractions = {'½', '¼', '¾', '⅓', '⅔', '⅛', '⅜', '⅝', '⅞'}

    descriptors = {
        "chopped", "softened", "or to taste", "or as needed", "divided", "melted", "or more to taste", "juiced", 
        "peeled", "drained", "cored", "minced", "beaten", "sliced", "diced", "pitted", "and sliced", "thawed", 
        "mashed", "halved", "seeded", "skinless", "finely chopped", "lightly beaten", "cut into cubes", 
        "cut into pieces", "crushed", "at room temperature", "zested", "shredded", "coarsely chopped",
        "crumbled", "toasted", "baked", "cut into wedges", "cubed", "hulled", "seeded and minced", "heated"
    }

    exclude = {'and', '', '-', '–', '—'}

    # Normalize and remove numbers, parentheses, and punctuation
    ingredients = raw_text.lower()
    ingredients = re.sub(r'\([^)]*\)', '', ingredients)  # remove text in parentheses
    ingredients = re.sub(r'[\d\/]+', '', ingredients)    # remove numbers and fractions like "1", "1/2"
    ingredients = re.sub(r'[^\w\s,-]', '', ingredients)  # remove special characters except commas and dashes

    # Split into list
    items = re.split(r',', ingredients)

    cleaned = []
    for item in items:
        # Normalize spacing and remove extra dashes
        item = item.strip(" -–—\t\n\r")
        if item in exclude:
            continue
        # Tokenize and remove all filler/measuring/descriptor words
        words = re.split(r'\s+', item)
        filtered = [
            word for word in words 
            if word not in filler_words and word not in measurements and word not in descriptors and word not in exclude and word not in fractions
        ]
        if filtered:
            cleaned.append(' '.join(filtered))

    return cleaned
