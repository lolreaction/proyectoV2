from flask import Flask, render_template, request, redirect, url_for
from models import Item, items

app = Flask(__name__)

# Datos de ejemplo para ítems de Necesse
def init_sample_data():
    if not items:
        sample_items = [
            Item(1, "Espada de Hierro", "Arma", "Una espada forjada en hierro", 25, "Común", "combate"),
            Item(2, "Arco Largo", "Arma", "Arco de largo alcance", 18, "Poco común", "distancia"),
            Item(3, "Poción de Vida", "Consumible", "Restaura 50 puntos de vida", 5, "Común", "curación"),
            Item(4, "Armadura de Cuero", "Armadura", "Armadura ligera de cuero", 15, "Común", "defensa"),
            Item(5, "Pico de Hierro", "Herramienta", "Para minar minerales", 12, "Común", "minería"),
            Item(6, "Hacha de Acero", "Herramienta", "Para talar árboles", 20, "Poco común", "tala"),
            Item(7, "Anillo de Fuerza", "Accesorio", "Aumenta el daño físico", 45, "Raro", "mejora"),
            Item(8, "Gema de Relámpago", "Material", "Material para encantar armas", 30, "Poco común", "encantamiento")
        ]
        items.extend(sample_items)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items')
def list_items():
    category = request.args.get('category')
    rarity = request.args.get('rarity')
    
    filtered_items = items
    
    if category and category != 'all':
        filtered_items = [item for item in filtered_items if item.category.lower() == category.lower()]
    
    if rarity and rarity != 'all':
        filtered_items = [item for item in filtered_items if item.rarity.lower() == rarity.lower()]
    
    categories = list(set(item.category for item in items))
    rarities = list(set(item.rarity for item in items))
    
    return render_template('items.html', 
                         items=filtered_items, 
                         categories=categories, 
                         rarities=rarities,
                         selected_category=category,
                         selected_rarity=rarity)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = next((item for item in items if item.id == item_id), None)
    if item:
        return render_template('item_detail.html', item=item)
    return "Ítem no encontrado", 404

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        new_id = max([item.id for item in items]) + 1 if items else 1
        new_item = Item(
            id=new_id,
            name=request.form['name'],
            category=request.form['category'],
            description=request.form['description'],
            damage=int(request.form.get('damage', 0)),
            rarity=request.form['rarity'],
            subtype=request.form['subtype']
        )
        items.append(new_item)
        return redirect(url_for('list_items'))
    
    return render_template('add_item.html')

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = next((item for item in items if item.id == item_id), None)
    if not item:
        return "Ítem no encontrado", 404
    
    if request.method == 'POST':
        item.name = request.form['name']
        item.category = request.form['category']
        item.description = request.form['description']
        item.damage = int(request.form.get('damage', 0))
        item.rarity = request.form['rarity']
        item.subtype = request.form['subtype']
        return redirect(url_for('item_detail', item_id=item_id))
    
    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    global items
    items = [item for item in items if item.id != item_id]
    return redirect(url_for('list_items'))

if __name__ == '__main__':
    init_sample_data()
    app.run(debug=True)