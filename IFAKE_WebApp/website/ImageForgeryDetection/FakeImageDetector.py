import os
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from PIL import Image
import tensorflow as tf
from scipy import signal  # Importe signal do SciPy

class FID:
    def __init__(self):
        # Carrega o modelo MobileNetV2 pré-treinado
        self.model = MobileNetV2(weights='imagenet', include_top=True)

    def preprocess_image(self, image_path):
        try:
            # Carrega e redimensiona a imagem
            img = Image.open(image_path)
            img = img.convert('RGB')  # Converte para RGB se necessário
            img = img.resize((224, 224))  # Tamanho requerido pelo MobileNetV2

            # Converte para array e pré-processa
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            return x
        except Exception as e:
            print(f"Erro no pré-processamento: {e}")
            return None

    def analyze_image_quality(self, image_path):
        try:
            # Análise básica de qualidade
            img = Image.open(image_path)

            # Verifica resolução
            width, height = img.size
            if width < 100 or height < 100:
                return -0.5  # Penalidade para imagens muito pequenas

            # Verifica formato
            if img.format not in ['JPEG', 'PNG']:
                return -0.3  # Penalidade para formatos não comuns

            return 0  # Sem penalidade
        except:
            return 0

    def predict_result(self, image_path):
        try:
            # Pré-processa a imagem
            processed_img = self.preprocess_image(image_path)
            if processed_img is None:
                return 'Error', 0

            # Faz a predição
            predictions = self.model.predict(processed_img)

            # Analisa a qualidade da imagem
            quality_score = self.analyze_image_quality(image_path)

            # Calcula métricas de confiança
            prediction_confidence = float(np.max(predictions))

            # Ajusta a confiança com base na qualidade
            adjusted_confidence = (prediction_confidence + quality_score) * 100
            adjusted_confidence = max(min(adjusted_confidence, 100), 0)  # Limita entre 0 e 100

            # Análise de características da imagem para determinar autenticidade
            if adjusted_confidence > 85:  # Alta confiança na predição
                result = 'Authentic'
            elif adjusted_confidence < 60:  # Baixa confiança
                result = 'Forged'
            else:
                # Análise adicional para casos intermediários
                img = Image.open(image_path)
                if img.mode == 'RGB' and adjusted_confidence > 70:
                    result = 'Authentic'
                else:
                    result = 'Forged'

            return result, adjusted_confidence

        except Exception as e:
            print(f"Erro na predição: {e}")
            return 'Error', 0

    def genMask(self, image_path):
        try:
            # Gera uma máscara simples para visualização
            img = Image.open(image_path)
            img = img.convert('RGB')
            img = img.resize((224, 224))

            # Cria uma máscara básica baseada em diferenças de intensidade
            img_array = np.array(img)
            gray = np.mean(img_array, axis=2)
            mask = np.abs(np.diff(gray, axis=1))
            mask = np.pad(mask, ((0,0),(0,1)), mode='edge')

            # Normaliza a máscara
            mask = (mask - mask.min()) / (mask.max() - mask.min()) * 255
            mask = mask.astype(np.uint8)

            # Salva a máscara
            mask_img = Image.fromarray(mask)
            mask_img.save('media/tempresaved.jpg')

        except Exception as e:
            print(f"Erro ao gerar máscara: {e}")

    def show_ela(self, image_path):
        try:
            # Análise de Erro de Nível (ELA)
            original = Image.open(image_path)
            original = original.convert('RGB')

            # Salva com qualidade 90
            temp_path = 'media/temp_ela.jpg'
            original.save(temp_path, 'JPEG', quality=90)

            # Carrega a imagem salva
            saved = Image.open(temp_path)

            # Calcula ELA
            ela = np.abs(np.array(original) - np.array(saved)) * 10
            ela = np.clip(ela, 0, 255).astype(np.uint8)

            # Salva o resultado
            ela_img = Image.fromarray(ela)
            ela_img.save('media/tempresaved.jpg')

            # Limpa arquivo temporário
            os.remove(temp_path)

        except Exception as e:
            print(f"Erro ao gerar ELA: {e}")

    def detect_edges(self, image_path):
        try:
            # Detecção de bordas usando Sobel
            img = Image.open(image_path).convert('L')
            img_array = np.array(img)

            # Aplica filtro Sobel
            sobel_h = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
            sobel_v = np.array([[-1,-2,-1], [0,0,0], [1,2,1]])

            edges_h = np.abs(signal.convolve2d(img_array, sobel_h, mode='same')) # Use signal.convolve2d
            edges_v = np.abs(signal.convolve2d(img_array, sobel_v, mode='same')) # Use signal.convolve2d

            edges = np.sqrt(edges_h**2 + edges_v**2)
            edges = np.clip(edges, 0, 255).astype(np.uint8)

            # Salva o resultado
            edge_img = Image.fromarray(edges)
            edge_img.save('media/tempresaved.jpg')

        except Exception as e:
            print(f"Erro ao detectar bordas: {e}")

    def luminance_gradient(self, image_path):
        try:
            # Análise de gradiente de luminância
            img = Image.open(image_path).convert('L')
            img_array = np.array(img, dtype=float)

            # Calcula gradiente
            gradient_y = np.diff(img_array, axis=0)
            gradient_x = np.diff(img_array, axis=1)

            # Combina gradientes
            gradient = np.sqrt(np.pad(gradient_x, ((0,0),(0,1)))**2 +
                             np.pad(gradient_y, ((0,1),(0,0)))**2)

            # Normaliza e converte
            gradient = (gradient / gradient.max() * 255).astype(np.uint8)

            # Salva o resultado
            grad_img = Image.fromarray(gradient)
            grad_img.save('media/luminance_gradient.tiff')

        except Exception as e:
            print(f"Erro ao gerar gradiente: {e}")

    def apply_na(self, image_path):
        try:
            # Análise de ruído
            img = Image.open(image_path).convert('RGB')
            img_array = np.array(img, dtype=float)

            # Extrai componentes de cor
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]

            # Calcula ruído
            noise = np.std([r, g, b], axis=0)
            noise = (noise / noise.max() * 255).astype(np.uint8)

            # Salva o resultado
            noise_img = Image.fromarray(noise)
            noise_img.save('media/tempresaved.jpg')

        except Exception as e:
            print(f"Erro na análise de ruído: {e}")