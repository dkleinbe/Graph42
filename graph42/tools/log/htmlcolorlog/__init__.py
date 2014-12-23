"""A logging formatter for colored output"""

from __future__ import absolute_import

from graph42.tools.log.htmlcolorlog.htmlcolorlog import (
    HtmlColoredFormatter, escape_codes, default_log_colors)

__all__ = [
    'HtmlColoredFormatter', 'default_log_colors', 'escape_codes', 'basicConfig',
    'root', 'getLogger', 'debug', 'info', 'warning', 'error', 'exception',
    'critical', 'log', 'exception'
]
