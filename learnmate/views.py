from django.shortcuts import render
from openai import OpenAI
import requests

# ✅ Initialize OpenAI client
client = OpenAI(api_key="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")  # <-- Replace with your real API key

# ✅ Generate Summary
def generate_summary(notes):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant that writes short, clear summaries."},
                {"role": "user", "content": f"Summarize these notes in 5 concise bullet points:\n{notes}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"

# ✅ Generate Flashcards
def generate_flashcards(notes):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a flashcard generator."},
                {"role": "user", "content": f"Create 5 flashcards from these notes in 'Q: ... | A: ...' format:\n{notes}"}
            ]
        )
        cards_text = response.choices[0].message.content.strip()
        return cards_text.split("\n")
    except Exception as e:
        return [f"Error generating flashcards: {e}"]

# ✅ Generate Quiz
def generate_quiz(notes):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a quiz generator that creates short quizzes."},
                {"role": "user", "content": f"Create 5 quiz questions (with 4 options each, mark correct answer) based on:\n{notes}"}
            ]
        )
        quiz_text = response.choices[0].message.content.strip()
        return quiz_text.split("\n")
    except Exception as e:
        return [f"Error generating quiz: {e}"]

# ✅ Fetch YouTube Videos
def get_youtube_videos(query):
    try:
        YT_API_KEY = "YOUR_YOUTUBE_API_KEY"  # <-- Replace with your YouTube API key
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=4&q={query}&key={YT_API_KEY}"
        response = requests.get(search_url)
        data = response.json()

        videos = []
        for item in data.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            })
        return videos
    except Exception as e:
        return [{"title": f"Error fetching videos: {e}", "url": "#"}]

# ✅ Main View
def learnmate_view(request):
    summary = flashcards = quiz = videos = None

    if request.method == "POST":
        notes = request.POST.get("notes")
        if notes:
            summary = generate_summary(notes)
            flashcards = generate_flashcards(notes)
            quiz = generate_quiz(notes)
            videos = get_youtube_videos(notes)

    return render(request, "learnmate.html", {
        "summary": summary,
        "flashcards": flashcards,
        "quiz": quiz,
        "videos": videos,
    })
