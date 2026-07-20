# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

The system scores each song against the user's preferences (favorite genre, mood, energy, valence, tempo, acousticness) and ranks them by total score.

**Data Flow Visualization:**

```
INPUT                  PROCESS                          OUTPUT
┌──────────────┐      ┌──────────────────────────────┐  ┌────────────────┐
│ User Prefs   │      │   SCORING LOOP               │  │  Top K Songs   │
│              │      │                              │  │  (Ranked)      │
│ • Genre      │──────│ For each song in CSV:        │──│  1. Song A     │
│ • Mood       │      │   score = genre(+2.0)        │  │  2. Song B     │
│ • Energy     │      │         + mood(+1.5)         │  │  3. Song C     │
│ • Valence    │      │         + energy(+1.0)       │  │  ...           │
│ • Tempo      │      │         + acoust(+0.8)       │  │                │
│ • Acoustic   │      │         + tempo(+0.7)        │  │  [Sorted by    │
│ • Dance      │      │         + valence(+0.5)      │  │   score DESC]  │
└──────────────┘      └──────────────────────────────┘  └────────────────┘
                               ↓
                        Max Score: ~7.9
                        (all matches)
```

**Algorithm Recipe (Point-Weighting Strategy):**
- **Genre Match**: +2.0 (exact match to favorite_genre)
- **Mood Match**: +1.5 (exact match to favorite_mood)
- **Energy Similarity**: +1.0 max (distance-based: 1.0 × (1 - |song_energy - target| / 0.4))
- **Acousticness Similarity**: +0.8 max (distance-based: 0.8 × (1 - |song_acoustic - target| / 0.25))
- **Tempo Similarity**: +0.7 max (distance-based: 0.7 × (1 - |song_tempo - target| / 40))
- **Valence Similarity**: +0.5 max (distance-based: 0.5 × (1 - |song_valence - target| / 0.4))
- **Max Possible Score**: ~7.9 (perfect match on all attributes)

**Design Rationale:**
- Genre is most reliable (stable, explicit), so weights highest
- Mood is specific but subjective, weights second
- Continuous attributes (energy, acousticness, tempo, valence) refine matches

Some prompts to answer:

- What features does each `Song` use in your system
  - Each song stores genre, mood, energy, tempo_bpm, valence, danceability, and acousticness so we can compare it to other songs.
- What information does your `UserProfile` store
  - The user profile stores favorite_genre, favorite_mood, target_energy, target_valence, target_tempo, target_danceability, and target_acousticness.
- How does your `Recommender` compute a score for each song
  - The recommender uses the point-weighting algorithm above: genre and mood are exact categorical matches (highest points), while energy, acousticness, tempo, and valence are scored based on distance from target values (continuous similarity).
- How do you choose which songs to recommend
  - We calculate scores for all songs, sort them from highest to lowest, and return the top k as recommendations with explanations.

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Run with: `python -m src.main` (from project root) or `python main.py` (from src/ directory)

```
======================================================================
Loaded 18 songs from catalog
User Profile: lofi + chill
======================================================================

TOP 5 RECOMMENDATIONS:

1. MIDNIGHT CODING
   Artist: LoRoom
   Score: 6.24
   Reasons: [Genre] lofi | [Mood] chill | Energy match: 0.95 | Acousticness: 0.67 | Tempo match: 0.66 | Valence: 0.45

2. LIBRARY RAIN
   Artist: Paper Lanterns
   Score: 5.88
   Reasons: [Genre] lofi | [Mood] chill | Energy match: 0.87 | Acousticness: 0.45 | Tempo match: 0.56 | Valence: 0.50

3. FOCUS FLOW
   Artist: LoRoom
   Score: 4.89
   Reasons: [Genre] lofi | Energy match: 1.00 | Acousticness: 0.70 | Tempo match: 0.70 | Valence: 0.49

4. SPACEWALK THOUGHTS
   Artist: Orbit Bloom
   Score: 3.24
   Reasons: [Mood] chill | Energy match: 0.70 | Acousticness: 0.26 | Tempo match: 0.35 | Valence: 0.44

5. DESERT BLUES
   Artist: Dusty Roads
   Score: 2.31
   Reasons: Energy match: 0.88 | Acousticness: 0.77 | Tempo match: 0.44 | Valence: 0.23
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

**System Biases:**

1. **Genre over-prioritization** — Genre receives +2.0 (highest weight), so a lofi song from a different artist/region could be ranked higher than a perfect energy/mood match from another genre. This system might ignore great songs just because they're not in the user's favorite genre.

2. **Categorical inflexibility** — Moods are treated as binary categories. A "focused" song might share 99% of "chill" characteristics but gets 0 points for mood match. Real mood is likely continuous.

3. **Feature-only matching** — The system only looks at audio features (energy, valence, acousticness, etc.) and ignores:
   - Lyrics and language
   - Artist popularity or cultural background
   - User's current context (time of day, weather, activity)
   - Recency and freshness of recommendations

4. **Small catalog problem** — Works fine with 18 songs but would struggle with millions. No collaborative filtering or semantic understanding.

5. **Homogenization risk** — Users who like lofi + chill will almost always get lofi + chill recommendations, limiting serendipitous discovery.

6. **Cold start** — New users without a history can't be scored effectively until they've rated songs.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



