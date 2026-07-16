#!/usr/bin/env python3
"""
Example 1: Basic video analysis

This is the simplest example showing basic usage.
"""

from analyzer import VideoAnalyzer


def main():
    # Initialize the analyzer
    analyzer = VideoAnalyzer(
        output_dir="output_frames",
        frame_interval=2.0,  # Extract one frame every 2 seconds
        model="claude-3-5-sonnet-20241022"
    )
    
    # Analyze a video
    video_path = "sample.mp4"
    
    print(f"Analyzing: {video_path}")
    results = analyzer.analyze(video_path=video_path)
    
    print(f"\n✓ Analysis complete!")
    print(f"Total frames: {len(results['frames'])}")
    print(f"Processing time: {results['processing_time_seconds']:.2f}s")
    print(f"Results saved to: {results['output_dir']}")


if __name__ == "__main__":
    main()
