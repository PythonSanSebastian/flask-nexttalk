from werkzeug.routing import BaseConverter, ValidationError

from config import valid_rooms_routes


class RoomsConverter(BaseConverter):
    def to_python(self, value):
        try:
            return valid_rooms_routes[value.lower()]
        except KeyError:
            raise ValidationError()

    def to_url(self, value):
        for k, v in valid_rooms_routes.items():
            if v == value:
                return k
