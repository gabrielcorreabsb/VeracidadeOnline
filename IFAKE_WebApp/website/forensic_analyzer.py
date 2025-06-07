import argparse
import hashlib
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

import PyPDF2
import openpyxl
from docx import Document

class ForensicAnalyzer:
    """
    Uma classe para realizar análises forenses em arquivos de documentos,
    extraindo metadados, calculando hashes e comparando arquivos.
    """

    def __init__(self):
        # Mapeia extensões de arquivo para suas funções de análise correspondentes.
        # Facilita a adição de novos tipos de arquivo.
        self._analyzers = {
            '.pdf': self._analyze_pdf,
            '.docx': self._analyze_docx,
            '.xlsx': self._analyze_excel,
            '.xls': self._analyze_excel,
        }

    def _calculate_file_hashes(self, file_path: str) -> tuple[str, str]:
        """Calcula os hashes MD5 e SHA256 de um arquivo."""
        md5_hash = hashlib.md5()
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
                sha256_hash.update(chunk)
        return md5_hash.hexdigest(), sha256_hash.hexdigest()
    
    def _parse_pdf_date(self, pdf_date: str) -> Optional[str]:
        """Converte o formato de data do PDF (ex: D:20230101120000Z) para ISO 8601."""
        if not pdf_date or not isinstance(pdf_date, str):
            return None
        try:
            # Remove o prefixo "D:" e ajusta para um formato que o strptime entende
            clean_date = pdf_date.replace("D:", "")[:14]
            dt_obj = datetime.strptime(clean_date, '%Y%m%d%H%M%S')
            return dt_obj.isoformat()
        except (ValueError, IndexError):
            return pdf_date # Retorna a string original se a conversão falhar

    def _analyze_pdf(self, file_path: str) -> Dict[str, Any]:
        """Analisa metadados de um arquivo PDF."""
        try:
            with open(file_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                metadata = pdf.metadata or {}
                return {
                    "file_type": "PDF",
                    "author": metadata.get('/Author'),
                    "creator": metadata.get('/Creator'),
                    "producer": metadata.get('/Producer'),
                    "created_date": self._parse_pdf_date(metadata.get('/CreationDate')),
                    "modified_date": self._parse_pdf_date(metadata.get('/ModDate')),
                    "page_count": len(pdf.pages),
                }
        except Exception as e:
            return {"error": f"Erro ao analisar PDF: {e}"}

    def _analyze_docx(self, file_path: str) -> Dict[str, Any]:
        """Analisa metadados de um arquivo DOCX."""
        try:
            doc = Document(file_path)
            props = doc.core_properties
            return {
                "file_type": "DOCX",
                "author": props.author,
                "created_date": props.created.isoformat() if props.created else None,
                "modified_date": props.modified.isoformat() if props.modified else None,
                "last_printed": props.last_printed.isoformat() if props.last_printed else None,
                "revision": props.revision,
            }
        except Exception as e:
            return {"error": f"Erro ao analisar DOCX: {e}"}

    def _analyze_excel(self, file_path: str) -> Dict[str, Any]:
        """Analisa metadados de um arquivo XLS/XLSX."""
        try:
            wb = openpyxl.load_workbook(file_path, read_only=True)
            props = wb.properties
            return {
                "file_type": "Excel (XLS/XLSX)",
                "author": props.creator,
                "created_date": props.created.isoformat() if props.created else None,
                "modified_date": props.modified.isoformat() if props.modified else None,
                "sheet_count": len(wb.sheetnames),
            }
        except Exception as e:
            return {"error": f"Erro ao analisar Excel: {e}"}

    def analyze_document(self, file_path: str) -> Dict[str, Any]:
        """
        Orquestra a análise forense de um único documento.
        """
        if not os.path.exists(file_path):
            return {"error": "Arquivo não encontrado."}

        file_extension = os.path.splitext(file_path)[1].lower()
        md5, sha256 = self._calculate_file_hashes(file_path)

        analysis = {
            "file_name": os.path.basename(file_path),
            "file_path": file_path,
            "hashes": {"md5": md5, "sha256": sha256},
            "file_system_metadata": {
                "size_bytes": os.path.getsize(file_path),
                "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                "created": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
            }
        }

        # Encontra a função de análise correta no dicionário
        analyzer_func = self._analyzers.get(file_extension)
        if analyzer_func:
            analysis["document_metadata"] = analyzer_func(file_path)
        else:
            analysis["document_metadata"] = {"error": f"Formato de arquivo '{file_extension}' não suportado."}
        
        return analysis

    def compare_files(self, file1_path: str, file2_path: str) -> Dict[str, Any]:
        """Compara dois arquivos para verificar se são idênticos com base nos hashes."""
        md5_1, sha256_1 = self._calculate_file_hashes(file1_path)
        md5_2, sha256_2 = self._calculate_file_hashes(file2_path)
        
        return {
            "comparison_summary": {
                "files_are_identical": md5_1 == md5_2 and sha256_1 == sha256_2,
                "md5_match": md5_1 == md5_2,
                "sha256_match": sha256_1 == sha256_2,
            },
            "file1_hashes": {"md5": md5_1, "sha256": sha256_1},
            "file2_hashes": {"md5": md5_2, "sha256": sha256_2}
        }
        
    def generate_report(self, data: Dict[str, Any], output_path: str):
        """Gera um relatório em JSON com os resultados da análise."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Relatório gerado com sucesso em: {output_path}")


def main():
    """Função principal que gerencia a execução via linha de comando."""
    parser = argparse.ArgumentParser(description="Ferramenta de Análise Forense de Documentos.")
    parser.add_argument("file", help="Caminho para o arquivo a ser analisado.")
    parser.add_argument("--compare", help="Caminho para um segundo arquivo para comparação de hashes.")
    parser.add_argument("-o", "--output", help="Caminho do arquivo JSON de saída para o relatório.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Não imprime o relatório JSON no console.")

    args = parser.parse_args()
    
    analyzer = ForensicAnalyzer()
    
    # Análise do arquivo principal
    final_report = analyzer.analyze_document(args.file)
    
    # Se um arquivo de comparação for fornecido, adiciona os dados da comparação
    if args.compare:
        if not os.path.exists(args.compare):
            print(f"⚠️ Erro: Arquivo de comparação não encontrado em '{args.compare}'")
        else:
            comparison_data = analyzer.compare_files(args.file, args.compare)
            final_report["comparison_results"] = comparison_data

    # Imprime o relatório no console, a menos que o modo silencioso esteja ativado
    if not args.quiet:
        print(json.dumps(final_report, indent=4, ensure_ascii=False))

    # Gera o arquivo de relatório se um caminho de saída for especificado
    if args.output:
        analyzer.generate_report(final_report, args.output)


if __name__ == "__main__":
    main()