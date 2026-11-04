#!/usr/bin/env python3
"""
Audio to SRT Converter
Converts audio files (MP3, WAV, M4A, FLAC, etc.) to SRT subtitle files with customizable formatting.
"""

import argparse
import os
import sys
from datetime import timedelta
from pathlib import Path


def check_environment():
    """Check if required packages and dependencies are installed."""
    missing_packages = []
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    
    # Check required packages
    try:
        import whisper
    except ImportError:
        missing_packages.append("openai-whisper")
    
    try:
        from pydub import AudioSegment
    except ImportError:
        missing_packages.append("pydub")
    
    # Check ffmpeg
    if os.system("which ffmpeg > /dev/null 2>&1") != 0:
        print("❌ ffmpeg is not installed")
        print("Install with: brew install ffmpeg")
        sys.exit(1)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print(f"Install with: pip install {' '.join(missing_packages)}")
        sys.exit(1)
    
    print("✅ Environment check passed")


def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    secs = int(td.total_seconds() % 60)
    millis = int((td.total_seconds() % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def split_text_by_chars(text, max_chars, min_chars=4):
    """
    Split text into chunks based on character limit.
    Respects word boundaries when possible.
    """
    if len(text) <= max_chars:
        return [text]
    
    lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        
        if len(test_line) <= max_chars:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # Ensure minimum character count
    result = []
    for line in lines:
        if len(line) >= min_chars:
            result.append(line)
        elif result:
            # Merge with previous line if too short
            result[-1] += " " + line
        else:
            result.append(line)
    
    return result


def merge_timeline_gaps(segments, gap_threshold=0.3):
    """
    Merge timeline gaps smaller than threshold.
    Extends previous segment end time to next segment start time.
    """
    if not segments:
        return segments
    
    merged = []
    for i, segment in enumerate(segments):
        if i == 0:
            merged.append(segment)
            continue
        
        prev_segment = merged[-1]
        gap = segment['start'] - prev_segment['end']
        
        if gap < gap_threshold:
            # Extend previous segment to current segment start
            prev_segment['end'] = segment['start']
        
        merged.append(segment)
    
    return merged


def transcribe_audio(audio_path, model_name="base"):
    """Transcribe audio file using Whisper."""
    import whisper
    
    print(f"Loading Whisper model: {model_name}")
    model = whisper.load_model(model_name)
    
    print(f"Transcribing: {audio_path}")
    result = model.transcribe(str(audio_path), language="zh", word_timestamps=True)
    
    return result


def generate_srt(segments, max_chars=22, min_chars=4):
    """Generate SRT content from transcription segments."""
    srt_content = []
    subtitle_index = 1
    
    for segment in segments:
        text = segment['text'].strip()
        if not text:
            continue
        
        # Split text into lines based on character limit
        lines = split_text_by_chars(text, max_chars, min_chars)
        
        # Calculate time per line
        duration = segment['end'] - segment['start']
        time_per_line = duration / len(lines)
        
        for i, line in enumerate(lines):
            start_time = segment['start'] + (i * time_per_line)
            end_time = segment['start'] + ((i + 1) * time_per_line)
            
            srt_content.append(f"{subtitle_index}")
            srt_content.append(f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}")
            srt_content.append(line)
            srt_content.append("")  # Empty line between subtitles
            
            subtitle_index += 1
    
    return "\n".join(srt_content)


def convert_audio_to_srt(audio_path, max_chars=22, output_path=None):
    """
    Main conversion function.
    
    Args:
        audio_path: Path to input audio file (MP3, WAV, M4A, FLAC, etc.)
        max_chars: Maximum characters per subtitle line (default: 22)
        output_path: Optional output path (default: origin.srt in same directory)
    """
    audio_path = Path(audio_path)
    
    # Validate input file
    if not audio_path.exists():
        print(f"❌ File not found: {audio_path}")
        sys.exit(1)
    
    # Check if file has a supported audio extension
    supported_formats = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.wma']
    if audio_path.suffix.lower() not in supported_formats:
        print(f"❌ Unsupported audio format: {audio_path.suffix}")
        print(f"Supported formats: {', '.join(supported_formats)}")
        sys.exit(1)
    
    # Set output path
    if output_path is None:
        output_path = audio_path.parent / "origin.srt"
    else:
        output_path = Path(output_path)
    
    # Transcribe audio
    result = transcribe_audio(audio_path)
    
    # Merge timeline gaps
    segments = merge_timeline_gaps(result['segments'])
    
    # Generate SRT content
    srt_content = generate_srt(segments, max_chars=max_chars)
    
    # Write to file
    output_path.write_text(srt_content, encoding='utf-8')
    print(f"✅ SRT file created: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert audio files to SRT subtitle file (supports MP3, WAV, M4A, FLAC, etc.)"
    )
    parser.add_argument(
        "audio_file",
        help="Path to input audio file (MP3, WAV, M4A, FLAC, etc.)"
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=22,
        help="Maximum characters per subtitle line (default: 22, minimum: 4)"
    )
    parser.add_argument(
        "--output",
        help="Output SRT file path (default: origin.srt in same directory)"
    )
    parser.add_argument(
        "--skip-check",
        action="store_true",
        help="Skip environment check"
    )
    
    args = parser.parse_args()
    
    # Validate max_chars
    if args.max_chars < 4:
        print("❌ max-chars must be at least 4")
        sys.exit(1)
    
    # Check environment
    if not args.skip_check:
        check_environment()
    
    # Convert
    convert_audio_to_srt(args.audio_file, args.max_chars, args.output)


if __name__ == "__main__":
    main()
