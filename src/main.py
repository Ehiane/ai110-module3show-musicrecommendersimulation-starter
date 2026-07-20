"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("../data/songs.csv")

    # Example user profile matching our scoring algorithm
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.60,
        "target_tempo": 80,
        "target_danceability": 0.60,
        "target_acousticness": 0.75,
    }

    print(f"\n{'='*70}")
    print(f"Loaded {len(songs)} songs from catalog")
    print(f"User Profile: {user_prefs['favorite_genre']} + {user_prefs['favorite_mood']}")
    print(f"{'='*70}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("TOP 5 RECOMMENDATIONS:\n")
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{i}. {song['title'].upper()}")
        print(f"   Artist: {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Reasons: {explanation}")
        print()


if __name__ == "__main__":
    main()
