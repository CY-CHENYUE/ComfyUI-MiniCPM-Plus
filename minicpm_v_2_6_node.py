import torch
from transformers import AutoTokenizer, AutoModel
import os
import folder_paths
import logging
import re
from huggingface_hub import snapshot_download
from PIL import Image
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

logger = logging.getLogger(__name__)
logging.getLogger("transformers").setLevel(logging.ERROR)

class MiniCPM_V_2_6_Handler:
    dependencies_checked = False

    def __init__(self):
        self.name = "openbmb/MiniCPM-V-2_6"
        self.local_path = os.path.join(folder_paths.models_dir, "MiniCPM", "MiniCPM-V-2_6")
        self.tokenizer = None
        self.model = None

    @classmethod
    def check_dependencies(cls):
        if not cls.dependencies_checked:
            from .install import check_and_install_dependencies
            if check_and_install_dependencies():
                logger.info("Dependencies were installed or updated. Please restart ComfyUI for changes to take effect.")
            cls.dependencies_checked = True

    def load_model(self):
        self.check_dependencies()
        
        if not os.path.exists(self.local_path) or not os.listdir(self.local_path):
            logger.info(f"Model not found locally. Downloading {self.name} from Hugging Face...")
            try:
                snapshot_download(repo_id=self.name, local_dir=self.local_path, local_dir_use_symlinks=False)
                logger.info(f"Model downloaded successfully to {self.local_path}")
            except Exception as e:
                logger.error(f"Error downloading model: {str(e)}")
                raise ImportError(f"Failed to download {self.name}. Error: {str(e)}")

        if self.model is None or self.tokenizer is None:
            #logger.info(f"Loading model {self.name}")
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.local_path, trust_remote_code=True)
                
                self.model = AutoModel.from_pretrained(
                    self.local_path,
                    trust_remote_code=True,
                    torch_dtype=torch.float16,  # or torch.bfloat16 if your GPU supports it
                    low_cpu_mem_usage=True
                )
                
                self.model = self.model.cuda().eval()
                #logger.info(f"Model {self.name} loaded successfully on GPU.")
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise RuntimeError(f"Failed to load {self.name}. Error: {str(e)}")

    def preprocess_image(self, image):
        if image is None:
            return None
        
        if isinstance(image, torch.Tensor):
            image = image.cpu().numpy()
        
        if isinstance(image, np.ndarray):
            if image.ndim == 4:
                image = image[0]
            image = Image.fromarray(np.clip(image * 255, 0, 255).astype(np.uint8))
        
        if isinstance(image, Image.Image):
            return image
        
        raise ValueError(f"Unsupported image type: {type(image)}")

    def generate(self, msgs, max_new_tokens, temperature, top_p, top_k, image=None):
        try:
            processed_image = self.preprocess_image(image) if image is not None else None
            
            if processed_image is not None:
                last_user_msg = msgs[-1]
                if isinstance(last_user_msg['content'], str):
                    last_user_msg['content'] = [processed_image, last_user_msg['content']]
                elif isinstance(last_user_msg['content'], list):
                    last_user_msg['content'].insert(0, processed_image)

            response = self.model.chat(
                tokenizer=self.tokenizer,
                image=None,
                msgs=msgs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k
            )
            return response
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            raise RuntimeError(f"Failed to generate response. Error: {str(e)}")

class MiniCPM_V_2_6:
    def __init__(self):
        self.model_handler = MiniCPM_V_2_6_Handler()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "max_new_tokens": ("INT", {"default": 300, "min": 1, "max": 3000}),
                "temperature": ("FLOAT", {"default": 0.5, "min": 0.1, "max": 2.0, "step": 0.1}),
                "top_p": ("FLOAT", {"default": 0.8, "min": 0.1, "max": 1.0, "step": 0.1}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 1000}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "extract_keywords": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "image": ("IMAGE",),
                "user_promptA": ("STRING", {"multiline": True}),  
                "user_promptB": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("responseText", "keywordsText")
    FUNCTION = "generate"
    CATEGORY = "MiniCPM"

    def generate(self, max_new_tokens, temperature, top_p, top_k, seed, extract_keywords, image=None, user_promptA=None, user_promptB=None):
        if user_promptA is None:
            user_promptA = ""
        if user_promptB is None:
            user_promptB = ""

        if seed != 0:
            torch.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)

        self.model_handler.load_model()

        msgs = []

        if user_promptA.strip():
            msgs.append({'role': 'user', 'content': user_promptA})
        elif user_promptB.strip():
            msgs.append({'role': 'user', 'content': user_promptB})
        else:
            msgs.append({'role': 'user', 'content': ''})

        if user_promptB.strip() and user_promptA.strip():
            msgs.append({'role': 'assistant', 'content': user_promptB})

        try:
            res = self.model_handler.generate(msgs, max_new_tokens, temperature, top_p, top_k, image)
            res = self.post_process_response(res)

            keyword_res = ""

            if extract_keywords:
                keyword_prompt = f"""Please extract keywords from the following text, including all occurrences of language (e.g. Chinese, English, etc.)：

{res}

Please list the keywords extracted, separated by commas. Make sure to include all important words, no matter what language. For English words, please keep the original case."""

                keyword_msgs = [{'role': 'user', 'content': keyword_prompt}]
                keyword_res = self.model_handler.generate(keyword_msgs, max_new_tokens, temperature, top_p, top_k, None)
                keyword_res = self.post_process_response(keyword_res)

            return (res, keyword_res)
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            raise RuntimeError(f"Failed to generate response. Error: {str(e)}")

    def post_process_response(self, response):
        pattern = r'^(###\s*)?(?:Assistant|AI|ChatGPT):\s*'
        response = re.sub(pattern, '', response, flags=re.IGNORECASE)
        response = response.lstrip()
        response = re.sub(r'\n(###\s*)?(?:Human|User):\s*$', '', response, flags=re.IGNORECASE)
        response = re.sub(r'\n\s*\n', '\n\n', response)
        return response.strip()