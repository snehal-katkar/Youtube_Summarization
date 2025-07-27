import json
from urllib.parse import urlparse, parse_qs
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

def extract_video_id(url):
    """
    Extract the YouTube video ID from various URL formats.
    """
    parsed = urlparse(url)

    if "youtu.be" in parsed.netloc:
        return parsed.path.strip("/")

    if "youtube.com" in parsed.netloc:
        query_params = parse_qs(parsed.query)
        return query_params.get("v", [None])[0]

    return None

def get_best_transcript(video_id):
    """
    Tries to fetch the transcript in Hindi first, then English.
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for lang_code in ["hi", "en"]:
            try:
                return transcript_list.find_transcript([lang_code]).fetch()
            except Exception:
                continue
        raise NoTranscriptFound()
    except (TranscriptsDisabled, NoTranscriptFound):
        raise NoTranscriptFound()

@csrf_exempt
def summarize_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = data.get("url", "")
            video_id = extract_video_id(url)

            print("URL received:", url)
            print("Extracted video ID:", video_id)

            if not video_id:
                return JsonResponse({"error": "Invalid YouTube URL"}, status=400)

            transcript = get_best_transcript(video_id)

            # ✅ FIX: handle both dict and FetchedTranscriptSnippet objects
            full_text = " ".join(
                [line["text"] if isinstance(line, dict) else getattr(line, "text", "") for line in transcript]
            )

            summary = full_text[:500] + "..." if len(full_text) > 500 else full_text
            return JsonResponse({"summary": summary})

        except NoTranscriptFound:
            return JsonResponse({"error": "No transcript available in Hindi or English."}, status=404)
        except Exception as e:
            print(f"[Django Error] {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
