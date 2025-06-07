import sys
import platform
import tensorflow as tf
import torch
import os

def check_system():
    print("=== Sistema ===")
    print(f"Sistema Operacional: {platform.system()} {platform.release()}")
    print(f"Versão Python: {sys.version.split()[0]}")
    
    print("\n=== TensorFlow ===")
    print(f"Versão TensorFlow: {tf.__version__}")
    print("Dispositivos TensorFlow disponíveis:")
    print([device.device_type for device in tf.config.list_physical_devices()])
    
    print("\n=== PyTorch ===")
    print(f"Versão PyTorch: {torch.__version__}")
    print(f"CUDA disponível para PyTorch: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Dispositivo CUDA: {torch.cuda.get_device_name(0)}")
    
    print("\n=== Variáveis de Ambiente CUDA ===")
    cuda_path = os.environ.get('CUDA_PATH', 'Não definido')
    print(f"CUDA_PATH: {cuda_path}")
    
check_system()