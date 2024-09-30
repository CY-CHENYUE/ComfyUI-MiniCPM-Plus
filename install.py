import os
import sys
import subprocess
import importlib
import logging
from packaging import version
import pkg_resources

# 设置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_installed_version(package_name):
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None

def check_and_install_dependencies():
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # requirements.txt 文件的路径
    requirements_path = os.path.join(current_dir, 'requirements.txt')
    
    changes_made = False
    
    # 读取 requirements.txt 文件
    with open(requirements_path, 'r') as f:
        requirements = f.read().splitlines()
    
    for requirement in requirements:
        # 忽略空行和注释
        if not requirement or requirement.startswith('#'):
            continue
        
        # 解析包名和版本
        parts = requirement.split('==')
        package_name = parts[0].strip()
        required_version = parts[1].strip() if len(parts) > 1 else None
        
        installed_version = get_installed_version(package_name)
        
        if installed_version is None:
            logger.info(f"Installing new package: {package_name}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
            changes_made = True
        elif required_version and version.parse(installed_version) < version.parse(required_version):
            logger.info(f"Updating package: {package_name} from {installed_version} to {required_version}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", requirement], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
            changes_made = True
        else:
            logger.debug(f"Package {package_name} is already up to date (installed: {installed_version}).")
    
    return changes_made

def package_installed(package_name):
    return get_installed_version(package_name) is not None

if __name__ == "__main__":
    check_and_install_dependencies()