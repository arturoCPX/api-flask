from flask import Flask, request, jsonify
from models import db, Country, Language
from schemas import ma, CountrySchema, LanguageSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///countries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

# Crear la base de datos y agregar datos de ejemplo
@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()
        if Country.query.count() == 0:
            example = Country(name="México", official_name="Estados Unidos Mexicanos", capital="Ciudad de México", region="América", subregion="Latinoamérica")
            db.session.add(example)
            db.session.commit()
        if Language.query.count() == 0:
            db.session.add(Language(language="Español"))
            db.session.commit()

# --- Rutas para Country ---
country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    return jsonify(countries_schema.dump(countries))

@app.route('/countries/<int:id>', methods=['GET'])
def get_country(id):
    country = Country.query.get_or_404(id)
    return jsonify(country_schema.dump(country))

@app.route('/countries', methods=['POST'])
def create_country():
    data = request.get_json()
    errors = country_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    country = Country(**data)
    db.session.add(country)
    db.session.commit()
    return jsonify(country_schema.dump(country)), 201

@app.route('/countries/<int:id>', methods=['PUT'])
def update_country(id):
    country = Country.query.get_or_404(id)
    data = request.get_json()
    errors = country_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(country, key, value)
    db.session.commit()
    return jsonify(country_schema.dump(country))

@app.route('/countries/<int:id>', methods=['DELETE'])
def delete_country(id):
    country = Country.query.get_or_404(id)
    db.session.delete(country)
    db.session.commit()
    return '', 204

# --- Rutas para Language ---
language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)

@app.route('/languages', methods=['GET'])
def get_languages():
    languages = Language.query.all()
    return jsonify(languages_schema.dump(languages))

@app.route('/languages/<int:id>', methods=['GET'])
def get_language(id):
    language = Language.query.get_or_404(id)
    return jsonify(language_schema.dump(language))

@app.route('/languages', methods=['POST'])
def create_language():
    data = request.get_json()
    errors = language_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    language = Language(**data)
    db.session.add(language)
    db.session.commit()
    return jsonify(language_schema.dump(language)), 201

@app.route('/languages/<int:id>', methods=['PUT'])
def update_language(id):
    language = Language.query.get_or_404(id)
    data = request.get_json()
    errors = language_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    language.language = data.get("language", language.language)
    db.session.commit()
    return jsonify(language_schema.dump(language))

@app.route('/languages/<int:id>', methods=['DELETE'])
def delete_language(id):
    language = Language.query.get_or_404(id)
    db.session.delete(language)
    db.session.commit()
    return '', 204

# Ruta de prueba
@app.route('/')
def hello():
    return "<h1>API de Countries y Languages</h1>"

if __name__ == '__main__':
    app.run(debug=True)
