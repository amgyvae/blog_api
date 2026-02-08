#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

def main() -> None:
    base_dir = Path(__file__).resolve().parent
    
    os.chdir(base_dir)
    
    env_id = os.environ.get('BLOG_ENV_ID', 'local')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.env.{env_id}')
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
