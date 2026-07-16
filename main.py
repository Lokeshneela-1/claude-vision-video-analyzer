#!/usr/bin/env python3
"""
Claude Vision Video Analyzer - Main Entry Point

A production-ready tool for extracting and analyzing video frames using Claude's Vision API.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from analyzer import VideoAnalyzer
from utils import setup_logging, print_header, print_success, print_error, print_info

logger = setup_logging()


def main():
    """Main entry point for the video analyzer CLI."""
    
    parser = argparse.ArgumentParser(
        description="Extract frames from videos and analyze them using Claude's Vision API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python main.py --video sample.mp4
  
  # Custom output directory
  python main.py --video sample.mp4 --output results
  
  # Extract every 5 seconds
  python main.py --video sample.mp4 --interval 5
  
  # Skip frame extraction (reuse existing)
  python main.py --video sample.mp4 --skip-extract
  
  # Custom analysis prompt
  python main.py --video sample.mp4 --prompt "Describe the main action in each frame"
        """
    )
    
    parser.add_argument(
        "--video",
        type=str,
        required=False,
        help="Path to input video file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_frames",
        help="Output directory for frames and analysis (default: output_frames)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Interval between frames in seconds (default: 2.0)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-5-sonnet-20241022",
        help="Claude model to use (default: claude-3-5-sonnet-20241022)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Custom analysis prompt (optional)"
    )
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="Skip frame extraction and reuse existing frames"
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Maximum number of frames to process (optional)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    print_header("Claude Vision Video Analyzer")
    
    # Validate inputs
    if not args.video and not args.skip_extract:
        print_error("--video argument is required (or use --skip-extract to reuse existing frames)")
        parser.print_help()
        sys.exit(1)
    
    if args.video and not Path(args.video).exists():
        print_error(f"Video file not found: {args.video}")
        sys.exit(1)
    
    # Initialize analyzer
    try:
        from analyzer import VideoAnalyzer
        print_info(f"Using Claude Vision Analyzer")
        
        analyzer = VideoAnalyzer(
            output_dir=args.output,
            frame_interval=args.interval,
            model=args.model,
            verbose=args.verbose
        )
    except ValueError as e:
        print_error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Run analysis
    try:
        print_info(f"Starting video analysis...")
        if args.video:
            print_info(f"Video: {args.video}")
        print_info(f"Output: {args.output}")
        print_info(f"Frame interval: {args.interval}s")
        print_info(f"Model: {args.model}\n")
        
        results = analyzer.analyze(
            video_path=args.video,
            skip_extraction=args.skip_extract,
            custom_prompt=args.prompt,
            max_frames=args.max_frames
        )
        
        # Display results
        print_success(f"\n✅ Analysis complete!")
        print_info(f"Total frames processed: {len(results['frames'])}")
        print_info(f"Processing time: {results.get('processing_time_seconds', 0):.2f}s")
        print_info(f"Output saved to: {results['output_dir']}\n")
        
        # Display sample result
        if results['frames']:
            first_frame = results['frames'][0]
            print_info("First frame analysis sample:")
            print_info(f"  Frame: {first_frame.get('frame_file', 'N/A')}")
            print_info(f"  Timestamp: {first_frame.get('timestamp', 'N/A')}")
            print_info(f"  Analysis: {first_frame.get('analysis', 'N/A')[:100]}...\n")
        
        print_success(f"Results saved to: {results['output_dir']}/analysis_results.json")
        
    except KeyboardInterrupt:
        print_error("\n❌ Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Analysis failed: {e}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
