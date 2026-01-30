import os
from typing import List, Dict

from pathlib import Path
from bs4 import BeautifulSoup
from pypdf import PdfReader
import docx

SUPPORTED_EXTENSIONS = {".pdf",".docx",".html",".txt"}

def parse_pdf(file_path: Path) -> List[Dict]:
    reader = PdfReader(str(file_path))
    docs = []
    
    for page_num, page in enumerate(reader.pages):
        text= page.extract_text()
        if text and text.strip():
            docs.append({
                "text" : text,
                "metadata" : {
                    "source" : file_path.name,
                    "page" : page_num + 1,
                    "file_type" : "pdf"
                }
            })
    return docs

def parse_docx(file_path : Path) -> List[Dict]:
    doc = docx.Document(str(file_path))
    full_text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    
    return [{
        "text" : full_text,
        "metadata" : {
            "source" : file_path.name,
            "file_type" : "docx"
        }
    }]
    
def parse_html(file_path : Path) -> List[Dict]:
    with open(file_path, "r",encoding ="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(),"html.parser")
        
    text = soup.get_text(separator="\n")
    
    return [{
        "text" : text,
        "metadata" : {
            "source" : file_path.name,
            "file_type" : "html"
        }
    }]
    
def parse_txt(file_path: Path) -> List[Dict]:
    with open(file_path, "r", encoding ="utf-8",errors="ignore") as f:
        text = f.read()
    
    return [{
        "text" : text,
        "metadata" : {
            "source" : file_path.name,
            "file_type" : "txt"
        }
    }]
    
def parse_file(file_path: Path) -> List[Dict]:
    ext = file_path.suffix.lower()
    
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    elif ext == ".html":
        return parse_html(file_path)
    elif ext == ".txt":
        return parse_txt(file_path)
    else: 
        raise ValueError(f"Unsupported file type: {ext}")
    
def parse_directory(data_dir : str) -> List[Dict]:
    parsed_docs = []
    
    for root,_, files in os.walk(data_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                try :
                    docs = parse_file(file_path)
                    parsed_docs.extend(docs)
                except Exception as e:
                    print(f"[WARN] Failed to parse {file_path}: {e}")
                    
    return parsed_docs

if __name__ == "__main__":
    docs = parse_directory("data/raw")
    print(f"Parsed {len(docs)} document units")