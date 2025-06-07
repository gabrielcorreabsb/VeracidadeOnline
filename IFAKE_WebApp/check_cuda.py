# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import tensorflow as tf

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8', errors='ignore').strip()
    except:
        return None

def check_cuda():
    print("=== CUDA Diagnostic ===\n")

    # 1. GPU Check
    print("1. GPU Information:")
    gpu_info = run_command("wmic path win32_VideoController get name")
    if gpu_info:
        print(gpu_info)
    else:
        print("Could not detect GPU")

    # 2. CUDA Path Check
    print("\n2. CUDA Path Check:")
    cuda_path = os.environ.get('CUDA_PATH')
    print(f"CUDA_PATH = {cuda_path}")

    if cuda_path and os.path.exists(cuda_path):
        print("[OK] CUDA_PATH exists")
        print(f"Files in {cuda_path}\\bin:")
        try:
            files = os.listdir(os.path.join(cuda_path, 'bin'))
            print('\n'.join(files[:5]) + '\n...')
        except:
            print("Could not list files")
    else:
        print("[ERROR] CUDA_PATH not found")

    # 3. NVCC Check
    print("\n3. NVCC (CUDA Compiler) Check:")
    nvcc_version = run_command("nvcc --version")
    if nvcc_version:
        print(nvcc_version)
    else:
        print("[ERROR] NVCC not found")
        print("Make sure CUDA is installed and in system PATH")

    # 4. TensorFlow Check
    print("\n4. TensorFlow Configuration:")
    print(f"TensorFlow version: {tf.__version__}")
    print("Available devices:")
    try:
        devices = tf.config.list_physical_devices()
        for device in devices:
            print(f"- {device.device_type}: {device.name}")
    except:
        print("Error listing TensorFlow devices")

    # 5. System PATH Check
    print("\n5. System PATH Check:")
    path = os.environ.get('PATH', '').split(os.pathsep)
    cuda_paths = [p for p in path if 'cuda' in p.lower()]
    if cuda_paths:
        print("CUDA entries in PATH:")
        for p in cuda_paths:
            print(f"- {p}")
    else:
        print("[ERROR] No CUDA entries found in PATH")

    # 6. Recommendations
    print("\n=== Recommendations ===")
    if not cuda_path:
        print("1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads")
    if not nvcc_version:
        print("2. Add CUDA bin folder to system PATH")
    if not cuda_paths:
        print("3. Check system environment variables")
    if not any('nvidia' in gpu_info.lower() if gpu_info else False):
        print("4. Check if you have a compatible NVIDIA GPU")

if __name__ == "__main__":
    check_cuda()
