__author__ = 'oier'

from jinja2 import Markup


class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    # Wrapper to call moment.js method
    def render(self, display_format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (
            self.timestamp.strftime("%Y-%m-%dT%H:%M:%S"), display_format))

    # Format time
    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def from_now(self):
        return self.render("from_now()")
