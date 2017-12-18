#!/usr/bin/env python
import os
import sys

def activate_venv(base):
    if os.path.exists(base):
        old_os_path = os.environ.get('PATH', '')
        os.environ['PATH'] = os.path.join(base, 'bin') + os.pathsep + old_os_path
        site_packages = os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages')
        prev_sys_path = list(sys.path)
        import site
        site.addsitedir(site_packages)
        sys.real_prefix = sys.prefix
        sys.prefix = base
        # Move the added items to the front of the path:
        new_sys_path = []
        for item in list(sys.path):
            if item not in prev_sys_path:
                new_sys_path.append(item)
                sys.path.remove(item)
        sys.path[:0] = new_sys_path


if __name__ == "__main__":
    root_dir = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
    activate_venv(os.path.normpath(os.path.join(root_dir, 'venv')))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camp.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
