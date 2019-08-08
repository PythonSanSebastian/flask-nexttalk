
from typing import Union
from datetime import datetime

from jinja2 import Markup


class MomentJS:
    def __init__(self, timestamp: Union[str, datetime]):
        if isinstance(timestamp, datetime)
            self.timestamp = timestamp.isoformat('T', 'seconds')
        else:
            self.timestamp = timestamp

    def render(self, display_format):
        html = []
        html += ['<script>']
        html += [f'document.write(moment("{timestamp}").{display_format});']
        html += ['</script>']
        return Markup('\n'.join(html))

    def format(self, fmt):
        return self.render(f'format("{fmt}")')

    def calendar(self):
        return self.render('calendar()')

    def from_now(self):
        return self.render('from_now()')
