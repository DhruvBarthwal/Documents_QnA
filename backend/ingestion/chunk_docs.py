from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(
    docs : List[Dict],
    chunk_size : int = 800,
    chunk_overlap: int = 120
)-> List[Dict]:
    """
    Chunk cleaned documents using RecursiveCharacterTextSplitter.
    
    :param docs: List of cleaned document units containing text and metadat
    :type docs: List[Dict]
    :param chunk_size: Maximum number of tokens per chunk
    :type chunk_size: int
    :param chunk_overlap: Number of overlapping tokens between consecutive chunks
    :type chunk_overlap: int
    :return: List of chunked documents with preserved metadata
    :rtype: List[Dict]
    """
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        separators = ["\n\n", "\n", ".", " ", ""] 
    )
    
    chunked_docs = []
    
    for doc in docs:
        splits = splitter.split_text(doc["text"])
        
        for i, split in enumerate(splits):
            chunked_docs.append({
                "text" : split,
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": f"{doc['metadata']['source']}_{i}"

                }
            })
            
    return chunked_docs

if __name__ == "__main__":
    from parse_docs import parse_directory
    from clean_text import clean_documents
    
    raw_docs = parse_directory("data/raw")
    cleaned_docs = clean_documents(raw_docs)
    chunked_docs = chunk_documents(cleaned_docs)
    
    print(f"Dcouments: {len(cleaned_docs)}")
    print(f"Chunks: {len(chunked_docs)}")