"""
Video Index - Stores and searches video analysis using vector embeddings
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class VideoIndex:
    """Manages searchable index of video analyses"""
    
    def __init__(self, persist_directory: str = "video_index_db"):
        """
        Initialize video index with vector database
        
        Args:
            persist_directory: Directory to store the database
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            persist_directory=str(self.persist_directory),
            anonymized_telemetry=False
        ))
        
        # Initialize embedding model
        print("Loading embedding model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection("video_analyses")
        except:
            self.collection = self.client.create_collection(
                name="video_analyses",
                metadata={"description": "Video frame analyses with embeddings"}
            )
        
        print(f"✅ Video index ready. Collection has {self.collection.count()} entries")
    
    def index_video_analysis(
        self,
        video_id: str,
        video_path: str,
        analysis_results: Dict[str, Any]
    ) -> None:
        """
        Index a complete video analysis for searching
        
        Args:
            video_id: Unique identifier for the video
            video_path: Path to the video file
            analysis_results: Complete analysis from VideoAnalyzer
        """
        print(f"\n📊 Indexing video analysis for: {video_id}")
        
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        # Index each frame analysis
        for idx, frame_data in enumerate(analysis_results.get('frames', [])):
            timestamp = frame_data.get('timestamp', f"frame_{idx}")
            analysis = frame_data.get('analysis', {})
            
            # Create searchable text from frame analysis
            text_parts = []
            if isinstance(analysis, dict):
                text_parts.append(f"At {timestamp}:")
                if 'objects' in analysis:
                    text_parts.append(f"Objects: {', '.join(analysis['objects'])}")
                if 'actions' in analysis:
                    text_parts.append(f"Actions: {analysis['actions']}")
                if 'setting' in analysis:
                    text_parts.append(f"Setting: {analysis['setting']}")
                if 'text_visible' in analysis:
                    text_parts.append(f"Text visible: {analysis['text_visible']}")
                if 'context' in analysis:
                    text_parts.append(f"Context: {analysis['context']}")
            else:
                # If analysis is a string
                text_parts.append(f"At {timestamp}: {analysis}")
            
            document_text = " ".join(text_parts)
            
            # Generate embedding
            embedding = self.embedder.encode(document_text).tolist()
            
            documents.append(document_text)
            embeddings.append(embedding)
            metadatas.append({
                'video_id': video_id,
                'video_path': video_path,
                'timestamp': timestamp,
                'frame_number': idx,
                'frame_path': frame_data.get('frame_path', ''),
                'indexed_at': datetime.now().isoformat()
            })
            ids.append(f"{video_id}_frame_{idx}")
        
        # Add to collection
        if documents:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Indexed {len(documents)} frames for video {video_id}")
        
        # Also index the overall summary if available
        if 'summary' in analysis_results:
            summary_text = f"Video summary: {analysis_results['summary']}"
            summary_embedding = self.embedder.encode(summary_text).tolist()
            
            self.collection.add(
                documents=[summary_text],
                embeddings=[summary_embedding],
                metadatas=[{
                    'video_id': video_id,
                    'video_path': video_path,
                    'timestamp': 'summary',
                    'frame_number': -1,
                    'indexed_at': datetime.now().isoformat()
                }],
                ids=[f"{video_id}_summary"]
            )
    
    def search(
        self,
        query: str,
        video_id: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant frames based on question
        
        Args:
            query: User's question or search query
            video_id: Optional - limit search to specific video
            top_k: Number of results to return
            
        Returns:
            List of relevant frame data with timestamps
        """
        # Generate query embedding
        query_embedding = self.embedder.encode(query).tolist()
        
        # Build where clause if video_id specified
        where = {"video_id": video_id} if video_id else None
        
        # Search collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'description': results['documents'][0][i],
                    'timestamp': results['metadatas'][0][i]['timestamp'],
                    'frame_number': results['metadatas'][0][i]['frame_number'],
                    'frame_path': results['metadatas'][0][i].get('frame_path', ''),
                    'video_id': results['metadatas'][0][i]['video_id'],
                    'video_path': results['metadatas'][0][i].get('video_path', ''),
                    'relevance_score': 1.0 - results['distances'][0][i]  # Convert distance to relevance
                })
        
        return formatted_results
    
    def get_video_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific video
        
        Args:
            video_id: Video identifier
            
        Returns:
            Video metadata or None
        """
        results = self.collection.get(
            where={"video_id": video_id},
            limit=1
        )
        
        if results['metadatas']:
            return results['metadatas'][0]
        return None
    
    def list_indexed_videos(self) -> List[str]:
        """
        Get list of all indexed video IDs
        
        Returns:
            List of video IDs
        """
        # Get all documents
        all_data = self.collection.get()
        
        # Extract unique video IDs
        video_ids = set()
        for metadata in all_data['metadatas']:
            video_ids.add(metadata['video_id'])
        
        return sorted(list(video_ids))
    
    def delete_video(self, video_id: str) -> None:
        """
        Remove all entries for a specific video
        
        Args:
            video_id: Video identifier to remove
        """
        # Get all IDs for this video
        results = self.collection.get(
            where={"video_id": video_id}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            print(f"✅ Deleted {len(results['ids'])} entries for video {video_id}")
