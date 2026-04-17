"""
Interactive terminal tool to inspect ChromaDB contents.
Run: python view_chromadb.py
"""

import chromadb
import json
from typing import Optional
import os


class ChromaDBViewer:
    """Interactive viewer for ChromaDB contents."""
    
    def __init__(self, vectorstore_dir="./vectorstore"):
        self.vectorstore_dir = vectorstore_dir
        self.client = None
        self.collection = None
        self.collection_name = None
        
    def connect(self):
        """Connect to ChromaDB."""
        try:
            if not os.path.exists(self.vectorstore_dir):
                print(f"❌ Vectorstore directory not found: {self.vectorstore_dir}")
                return False
            
            self.client = chromadb.PersistentClient(path=self.vectorstore_dir)
            print(f"✅ Connected to ChromaDB at {self.vectorstore_dir}\n")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return False
    
    def list_collections(self):
        """List all available collections."""
        try:
            collections = self.client.list_collections()
            if not collections:
                print("❌ No collections found in ChromaDB\n")
                return False
            
            print(f"\n📚 Available Collections ({len(collections)}):")
            for i, col in enumerate(collections, 1):
                print(f"  {i}. {col.name}")
            print()
            return True
        except Exception as e:
            print(f"❌ Error listing collections: {str(e)}\n")
            return False
    
    def select_collection(self, name: str):
        """Select a collection to view."""
        try:
            self.collection = self.client.get_collection(name=name)
            self.collection_name = name
            count = self.collection.count()
            print(f"✅ Selected collection: {name}")
            print(f"   Total documents: {count}\n")
            return True
        except Exception as e:
            print(f"❌ Error selecting collection: {str(e)}\n")
            return False
    
    def view_all_chunks(self):
        """Display all chunks in the collection."""
        try:
            if not self.collection:
                print("❌ No collection selected\n")
                return
            
            count = self.collection.count()
            if count == 0:
                print("❌ Collection is empty\n")
                return
            
            results = self.collection.get(
                include=["documents", "metadatas", "embeddings"]
            )
            
            print(f"\n📄 All Chunks in '{self.collection_name}' ({count} total):")
            print("=" * 100)
            
            for i, (doc_id, document, metadata) in enumerate(
                zip(results["ids"], results["documents"], results["metadatas"]), 1
            ):
                embedding = results["embeddings"][i-1] if results["embeddings"] else None
                
                print(f"\n[Chunk {i}]")
                print(f"  ID: {doc_id}")
                print(f"  Metadata: {json.dumps(metadata)}")
                print(f"  Embedding Dimension: {len(embedding) if embedding else 'N/A'}")
                print(f"  Content ({len(document)} chars):")
                print(f"  {'-' * 96}")
                print(f"  {document}")
                print(f"  {'-' * 96}")
            
        except Exception as e:
            print(f"❌ Error viewing chunks: {str(e)}\n")
    
    def view_chunk(self, chunk_number: int):
        """Display a specific chunk."""
        try:
            if not self.collection:
                print("❌ No collection selected\n")
                return
            
            count = self.collection.count()
            if chunk_number < 1 or chunk_number > count:
                print(f"❌ Invalid chunk number. Valid range: 1-{count}\n")
                return
            
            results = self.collection.get(
                include=["documents", "metadatas", "embeddings"]
            )
            
            idx = chunk_number - 1
            doc_id = results["ids"][idx]
            document = results["documents"][idx]
            metadata = results["metadatas"][idx]
            embedding = results["embeddings"][idx] if results["embeddings"] else None
            
            print(f"\n📄 Chunk {chunk_number}:")
            print("=" * 100)
            print(f"ID: {doc_id}")
            print(f"Metadata: {json.dumps(metadata, indent=2)}")
            if embedding:
                print(f"Embedding Dimension: {len(embedding)}")
                print(f"Embedding (first 10 values): {embedding[:10]}")
            print(f"\nContent ({len(document)} chars):")
            print("-" * 100)
            print(document)
            print("-" * 100)
            
        except Exception as e:
            print(f"❌ Error viewing chunk: {str(e)}\n")
    
    def search_chunks(self, query: str, limit: int = 5):
        """Search for chunks by text content."""
        try:
            if not self.collection:
                print("❌ No collection selected\n")
                return
            
            results = self.collection.get(
                include=["documents", "metadatas"]
            )
            
            matching = []
            for i, doc in enumerate(results["documents"]):
                if query.lower() in doc.lower():
                    matching.append((i+1, doc, results["metadatas"][i]))
            
            if not matching:
                print(f"❌ No chunks found containing '{query}'\n")
                return
            
            print(f"\n🔍 Found {len(matching)} chunks containing '{query}':")
            print("=" * 100)
            
            for count, (chunk_num, content, metadata) in enumerate(matching[:limit], 1):
                print(f"\n[Result {count}] Chunk {chunk_num}:")
                print(f"Metadata: {json.dumps(metadata)}")
                preview = content[:300] + "..." if len(content) > 300 else content
                print(f"Content: {preview}")
            
            if len(matching) > limit:
                print(f"\n... and {len(matching) - limit} more results")
            
        except Exception as e:
            print(f"❌ Error searching: {str(e)}\n")
    
    def get_stats(self):
        """Display collection statistics."""
        try:
            if not self.collection:
                print("❌ No collection selected\n")
                return
            
            count = self.collection.count()
            if count == 0:
                print("❌ Collection is empty\n")
                return
            
            results = self.collection.get(
                include=["documents", "embeddings"]
            )
            
            total_chars = sum(len(doc) for doc in results["documents"])
            avg_len = total_chars // count
            
            print(f"\n📊 Statistics for '{self.collection_name}':")
            print(f"  Total Chunks: {count}")
            print(f"  Total Characters: {total_chars:,}")
            print(f"  Average Chunk Length: {avg_len:,}")
            if results["embeddings"]:
                print(f"  Embedding Dimension: {len(results['embeddings'][0])}")
            print()
            
        except Exception as e:
            print(f"❌ Error getting stats: {str(e)}\n")
    
    def run_interactive(self):
        """Run interactive menu."""
        if not self.connect():
            return
        
        while True:
            print("\n" + "="*50)
            print("ChromaDB Viewer - Main Menu")
            print("="*50)
            print("1. List all collections")
            print("2. Select collection")
            print("3. View all chunks")
            print("4. View specific chunk")
            print("5. Search chunks by text")
            print("6. Get collection statistics")
            print("7. Exit")
            print("="*50)
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                self.list_collections()
            
            elif choice == "2":
                if self.list_collections():
                    name = input("Enter collection name: ").strip()
                    self.select_collection(name)
            
            elif choice == "3":
                self.view_all_chunks()
            
            elif choice == "4":
                if not self.collection:
                    print("❌ Please select a collection first\n")
                else:
                    try:
                        chunk_num = int(input("Enter chunk number: ").strip())
                        self.view_chunk(chunk_num)
                    except ValueError:
                        print("❌ Please enter a valid number\n")
            
            elif choice == "5":
                if not self.collection:
                    print("❌ Please select a collection first\n")
                else:
                    query = input("Enter search term: ").strip()
                    if query:
                        self.search_chunks(query)
            
            elif choice == "6":
                self.get_stats()
            
            elif choice == "7":
                print("\n👋 Goodbye!\n")
                break
            
            else:
                print("❌ Invalid choice. Please try again.\n")


if __name__ == "__main__":
    viewer = ChromaDBViewer()
    viewer.run_interactive()
