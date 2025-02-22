from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from pytube import extract

def get_transcript(url, target_language="en"):
    video_id = extract.video_id(url)
    
    if not video_id:
        return "Invalid YouTube URL"
    
    try:
        # Fetch available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to fetch the transcript in the target language
        try:
            transcript = transcript_list.find_transcript([target_language])
        except:
            # If target language isn't available, get an auto-generated one
            transcript = transcript_list.find_generated_transcript(["es"])  # Default to Spanish if available
        
        # Translate if needed
        if target_language != transcript.language_code:
            transcript = transcript.translate(target_language)
        
        return "\n".join([entry["text"] for entry in transcript.fetch()])
    
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    url = input("Enter video url: ")
    print(get_transcript(url))