import os
import sys
import subprocess
import importlib.util
import logging

# 设置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_and_install_dependencies():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(current_dir, 'requirements.txt')
    
    try:
        with open(requirements_path, 'r') as f:
            dependencies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.error(f"Error: 'requirements.txt' not found at {requirements_path}")
        return False

    newly_installed = False
    for package in dependencies:
        package_name = package.split("==")[0].split(">=")[0]
        if not package_installed(package_name):
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--no-warn-script-location"],
                                      stdout=subprocess.DEVNULL)
                newly_installed = True
            except subprocess.CalledProcessError as e:
                logger.error(f"Error installing {package}: {e}")
                logger.error(f"Please install {package} manually.")

    if newly_installed:
        logger.info("New dependencies were installed. It is recommended to restart ComfyUI for changes to take full effect.")
    
    return newly_installed

def package_installed(package_name):
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

if __name__ == "__main__":
    newly_installed = check_and_install_dependencies()
    if newly_installed:
        logger.info("Please restart ComfyUI for the changes to take effect.")
    else:
        logger.info("No new packages were installed.")