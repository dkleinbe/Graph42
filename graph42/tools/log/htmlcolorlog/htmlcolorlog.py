"""The ColoredFormatter class"""

from __future__ import absolute_import

import logging
import sys
import html

from graph42.tools.log.htmlcolorlog.escape_codes import escape_codes


__all__ = ['escape_codes', 'default_log_colors', 'HtmlColoredFormatter']

# The default colors to use for the debug levels
default_log_colors = {
    'DEBUG':    'white',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'bold_red',
}


class HtmlColoredFormatter(logging.Formatter):
    """A formatter that allows colors to be placed in the format string.

    Intended to help in creating more readable logging output."""

    def __init__(self, format, datefmt=None,
                 log_colors=default_log_colors, reset=True, style='%'):
        """
        :Parameters:
        - format (str): The format string to use
        - datefmt (str): A format string for the date
        - log_colors (dict):
            A mapping of log level names to color names
        - reset (bool):
            Implictly append a color reset to all records unless False
        - style ('%' or '{' or '$'):
            The format style to use. No meaning prior to Python 3.2.

        The ``format``, ``datefmt`` and ``style`` args are passed on to the
        Formatter constructor.
        """
        if sys.version_info > (3, 2):
            super(HtmlColoredFormatter, self).__init__(
                format, datefmt, style=style)
        elif sys.version_info > (2, 7):
            super(HtmlColoredFormatter, self).__init__(format, datefmt)
        else:
            logging.Formatter.__init__(self, format, datefmt)
        self.log_colors = log_colors
        self.reset = reset

    def formatMessage(self, record):

        # Escape html code in message
        record.message = html.escape(record.message)

        # Add the color codes to the record
        record.__dict__.update(escape_codes)

        # If we recognise the level name,
        # add the levels color as `log_color`
        if record.levelname in self.log_colors:
            color = self.log_colors[record.levelname]
            record.log_color = escape_codes[color]
        else:
            record.log_color = ""

        # Format the message
        if sys.version_info > (2, 7):
            message = super(HtmlColoredFormatter, self).formatMessage(record)
        else:
            message = logging.Formatter.formatMessage(self, record)

        # Add a reset code to the end of the message
        # (if it wasn't explicitly added in format str)
        if self.reset and not message.endswith(escape_codes['br']):
            pass
            #message += escape_codes['br']

        return message
