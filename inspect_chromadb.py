"""
Script to inspect ChromaDB contents - embeddings and chunks.
"""

import chromadb
import json
from tabulate import tabulate

def inspect_chromadb(vectorstore_dir="./vectorstore", collection_name="sustainability"):
    """Inspect and display ChromaDB contents."""
    
    try:
        # Connect to ChromaDB
        client = chromadb.PersistentClient(path=vectorstore_dir)
        
        # List all collections
        collections = client.list_collections()
        print(f"\n📚 Available Collections: {len(collections)}")
        for col in collections:
            print(f"  - {col.name}")
        
        # Get the specified collection
        collection = client.get_collection(name=collection_name)
        
        # Get collection stats
        count = collection.count()
        print(f"\n📊 Collection '{collection_name}' Statistics:")
        print(f"  Total documents: {count}")
        
        # Get all documents
        if count > 0:
            results = collection.get(
                include=["documents", "embeddings", "metadatas", "distances"]
            )
            
            print(f"\n📄 Documents and Chunks:")
            print("-" * 80)
            
            for i, (doc_id, document, metadata) in enumerate(
                zip(results["ids"], results["documents"], results["metadatas"])
            ):
                embedding = results["embeddings"][i] if results["embeddings"] else None
                print(f"\n[Document {i+1}]")
                print(f"  ID: {doc_id}")
                print(f"  Metadata: {json.dumps(metadata, indent=2)}")
                print(f"  Chunk Preview: {document[:200]}..." if len(document) > 200 else f"  Chunk: {document}")
                if embedding:
                    print(f"  Embedding Dimension: {len(embedding)}")
                    print(f"  Embedding (first 5 values): {embedding[:5]}")
            
            # Summary table
            print("\n" + "=" * 80)
            print("📋 Summary Table:")
            table_data = []
            for i, (doc_id, document) in enumerate(zip(results["ids"], results["documents"])):
                preview = document[:50].replace('\n', ' ') + "..." if len(document) > 50 else document
                table_data.append([i+1, doc_id, preview, len(document)])
            
            print(tabulate(table_data, headers=["#", "ID", "Preview", "Length"], tablefmt="grid"))
        
        else:
            print(f"\n⚠️  Collection is empty. No chunks found.")
    
    except Exception as e:
        print(f"❌ Error accessing ChromaDB: {str(e)}")
        print(f"\nMake sure:")
        print(f"  1. ChromaDB is properly initialized")
        print(f"  2. Vectorstore directory exists: {vectorstore_dir}")
        print(f"  3. Collection '{collection_name}' has been created by uploading documents first")

if __name__ == "__main__":
    inspect_chromadb()
