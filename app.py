from flask import Flask, render_template, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase    
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)

#Creamos la cadena de conexion 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokedex.sqlite"

#Vinculamos la base de datos con la app
db = SQLAlchemy(app)

#Creamos el modelo
class pokemon(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)
    height: Mapped[float] = mapped_column(db.Float, nullable=False)
    weight: Mapped[float] = mapped_column(db.Float, nullable=False)
    order: Mapped[int] = mapped_column(db.Integer, nullable=False)
    type: Mapped[str] = mapped_column(db.String, nullable=False)


#con esta sentencia se crea las tablas 
with app.app_context():
    db.create_all()


def get_pokemon_data(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r = requests.get(url).json()
    return r 

@app.route("/", methods=['GET', 'POST'])
def home():
    pokemon=None
    if request.method == 'POST':
        name_pokemon = request.form.get('nombre')
        if name_pokemon:
            data = get_pokemon_data(name_pokemon.lower())
            pokemon={
                'id':data.get('id'),
                'name': data.get('name').upper(),
                'height': data.get('height'),
                'weight': data.get('weight'),
                'order': data.get('order'),
                'type': 'Estudiante',
                'hp': data.get('stats')[0].get('base_stat'),
                'attack': data.get('stats')[1].get('base_stat'),
                'defence': data.get('stats')[2].get('base_stat'),
                'speed': data.get('stats')[5].get('base_stat'),
                'photo':data.get('sprites').get('other').get('official-artwork').get('front_default'),
                'photo1':data.get('sprites').get('other').get('dream_world').get('front_default'),
                    }
    return render_template('pokemon.html', pokemon=pokemon)


@app.route("/detalle/<name>/")
def detalle(name):
    data = get_pokemon_data(name.lower())
    pokemon={
        'id':data.get('id'),
        'name': data.get('name').upper(),
        'height': data.get('height'),
        'weight': data.get('weight'),
        'order': data.get('order'),
        'type': 'Estudiante',
        'hp': data.get('stats')[0].get('base_stat'),
        'attack': data.get('stats')[1].get('base_stat'),
        'defence': data.get('stats')[2].get('base_stat'),
        'speed': data.get('stats')[5].get('base_stat'),
        'photo1':data.get('sprites').get('other').get('dream_world').get('front_default'),
        'photo':data.get('sprites').get('other').get('official-artwork').get('front_default')
                    }
    return render_template('detalle.html', pokemon=pokemon)


#pruebas de base de datos 
@app.route("/insert_pokemon/<pokemon>")
def insert_pokemon(pokemon):
    new_pokemon = pokemon
    if new_pokemon:
        obj = pokemon(pokemon)
        db.session.add(obj)
        db.session.commit() 
    return 'Pokemon Agregado'

@app.route("/select")
def select():
    Lista_pokemon = pokemon.query.all()
    for p in Lista_pokemon:
        print(p.name)
    return 'alo'

@app.route("/selectbyname/<name>")
def selectbyname(name):
    poke = pokemon.query.filter_by(name=name).first()
    return str(poke.id)

#Para mostrar 
@app.route("/selectbyid/<id>")
def selectbyid(id):
    poke = pokemon.query.filter_by(id=id).first()
    return str(poke.id) + str(poke.name)

#Eliminar el id de un pokemon 
@app.route("/deletebyid/<id>")
def deletebyid(id):
    pokemon_a_eliminar = pokemon.query.filter_by(id=id).first()
    db.session.delete(pokemon_a_eliminar)
    db.session.commit()
    return 'Pokemon Eliminado'


if __name__ == '__main__':
    app.run(debug=True)