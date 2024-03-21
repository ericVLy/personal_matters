# node_dependency_checker/management/commands/install_node_dependencies.py
import os
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand


currentPath = os.path.split(os.path.realpath(__file__))[0]
projectRootPath = os.path.abspath(os.path.join(currentPath, '..', '..', '..'))

if settings.DEBUG:
    static_path = os.path.join(projectRootPath, 'personal_matters', 'static')
else:
    static_path = os.path.join(projectRootPath, "static/")


class Command(BaseCommand):
    help = 'Check and install Node.js dependencies'

    def handle(self, *args, **options):
        try:
            # 检查 Node.js 是否可用
            subprocess.run(['node', '--version'], check=True)
            subprocess.run(['npm', '--version'], check=True)
            print('Node.js is installed.')

            # 检查并安装 Node.js 依赖
            print(static_path)
            subprocess.run(['npm', 'install'], check=True, cwd=static_path)
            print('Node.js dependencies installed successfully.')

        except FileNotFoundError:
            print('Node.js is not installed. Please install Node.js and npm first.')

        except subprocess.CalledProcessError as e:
            print('An error occurred while installing Node.js dependencies:', e)
