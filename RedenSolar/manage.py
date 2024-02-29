#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import psycopg2
import time

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RedenSolar.settings')
    # execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
