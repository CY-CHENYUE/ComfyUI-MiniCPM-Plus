import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import folder_paths
import logging
import warnings
import re
from huggingface_hub import snapshot_download

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

logger = logging.getLogger(__name__)
logging.getLogger("transformers").setLevel(logging.ERROR)

class MiniCPM3_4B_Handler:
    def __init__(self):
        self.name = "openbmb/MiniCPM3-4B" 
        self.local_path = os.path.join(folder_paths.models_dir, "MiniCPM", "MiniCPM3-4B")
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def load_model(self):
        from .install import check_and_install_dependencies
        check_and_install_dependencies()

        if not os.path.exists(self.local_path) or not os.listdir(self.local_path):
            logger.info(f"Model not found locally. Downloading {self.name} from Hugging Face...")
            try:
                snapshot_download(repo_id=self.name, local_dir=self.local_path, local_dir_use_symlinks=False)
                logger.info(f"Model downloaded successfully to {self.local_path}")
            except Exception as e:
                logger.error(f"Error downloading model: {str(e)}")
                raise ImportError(f"Failed to download {self.name}. Error: {str(e)}")

        if self.model is None or self.tokenizer is None:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.local_path, trust_remote_code=True)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.local_path,
                    torch_dtype=torch.float16,
                    device_map=self.device,
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
                
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise ImportError(f"Failed to load {self.name}. Error: {str(e)}")

class MiniCPM3_4B:
    def __init__(self):
        self.model_handler = MiniCPM3_4B_Handler()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "user_promptA": ("STRING", {"multiline": True}),
                "user_promptB": ("STRING", {"multiline": True}),
            },
            "required": {
                "max_new_tokens": ("INT", {"default": 300, "min": 1, "max": 3000}),
                "temperature": ("FLOAT", {"default": 0.5, "min": 0.1, "max": 2.0, "step": 0.1}),
                "top_p": ("FLOAT", {"default": 0.8, "min": 0.1, "max": 1.0, "step": 0.1}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 1000}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "MiniCPM"

    def generate(self, max_new_tokens, temperature, top_p, top_k, seed, user_promptA=None, user_promptB=None):
        default_prompt = "......:"
        if user_promptA is None or len(user_promptA.strip()) < 4:
            user_promptA = (user_promptA or "") + default_prompt 
        
        if user_promptB is None:
            user_promptB = ""

        combined_prompt = user_promptA + " " + user_promptB
        self.model_handler.load_model()

        msgs = [
            {'role': 'user', 'content': combined_prompt}
        ]

        model_inputs = self.model_handler.tokenizer.apply_chat_template(
            msgs,
            return_tensors="pt",
            add_generation_prompt=True
        ).to(self.model_handler.device)

        generation_config = {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "pad_token_id": self.model_handler.tokenizer.pad_token_id,
            "eos_token_id": self.model_handler.tokenizer.eos_token_id,
        }

        with torch.no_grad():
            model_outputs = self.model_handler.model.generate(
                model_inputs,
                **generation_config
            )

        output_token_ids = model_outputs[0][len(model_inputs[0]):]
        res = self.model_handler.tokenizer.decode(output_token_ids, skip_special_tokens=True)
        res = self.post_process_response(res)
        
        return (res,)

    def post_process_response(self, response):
        pattern = r'^(###\s*)?(?:Assistant|AI|ChatGPT):\s*'
        response = re.sub(pattern, '', response, flags=re.IGNORECASE)
        response = response.lstrip()
        response = re.sub(r'\n(###\s*)?(?:Human|User):\s*$', '', response, flags=re.IGNORECASE)
        response = re.sub(r'\n\s*\n', '\n\n', response)
        return response.strip()