class Item:
    def __init__(self, id, name, category, description, damage=0, rarity="Común", subtype=""):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.damage = damage
        self.rarity = rarity
        self.subtype = subtype
    
    def get_rarity_color(self):
        colors = {
            "Común": "#FFFFFF",
            "Poco común": "#1EFF00",
            "Raro": "#0070DD",
            "Épico": "#A335EE",
            "Legendario": "#FF8000"
        }
        return colors.get(self.rarity, "#FFFFFF")

# Lista global para almacenar los ítems (en una app real usarías una base de datos)
items = []