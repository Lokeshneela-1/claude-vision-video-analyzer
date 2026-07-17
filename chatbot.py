"""
Video Chatbot - Interactive Q&A for analyzed videos with conversation memory
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from anthropic import Anthropic

from video_index import VideoIndex


class ConversationMemory:
    """Stores and retrieves conversation history"""
    
    def __init__(self, storage_dir: str = "conversations"):
        """
        Initialize conversation memory
        
        Args:
            storage_dir: Directory to store conversation logs
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.conversations = {}  # In-memory cache: {video_id: [messages]}
    
    def add_message(self, video_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Add a message to conversation history
        
        Args:
            video_id: Video identifier
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata (timestamps, frame refs, etc.)
        """
        if video_id not in self.conversations:
            self.conversations[video_id] = []
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.conversations[video_id].append(message)
        
        # Save to disk
        self._save_conversation(video_id)
    
    def get_conversation(self, video_id: str) -> List[Dict]:
        """
        Get full conversation history for a video
        
        Args:
            video_id: Video identifier
            
        Returns:
            List of messages
        """
        if video_id not in self.conversations:
            # Try to load from disk
            self._load_conversation(video_id)
        
        return self.conversations.get(video_id, [])
    
    def get_context_messages(self, video_id: str, last_n: int = 5) -> List[Dict]:
        """
        Get recent messages for context
        
        Args:
            video_id: Video identifier
            last_n: Number of recent messages to return
            
        Returns:
            Recent messages
        """
        conversation = self.get_conversation(video_id)
        return conversation[-last_n:] if conversation else []
    
    def _save_conversation(self, video_id: str):
        """Save conversation to disk"""
        filepath = self.storage_dir / f"{video_id}_conversation.json"
        with open(filepath, 'w') as f:
            json.dump(self.conversations[video_id], f, indent=2)
    
    def _load_conversation(self, video_id: str):
        """Load conversation from disk"""
        filepath = self.storage_dir / f"{video_id}_conversation.json"
        if filepath.exists():
            with open(filepath, 'r') as f:
                self.conversations[video_id] = json.load(f)


class VideoChatbot:
    """Interactive chatbot for querying analyzed videos"""
    
    def __init__(self, video_index: VideoIndex, api_key: Optional[str] = None):
        """
        Initialize video chatbot
        
        Args:
            video_index: VideoIndex instance for searching
            api_key: Anthropic API key (or from environment)
        """
        self.index = video_index
        self.memory = ConversationMemory()
        
        # Initialize Claude client
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        
        self.claude = Anthropic(api_key=api_key)
        self.model = os.getenv("MODEL", "claude-3-5-sonnet-20241022")
    
    def answer_question(
        self,
        video_id: str,
        question: str,
        use_conversation_history: bool = True
    ) -> Dict[str, Any]:
        """
        Answer a question about the video using indexed data and AI
        
        Args:
            video_id: Video identifier
            question: User's question
            use_conversation_history: Whether to use previous conversation context
            
        Returns:
            Dict with answer, relevant timestamps, and frame references
        """
        print(f"\n💬 Question: {question}")
        
        # 1. Search for relevant frames
        relevant_frames = self.index.search(
            query=question,
            video_id=video_id,
            top_k=5
        )
        
        if not relevant_frames:
            return {
                'answer': "I couldn't find any relevant information in the video analysis for that question.",
                'timestamps': [],
                'frames': [],
                'confidence': 'low'
            }
        
        # 2. Build context from relevant frames
        context_parts = ["Video Analysis Context:\n"]
        timestamps = []
        frame_paths = []
        
        for frame in relevant_frames:
            timestamp = frame['timestamp']
            description = frame['description']
            context_parts.append(f"[{timestamp}] {description}")
            timestamps.append(timestamp)
            if frame.get('frame_path'):
                frame_paths.append(frame['frame_path'])
        
        context = "\n".join(context_parts)
        
        # 3. Get conversation history if enabled
        conversation_context = ""
        if use_conversation_history:
            recent_messages = self.memory.get_context_messages(video_id, last_n=6)
            if recent_messages:
                conversation_context = "\n\nPrevious Conversation:\n"
                for msg in recent_messages:
                    role = "User" if msg['role'] == 'user' else "Assistant"
                    conversation_context += f"{role}: {msg['content']}\n"
        
        # 4. Build prompt for Claude
        prompt = f"""You are a helpful video analysis assistant. A user is asking questions about a video that has been analyzed.

{context}
{conversation_context}

User's Question: {question}

Please provide a clear, concise answer based on the video analysis context. Include specific timestamps when relevant. If the context doesn't contain enough information to answer fully, say so clearly.

Format your response naturally, mentioning timestamps like "At 00:01:45" or "Around the 2-minute mark"."""
        
        # 5. Get answer from Claude
        try:
            response = self.claude.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            
            answer = response.content[0].text
            
            # 6. Store in conversation memory
            self.memory.add_message(video_id, 'user', question)
            self.memory.add_message(
                video_id,
                'assistant',
                answer,
                metadata={
                    'timestamps': timestamps,
                    'frame_paths': frame_paths,
                    'relevance_scores': [f['relevance_score'] for f in relevant_frames]
                }
            )
            
            return {
                'answer': answer,
                'timestamps': timestamps,
                'frames': frame_paths,
                'confidence': 'high' if relevant_frames[0]['relevance_score'] > 0.7 else 'medium',
                'relevant_frames': relevant_frames[:3]  # Top 3 most relevant
            }
            
        except Exception as e:
            print(f"❌ Error getting answer from Claude: {e}")
            return {
                'answer': f"Error processing question: {str(e)}",
                'timestamps': timestamps,
                'frames': frame_paths,
                'confidence': 'error'
            }
    
    def get_video_summary(self, video_id: str) -> str:
        """
        Get a conversational summary of what's in the video
        
        Args:
            video_id: Video identifier
            
        Returns:
            Summary text
        """
        # Search for summary or get general overview
        results = self.index.search(
            query="overall summary of video",
            video_id=video_id,
            top_k=10
        )
        
        if not results:
            return "No analysis available for this video yet."
        
        # Build comprehensive context
        context = "Video Analysis:\n"
        for result in results:
            context += f"- {result['description']}\n"
        
        # Ask Claude to summarize
        prompt = f"""Based on this video analysis data, provide a friendly summary of what happens in the video. 
Include key events, people, objects, and actions. Make it conversational and helpful.

{context}

Summary:"""
        
        try:
            response = self.claude.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def suggest_questions(self, video_id: str) -> List[str]:
        """
        Suggest relevant questions users can ask about the video
        
        Args:
            video_id: Video identifier
            
        Returns:
            List of suggested questions
        """
        # Get sample frames
        results = self.index.search(
            query="main activity people objects",
            video_id=video_id,
            top_k=5
        )
        
        if not results:
            return [
                "What happens in the video?",
                "What objects are visible?",
                "Are there any people in the video?"
            ]
        
        # Analyze content to suggest questions
        context = "\n".join([r['description'] for r in results])
        
        prompt = f"""Based on this video analysis, suggest 5 interesting questions someone might want to ask:

{context}

Provide 5 specific questions (one per line):"""
        
        try:
            response = self.claude.messages.create(
                model=self.model,
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}]
            )
            
            questions = response.content[0].text.strip().split('\n')
            # Clean up questions (remove numbers, bullets)
            cleaned = []
            for q in questions:
                q = q.strip()
                # Remove leading numbers/bullets
                while q and (q[0].isdigit() or q[0] in ['.', '-', '*', ')']):
                    q = q[1:].strip()
                if q:
                    cleaned.append(q)
            
            return cleaned[:5]
            
        except Exception as e:
            return [
                "What happens in the video?",
                "When do key events occur?",
                "What objects or people appear?",
                "Are there any notable actions?",
                "What is the overall context?"
            ]
    
    def export_conversation(self, video_id: str, output_path: Optional[str] = None) -> str:
        """
        Export conversation history to text file
        
        Args:
            video_id: Video identifier
            output_path: Optional output file path
            
        Returns:
            Path to saved file
        """
        conversation = self.memory.get_conversation(video_id)
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"conversation_{video_id}_{timestamp}.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Video Analysis Conversation\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for msg in conversation:
                role = "👤 User" if msg['role'] == 'user' else "🤖 Assistant"
                timestamp = msg['timestamp']
                content = msg['content']
                
                f.write(f"{role} [{timestamp}]:\n")
                f.write(f"{content}\n\n")
                
                # Add metadata if available
                if msg.get('metadata') and msg['metadata'].get('timestamps'):
                    f.write(f"  📍 Referenced timestamps: {', '.join(msg['metadata']['timestamps'])}\n\n")
        
        return output_path
