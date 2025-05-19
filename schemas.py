from flask_marshmallow import Marshmallow
from marshmallow import validate
from models import Country, Language

ma = Marshmallow()

class CountrySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Country

    country_id = ma.auto_field()
    name = ma.auto_field(required=True, validate=validate.Length(min=1))
    official_name = ma.auto_field()
    capital = ma.auto_field()
    region = ma.auto_field()
    subregion = ma.auto_field()

class LanguageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Language

    language_id = ma.auto_field()
    language = ma.auto_field(required=True, validate=validate.Length(min=1))
