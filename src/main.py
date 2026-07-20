"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, score_song_no_mood


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    """Print recommendations for a user profile."""
    print(f"\n{'='*70}")
    print(f"PROFILE: {profile_name}")
    print(f"Genre: {user_prefs['favorite_genre']} | Mood: {user_prefs['favorite_mood']}")
    print(f"Energy: {user_prefs['target_energy']} | Valence: {user_prefs['target_valence']}")
    print(f"{'='*70}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{i}. {song['title'].upper()}")
        print(f"   Artist: {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Reasons: {explanation}")
        print()


def print_feature_removal_experiment(profile_name: str, user_prefs: dict, songs: list) -> None:
    """Compare recommendations WITH and WITHOUT mood matching."""
    print(f"\n{'='*70}")
    print(f"EXPERIMENT: Feature Removal (No Mood) - {profile_name}")
    print(f"{'='*70}\n")

    # WITH mood (current)
    recommendations_with = recommend_songs(user_prefs, songs, k=3)

    # WITHOUT mood (experiment)
    scored_without = [(song, score_song_no_mood(user_prefs, song))
                      for song in songs]
    scored_without.sort(key=lambda x: x[1][0], reverse=True)
    recommendations_without = scored_without[:3]

    print("WITH MOOD MATCHING (Current):")
    for i, (song, score, reasons) in enumerate(recommendations_with, 1):
        print(f"{i}. {song['title']} ({song['genre']}/{song['mood']}) - {score:.2f}")

    print("\nWITHOUT MOOD MATCHING (Experiment):")
    for i, (song, (score, reasons)) in enumerate(recommendations_without, 1):
        print(f"{i}. {song['title']} ({song['genre']}/{song['mood']}) - {score:.2f}")

    # Identify differences
    with_titles = {rec[0]['id'] for rec in recommendations_with}
    without_titles = {rec[0]['id'] for rec in recommendations_without}

    if with_titles == without_titles:
        print("\n[OK] NO CHANGE - Top 3 remain the same")
    else:
        print(f"\n[CHANGED] RANKINGS DIFFERENT - {len(with_titles - without_titles)} song(s) replaced")
    print()


def main() -> None:
    songs = load_songs("../data/songs.csv")

    print(f"\nLoaded {len(songs)} songs from catalog\n")

    # Profile 1: Chill Lofi
    profile1 = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.60,
        "target_tempo": 80,
        "target_danceability": 0.60,
        "target_acousticness": 0.75,
    }
    print_recommendations("Chill Lofi", profile1, songs)

    # Profile 2: High-Energy Pop
    profile2 = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_valence": 0.80,
        "target_tempo": 125,
        "target_danceability": 0.85,
        "target_acousticness": 0.20,
    }
    print_recommendations("High-Energy Pop", profile2, songs)

    # Profile 3: Deep Intense Rock
    profile3 = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.40,
        "target_tempo": 150,
        "target_danceability": 0.70,
        "target_acousticness": 0.10,
    }
    print_recommendations("Deep Intense Rock", profile3, songs)

    # Profile 4: Melancholic Jazz (edge case)
    profile4 = {
        "favorite_genre": "jazz",
        "favorite_mood": "melancholic",
        "target_energy": 0.45,
        "target_valence": 0.40,
        "target_tempo": 95,
        "target_danceability": 0.50,
        "target_acousticness": 0.85,
    }
    print_recommendations("Melancholic Jazz", profile4, songs)

    # Weight comparison for Jazz profile
    print_feature_removal_experiment("Melancholic Jazz (mood removal test)", profile4, songs)


if __name__ == "__main__":
    main()
