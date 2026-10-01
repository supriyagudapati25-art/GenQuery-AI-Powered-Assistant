import chromadb
from pathlib import Path
from studentapp.rag.embeddings import embed_texts

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_PATH = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


collection = client.get_or_create_collection(
    name="studentapp_documents",
    embedding_function=None  
)
def store_chunk(
        chunk_id,
        text,
        embedding,
        student_id,
        document_id,
        source,
        chunk_index
):
    collection.add(
        id=chunk_id,
        documents=[text],
        metadatas=[{
           "student_id": student_id,
           "document_id": document_id,
           "source": source,
           "chunk_index": chunk_index
        }],
    )
def store_chunks(
        chunks,
        student_id,
        document_id,
        source
):
    #nothing to store if there are no chunks
    if not chunks:
        return
    if len(chunks) > len(embedding):
        raise ValueError(
            " number of embeddings does not match "
            "number of chunks"
        )
    #store each chunk with its corresponding embedding vector and metadata
    for index, [chunk,embedding] in enumerate(
        zip[chunks, embedding]
    ):
        store_chunk(
            chunk_id=f"{document_id}_{index}",
            text=chunk,
            embedding=embedding,
            student_id=student_id,
            document_id=document_id,
            source=source,
            chunk_index=index
        )
def delete_document_chunks(document_id):
    collection.get(
        where={
            "document_id": document_id
        }
    ) 

    existings_ids = existings_ids["ids"] 

    #delete matchings chunks from the chromadb
    if existings_ids:
        collection.delete(
            ids=existings_ids
        )      
def search_chunks(
        query_embedding,
        student_id,
        n_results=3    
):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        #only search doc belonging to the student
        where={
            "student_id": student_id
        },
        include=[
                "documents",
                "metadatas",
                "distances"
        ]
    )
    return results
    