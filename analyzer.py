"""
Core video analysis module using Claude Vision API.
"""

import base64
import json
import logging
import os
import subprocess
from datetime import timedelta
from pathlib import Path
from time import time
from typing import Optional, List, Dict, Any

from anthropic import Anthropic
from PIL import Image

from utils import print_info, print_error, print_success

logger = logging.getLogger(__name__)


class VideoAnalyzer:
    """Analyzes video frames using Claude's Vision API."""
    
    # Claude Vision supported image types
    SUPPORTED_IMAGE_TYPES = ("image/jpeg", "image/png", "image/gif", "image/webp")
    DEFAULT_PROMPT = (
        "Please analyze this video frame. Describe:\n"
        "1. Main objects and people visible\n"
        "2. Actions being performed\n"
        "3. Setting and environment\n"
        "4. Any text visible\n"
        "5. Overall context and what's happening\n\n"
        "Be concise but detailed."
    )
    
    def __init__(
        self,
        output_dir: str = "output_frames",
        frame_interval: float = 2.0,
        model: str = "claude-3-5-sonnet-20241022",
        verbose: bool = False
    ):
        """
        Initialize the video analyzer.
        
        Args:
            output_dir: Directory to save frames and results
            frame_interval: Seconds between frames to extract
            model: Claude model to use for analysis
            verbose: Enable verbose logging
        """
        self.output_dir = Path(output_dir)
        self.frame_interval = frame_interval
        self.model = model
        self.verbose = verbose
        
        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please set it in .env file or environment."
            )
        self.client = Anthropic(api_key=api_key)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.verbose:
            logger.info(f"VideoAnalyzer initialized with model: {model}")
    
    def extract_frames(
        self,
        video_path: str,
        output_subdir: Path,
        max_frames: Optional[int] = None
    ) -> List[Path]:
        """
        Extract frames from video using FFmpeg.
        
        Args:
            video_path: Path to input video file
            output_subdir: Subdirectory for saving frames
            max_frames: Maximum number of frames to extract
            
        Returns:
            List of paths to extracted frame images
        """
        frames_dir = output_subdir / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        
        print_info(f"Extracting frames at {self.frame_interval}s intervals...")
        
        try:
            # FFmpeg command to extract frames
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-vf", f"fps=1/{self.frame_interval}",
                "-q:v", "2",  # High quality
                str(frames_dir / "frame_%04d.jpg")
            ]
            
            # Add filter to limit frames if specified
            if max_frames:
                cmd = [
                    "ffmpeg",
                    "-i", video_path,
                    "-vf", f"fps=1/{self.frame_interval},scale=-1:720",
                    "-q:v", "2",
                    "-frames:v", str(max_frames),
                    str(frames_dir / "frame_%04d.jpg")
                ]
            
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg error: {result.stderr}")
            
            # Collect extracted frames
            frames = sorted(frames_dir.glob("frame_*.jpg"))
            print_success(f"✓ Extracted {len(frames)} frames")
            
            return frames
            
        except FileNotFoundError:
            raise RuntimeError(
                "FFmpeg not found. Install it with:\n"
                "  macOS: brew install ffmpeg\n"
                "  Ubuntu: sudo apt-get install ffmpeg\n"
                "  Windows: choco install ffmpeg"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Frame extraction timed out (>5 minutes)")
        except Exception as e:
            raise RuntimeError(f"Frame extraction failed: {e}")
    
    def analyze_frame(
        self,
        frame_path: Path,
        custom_prompt: Optional[str] = None
    ) -> str:
        """
        Analyze a single frame using Claude Vision API.
        
        Args:
            frame_path: Path to frame image
            custom_prompt: Custom analysis prompt (optional)
            
        Returns:
            Analysis text from Claude
        """
        # Read and encode image
        with open(frame_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")
        
        # Determine media type
        media_type = "image/jpeg"
        if frame_path.suffix.lower() == ".png":
            media_type = "image/png"
        
        # Use custom prompt or default
        prompt = custom_prompt or self.DEFAULT_PROMPT
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Failed to analyze frame {frame_path}: {e}")
            raise
    
    def get_video_duration(self, video_path: str) -> float:
        """Get video duration in seconds using FFprobe."""
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1:nokey=1",
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return float(result.stdout.strip())
            return 0
            
        except Exception as e:
            logger.warning(f"Could not get video duration: {e}")
            return 0
    
    def seconds_to_timestamp(self, seconds: float) -> str:
        """Convert seconds to HH:MM:SS format."""
        delta = timedelta(seconds=int(seconds))
        return str(delta)
    
    def analyze(
        self,
        video_path: Optional[str] = None,
        skip_extraction: bool = False,
        custom_prompt: Optional[str] = None,
        max_frames: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Main analysis pipeline.
        
        Args:
            video_path: Path to input video file
            skip_extraction: Skip frame extraction and reuse existing frames
            custom_prompt: Custom analysis prompt
            max_frames: Maximum frames to analyze
            
        Returns:
            Analysis results dictionary
        """
        start_time = time()
        
        # Create output subdirectory
        if video_path:
            video_name = Path(video_path).stem
        else:
            video_name = "analysis"
        
        output_subdir = self.output_dir / video_name
        output_subdir.mkdir(parents=True, exist_ok=True)
        
        # Extract frames or load existing
        if skip_extraction:
            frames_dir = output_subdir / "frames"
            if not frames_dir.exists():
                raise ValueError(
                    f"No existing frames found in {frames_dir}. "
                    "Remove --skip-extract to extract frames."
                )
            frames = sorted(frames_dir.glob("frame_*.jpg"))
            if not frames:
                raise ValueError(f"No frames found in {frames_dir}")
            print_success(f"✓ Using existing frames ({len(frames)} frames)")
        else:
            if not video_path:
                raise ValueError("video_path required when not using --skip-extract")
            frames = self.extract_frames(video_path, output_subdir, max_frames)
        
        # Get video duration for timestamps
        duration = self.get_video_duration(video_path) if video_path else 0
        
        # Analyze frames
        print_info(f"\nAnalyzing frames with Claude {self.model}...")
        
        results_list = []
        for idx, frame_path in enumerate(frames, 1):
            # Skip frames beyond max_frames if specified
            if max_frames and idx > max_frames:
                break
            
            frame_num = idx
            timestamp_seconds = (idx - 1) * self.frame_interval
            timestamp = self.seconds_to_timestamp(timestamp_seconds)
            
            print_info(f"  [{idx}/{len(frames)}] Analyzing {frame_path.name}...", end="")
            
            try:
                analysis = self.analyze_frame(frame_path, custom_prompt)
                results_list.append({
                    "frame_number": frame_num,
                    "timestamp": timestamp,
                    "frame_file": frame_path.name,
                    "analysis": analysis
                })
                print(" ✓")
            except Exception as e:
                print(f" ✗ (Error: {e})")
                logger.error(f"Failed to analyze frame {idx}: {e}")
                results_list.append({
                    "frame_number": frame_num,
                    "timestamp": timestamp,
                    "frame_file": frame_path.name,
                    "analysis": f"Error: {e}"
                })
        
        processing_time = time() - start_time
        
        # Save results
        results = {
            "video_path": video_path or "N/A",
            "video_duration": duration,
            "total_frames": len(frames),
            "frames_analyzed": len(results_list),
            "frame_interval": self.frame_interval,
            "model": self.model,
            "custom_prompt_used": custom_prompt is not None,
            "processing_time_seconds": processing_time,
            "analysis_date": datetime.now().isoformat(),
            "frames": results_list,
            "output_dir": str(output_subdir)
        }
        
        # Save to JSON
        results_file = output_subdir / "analysis_results.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print_success(f"✓ Results saved to {results_file}")
        
        # Save summary
        summary_file = output_subdir / "summary.txt"
        with open(summary_file, "w") as f:
            f.write("Claude Vision Video Analyzer - Summary\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Video: {video_path or 'N/A'}\n")
            f.write(f"Duration: {self.seconds_to_timestamp(duration)}\n")
            f.write(f"Total Frames: {len(frames)}\n")
            f.write(f"Frames Analyzed: {len(results_list)}\n")
            f.write(f"Frame Interval: {self.frame_interval}s\n")
            f.write(f"Processing Time: {processing_time:.2f}s\n")
            f.write(f"Model: {self.model}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Frame-by-Frame Analysis:\n")
            f.write("-" * 50 + "\n\n")
            for frame_result in results_list:
                f.write(f"Frame {frame_result['frame_number']} ({frame_result['timestamp']}):\n")
                f.write(f"{frame_result['analysis']}\n\n")
        
        return results
