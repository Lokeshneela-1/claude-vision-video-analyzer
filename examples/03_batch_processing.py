#!/usr/bin/env python3
"""
Example 3: Batch processing and result analysis

Shows how to process multiple videos and analyze results.
"""

import json
from pathlib import Path
from analyzer import VideoAnalyzer


def process_multiple_videos(video_files):
    """Process multiple video files."""
    analyzer = VideoAnalyzer(
        output_dir="batch_output",
        frame_interval=3.0,  # Lower resolution for batch
        model="claude-3-5-sonnet-20241022"
    )
    
    results = {}
    
    for video_file in video_files:
        if not Path(video_file).exists():
            print(f"⚠️  Skipping {video_file} - file not found")
            continue
        
        print(f"\n📹 Processing: {video_file}")
        try:
            analysis_results = analyzer.analyze(video_path=video_file)
            results[video_file] = analysis_results
            print(f"✓ Completed: {video_file}")
        except Exception as e:
            print(f"✗ Failed: {video_file} - {e}")
            results[video_file] = {"error": str(e)}
    
    return results


def analyze_results(results):
    """Analyze the results from batch processing."""
    print("\n" + "="*60)
    print("BATCH PROCESSING SUMMARY")
    print("="*60 + "\n")
    
    successful = 0
    total_frames = 0
    total_time = 0
    
    for video, result in results.items():
        if "error" in result:
            print(f"✗ {video}: Error - {result['error']}")
        else:
            successful += 1
            frames = len(result.get('frames', []))
            proc_time = result.get('processing_time_seconds', 0)
            
            total_frames += frames
            total_time += proc_time
            
            print(f"✓ {video}")
            print(f"  Frames: {frames}")
            print(f"  Time: {proc_time:.2f}s")
            
            # Show interesting findings
            if result['frames']:
                print(f"  Analysis preview:")
                for frame in result['frames'][:2]:
                    analysis = frame['analysis'][:80]
                    print(f"    - {analysis}...")
    
    print(f"\n{'='*60}")
    print(f"Total successful: {successful}/{len(results)}")
    print(f"Total frames: {total_frames}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Avg time per video: {total_time/successful:.2f}s" if successful > 0 else "")


def search_results(results, keyword):
    """Search for keyword in analysis results."""
    print(f"\n🔍 Searching for: '{keyword}'")
    print("="*60 + "\n")
    
    matches = []
    
    for video, result in results.items():
        if "error" in result:
            continue
        
        for frame in result.get('frames', []):
            if keyword.lower() in frame['analysis'].lower():
                matches.append({
                    'video': video,
                    'frame': frame['frame_number'],
                    'timestamp': frame['timestamp'],
                    'analysis': frame['analysis']
                })
    
    if matches:
        print(f"Found {len(matches)} matches:\n")
        for match in matches:
            print(f"📹 {match['video']}")
            print(f"   Frame {match['frame']} at {match['timestamp']}")
            print(f"   {match['analysis'][:100]}...\n")
    else:
        print(f"No matches found for '{keyword}'")


def main():
    # Example 1: Analyze single video
    print("EXAMPLE 1: Single Video Analysis")
    print("="*60)
    
    analyzer = VideoAnalyzer(frame_interval=2.0)
    
    # Assuming you have a sample.mp4 file
    video = "sample.mp4"
    if Path(video).exists():
        results = analyzer.analyze(video_path=video, max_frames=10)
        print(f"✓ Analyzed {len(results['frames'])} frames")
    else:
        print(f"⚠️  {video} not found. Create one with:")
        print(f"   ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=10 -f lavfi -i sine=f=1000:d=10 {video}")
    
    # Example 2: Batch processing
    print("\n\nEXAMPLE 2: Batch Processing")
    print("="*60)
    
    # List of videos to process
    # Replace with your actual video files
    videos_to_process = [
        "sample.mp4",
        # "video2.mp4",
        # "video3.mp4",
    ]
    
    batch_results = process_multiple_videos(videos_to_process)
    analyze_results(batch_results)
    
    # Example 3: Search results
    print("\n\nEXAMPLE 3: Search Results")
    print("="*60)
    search_results(batch_results, "person")


if __name__ == "__main__":
    main()
