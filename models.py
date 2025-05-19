from flask_sqlalchemy import SQLAlchemy

#Inicializamos SQLAlchemy
db = SQLAlchemy()

#Cracion del modelo con sus respectivos atos
class Country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    official_name = db.Column(db.String(150), nullable=True)
    capital = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(50), nullable=True)
    subregion = db.Column(db.String(50), nullable=True)

    #Devolver los datos en json y no objeto
    def to_dict(self):
        return {
            "country_id": self.country_id,
            "name": self.name,
            "official_name": self.official_name,
            "capital": self.capital,
            "region": self.region,
            "subregion": self.subregion
        }

class Language(db.Model):
    language_id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "language_id": self.language_id,
            "language": self.language
        }
