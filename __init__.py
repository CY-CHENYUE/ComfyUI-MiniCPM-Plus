"""
@author: CY-CHENYUE
@title: MiniCPM-Plus
@nickname: MiniCPM-Plus
@description: Custom nodes for MiniCPM language models in ComfyUI
"""

import os
import sys
import importlib


current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


from .install import check_and_install_dependencies

newly_installed = check_and_install_dependencies()


restart_flag = os.path.join(current_dir, '.restart_required')
if os.path.exists(restart_flag):
    if newly_installed:
        print("New dependencies were installed. Please restart ComfyUI for them to take effect.")
        os.remove(restart_flag)  
        sys.exit(0)  
    else:
        os.remove(restart_flag) 


try:
    from .minicpm3_4b_node import MiniCPM3_4B
    from .minicpm_v_2_6_node import MiniCPM_V_2_6
    from .minicpm_v_2_6_int_4_node import MiniCPM_V_2_6_Int4
    from .minicpm3_4b_GPTQ_int4_node import MiniCPM3_4B_GPTQ_Int4
    from .text_display_node import TextDisplay

    NODE_CLASS_MAPPINGS = {
        "MiniCPM_V_2_6": MiniCPM_V_2_6,
        "MiniCPM_V_2_6_Int4": MiniCPM_V_2_6_Int4,    
        "MiniCPM3_4B": MiniCPM3_4B,
        "MiniCPM3_4B_GPTQ_Int4": MiniCPM3_4B_GPTQ_Int4,
        "TextDisplay": TextDisplay
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "MiniCPM_V_2_6": "MiniCPM-Plus: V-2.6", 
        "MiniCPM_V_2_6_Int4": "MiniCPM-Plus: V-2.6_Int4",
        "MiniCPM3_4B": "MiniCPM-Plus: 3-4B", 
        "MiniCPM3_4B_GPTQ_Int4": "MiniCPM-Plus: 3-4B-GPTQ-Int4",
        "TextDisplay": "MiniCPM-Plus: TextDisplay"
    }
except Exception as e:
    print(f"Error loading MiniCPM nodes: {str(e)}")
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']