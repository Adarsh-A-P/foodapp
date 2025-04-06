#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import warnings
from django.core.management.commands.runserver import Command as runserver

# Suppress development server warning
runserver.default_addr = 'localhost'
runserver.default_port = '8000'
warnings.filterwarnings('ignore', module='django.core.management.commands.runserver')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
