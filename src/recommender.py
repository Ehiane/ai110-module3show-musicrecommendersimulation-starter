from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_tempo: float
    target_danceability: float
    target_acousticness: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return as list of dictionaries."""
    import csv
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song based on user preferences, returning score and reasoning."""
    score = 0.0
    reasons = []

    # Genre match: +1.5 (reduced from 2.0 to allow cross-genre discovery)
    if song['genre'] == user_prefs['favorite_genre']:
        score += 1.5
        reasons.append(f"[Genre] {song['genre']}")

    # Mood match: +1.0 (reduced from 1.5 to balance with continuous attributes)
    if song['mood'] == user_prefs['favorite_mood']:
        score += 1.0
        reasons.append(f"[Mood] {song['mood']}")

    # Energy similarity: +1.5 max (increased from 1.0 for better musical matching)
    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    energy_score = max(0, 1.5 * (1 - energy_diff / 0.4))
    score += energy_score
    reasons.append(f"Energy match: {energy_score:.2f}")

    # Acousticness similarity: +1.2 max (increased from 0.8)
    acousticness_diff = abs(song['acousticness'] - user_prefs['target_acousticness'])
    acousticness_score = max(0, 1.2 * (1 - acousticness_diff / 0.25))
    score += acousticness_score
    reasons.append(f"Acousticness: {acousticness_score:.2f}")

    # Tempo similarity: +1.0 max (increased from 0.7)
    tempo_diff = abs(song['tempo_bpm'] - user_prefs['target_tempo'])
    tempo_score = max(0, 1.0 * (1 - tempo_diff / 40))
    score += tempo_score
    reasons.append(f"Tempo match: {tempo_score:.2f}")

    # Valence similarity: +0.8 max (increased from 0.5)
    valence_diff = abs(song['valence'] - user_prefs['target_valence'])
    valence_score = max(0, 0.8 * (1 - valence_diff / 0.4))
    score += valence_score
    reasons.append(f"Valence: {valence_score:.2f}")

    return (score, reasons)


def score_song_alt(user_prefs: Dict, song: Dict, weights: Dict) -> Tuple[float, List[str]]:
    """Score a song with custom weights. Used for weight experimentation."""
    score = 0.0
    reasons = []

    if song['genre'] == user_prefs['favorite_genre']:
        score += weights['genre']
        reasons.append(f"[Genre] {song['genre']}")

    if song['mood'] == user_prefs['favorite_mood']:
        score += weights['mood']
        reasons.append(f"[Mood] {song['mood']}")

    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    energy_score = max(0, weights['energy'] * (1 - energy_diff / 0.4))
    score += energy_score
    reasons.append(f"Energy: {energy_score:.2f}")

    acousticness_diff = abs(song['acousticness'] - user_prefs['target_acousticness'])
    acousticness_score = max(0, weights['acousticness'] * (1 - acousticness_diff / 0.25))
    score += acousticness_score
    reasons.append(f"Acoustic: {acousticness_score:.2f}")

    tempo_diff = abs(song['tempo_bpm'] - user_prefs['target_tempo'])
    tempo_score = max(0, weights['tempo'] * (1 - tempo_diff / 40))
    score += tempo_score
    reasons.append(f"Tempo: {tempo_score:.2f}")

    valence_diff = abs(song['valence'] - user_prefs['target_valence'])
    valence_score = max(0, weights['valence'] * (1 - valence_diff / 0.4))
    score += valence_score
    reasons.append(f"Valence: {valence_score:.2f}")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return top k recommendations with explanations."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))

    # Sort by score descending and return top k
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
