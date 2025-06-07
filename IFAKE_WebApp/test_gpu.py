import sys
import tensorflow as tf
import numpy as np
import time

def test_gpu():
    print("="*50)
    print("Informações do Ambiente:")
    print("="*50)
    print("Python version:", sys.version)
    print("TensorFlow version:", tf.__version__)
    print("NumPy version:", np.__version__)
    print("\nVerificando GPU...")

    gpus = tf.config.list_physical_devices('GPU')
    print(f"\nGPUs disponíveis: {gpus}")

    if len(gpus) > 0:
        # Configurar memória da GPU para crescimento gradual
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print("Memória da GPU configurada com sucesso!")
        except RuntimeError as e:
            print("Erro ao configurar GPU:", e)

        print("\nTestando performance da GPU...")
        try:
            # Teste de performance com operações matriciais
            with tf.device('/GPU:0'):
                # Aquecer a GPU
                _ = tf.random.normal([1000, 1000])
                tf.config.experimental.reset_memory_stats('GPU:0')

                # Teste real
                start_time = time.time()
                a = tf.random.normal([5000, 5000])
                b = tf.random.normal([5000, 5000])
                c = tf.matmul(a, b)
                tf.debugging.assert_all_finite(c, "Erro no cálculo")
                end_time = time.time()

                print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
                print("Operação com GPU concluída com sucesso!")
        except Exception as e:
            print("Erro durante o teste de GPU:", e)
    else:
        print("[91mATENÇÃO: Nenhuma GPU encontrada![0m")

if __name__ == "__main__":
    test_gpu()
