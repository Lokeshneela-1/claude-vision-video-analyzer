#!/usr/bin/env python3
"""
Example 2: Custom analysis prompt

Shows how to use custom prompts for specialized analysis.
"""

from analyzer import VideoAnalyzer


def main():
    analyzer = VideoAnalyzer(output_dir="output_frames")
    
    # Custom prompts for different use cases
    
    # Use case 1: Sports analysis
    sports_prompt = """
    Analyze this frame from a sports video. Identify:
    1. Athletes and their positions
    2. Equipment or sports gear visible
    3. Playing action or movements
    4. Score or game status if visible
    5. Notable plays or moments
    """
    
    # Use case 2: Security monitoring
    security_prompt = """
    Analyze this security footage frame. Report:
    1. Number and appearance of people
    2. Any suspicious or unusual behavior
    3. Objects of interest
    4. Entry/exit points used
    5. Time-sensitive observations
    """
    
    # Use case 3: Educational content
    education_prompt = """
    Analyze this educational video frame. Extract:
    1. Main topics or concepts being taught
    2. Any visible text, formulas, or diagrams
    3. Key learning points
    4. Visual aids or demonstrations
    5. Instructor actions or gestures
    """
    
    # Use case 4: Content description
    content_prompt = """
    Provide a detailed description of this video frame:
    1. Main subject/focus
    2. Background and setting
    3. Colors and lighting
    4. Any text or captions
    5. Emotional tone or atmosphere
    """
    
    # Analyze with custom prompt
    video_path = "sample.mp4"
    custom_prompt = content_prompt  # Choose one
    
    print(f"Analyzing video with custom prompt...")
    results = analyzer.analyze(
        video_path=video_path,
        custom_prompt=custom_prompt
    )
    
    print(f"✓ Analysis complete!")
    print(f"Frames analyzed: {len(results['frames'])}")
    
    # Display first frame analysis
    if results['frames']:
        first = results['frames'][0]
        print(f"\nFirst frame analysis:\n{first['analysis']}")


if __name__ == "__main__":
    main()
