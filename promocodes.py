PROMO_CODES = {
    "PROMO2024": 0.05,
    "BONUS2024": 0.10,
}

def validate_promo_code(promo_code):
    return PROMO_CODES.get(promo_code.upper())