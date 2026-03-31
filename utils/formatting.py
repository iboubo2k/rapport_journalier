from datetime import date, datetime

def format_montant(value):
    if value is None:
        return ""
    return f"{int(round(float(value))):,}".replace(",", " ") + " FCFA"

def format_quantite(value):
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.1f}".replace(".", ",")
    return f"{int(round(value)):,}".replace(",", " ")

def format_taux(value):
    if value is None:
        return ""
    return f"{float(value):.1f}".replace(".", ",") + " %"

def format_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime("%d-%m-%Y")
    return ""

def format_field_name(name: str) -> str:
    return name.replace("_", " ").title()
