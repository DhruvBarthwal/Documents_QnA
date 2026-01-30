import re
from typing import List, Dict

WHITESPACE_RE = re.compile(r"[ \t]+")
PAGE_NUMBER_RE = re.compile(r"^\s*\d+\s*$")
HEADER_FOOTER_RE = re.compile(
    r"^(confidential|page \d+ of \d+|copyright)$",
    re.IGNORECASE
)

def clean_line(line: str) -> str:
    """
    Cleans a simgle line of text by removing extra spaces and newlines.
    
    :param line: Raw text line
    :type line: str
    :return: Cleaned text line
    :rtype: str
    """
    line = line.strip()
    
    line = re.sub(
        r"(?:\b[A-Za-z]\s){3,}[A-Za-z]",
        lambda m: m.group(0).replace(" ", ""),
        line
    )

    line = re.sub(
        r"(?:\b\d\s){3,}\d",
        lambda m: m.group(0).replace(" ", ""),
        line
    )
    line = re.sub(r'[\uf0b7\uf0a7]', '', line)
    
    if PAGE_NUMBER_RE.match(line):
        return ""
    
    if HEADER_FOOTER_RE.search(line):
        return ""
    
    return line

def clean_text(text:str) -> str:
    """
    Cleans raw documents text while preserving semantic content.
    
    :param text: Raw input extracted from document 
    :type text: str
    :return: Cleaned and normalized text
    :rtype: str
    """
    
    lines = text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        cleaned = clean_line(line)
        if cleaned:
            cleaned_lines.append(cleaned)
    
    cleaned_text = "\n".join(cleaned_lines)
    cleaned_text = WHITESPACE_RE.sub(" ",cleaned_text)
    
    return cleaned_text.strip()

def clean_documents(docs: List[Dict]) -> List[Dict]:
    """
    Cleans a list of parsed document units by normalizing text and preserving metadata.
    
    :param docs: List of parsed documents
    :type docs: List[Dict]
    :return: List of cleaned documents
    :rtype: List[Dict]
    """
    cleaned_docs = []
    
    for doc in docs:
        text = doc.get("text", "")
        cleaned_text = clean_text(text)
        
        if not cleaned_text:
            continue
        
        cleaned_docs.append({
            "text" : cleaned_text,
            "metadata" : doc["metadata"]
        })
    
    return cleaned_docs

if __name__ == "__main__":
    from parse_docs import parse_directory
    
    raw_docs = parse_directory("data/raw")
    cleaned_docs = clean_documents(raw_docs)
    
    print(f"Raw docs: {len(raw_docs)}")
    print(f"Cleaned docs: {len(cleaned_docs)}")