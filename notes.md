# Music Recommendation Systems: Data Types & Signals

## User Interaction Data (Collaborative Filtering Signals)

### Explicit Feedback
- **Likes/Saves** - Direct positive signals that a user loved a track
- **Ratings** - Numeric scores (1-5 stars) if the platform uses them
- **Playlist additions** - When users add songs to playlists, it signals preference

### Implicit Feedback
- **Listen history** - Every song played is a signal (even if not explicitly liked)
- **Skip behavior** - Skipping a song is a negative signal (user didn't like it)
- **Play duration** - How long a user listened before skipping matters (30 seconds vs. full play)
- **Repeat plays** - Playing the same song multiple times is a strong positive signal
- **Share behavior** - Sharing a song indicates high engagement

---

## Song Metadata & Audio Features (Content-Based Filtering Signals)

### Intrinsic Audio Features
- **Tempo** (BPM) - Speed of the song
- **Energy** - Intensity/loudness of the track
- **Danceability** - How suitable for dancing
- **Acousticness** - How acoustic vs. produced
- **Instrumentalness** - Amount of vocals vs. instruments
- **Liveness** - Whether it sounds like a live recording
- **Speechiness** - Amount of spoken words
- **Loudness** - Average decibel level
- **Mood/Valence** - Happiness/positivity of the track (0-1 scale)

### Categorical Metadata
- **Genre/Subgenre** - Rock, Hip-Hop, Electronic, Indie Folk, etc.
- **Artist** - Who created the song
- **Release date** - When the song came out (recency matters)
- **Producer/Songwriter** - Creative credits

### Semantic Tags
- **Mood descriptors** - "Chill," "Energetic," "Sad," "Party," "Focus"
- **Use case tags** - "Workout," "Sleep," "Commute," "Study"
- **Artist tags** - Genre associations, style descriptors

---

## User Profile Data

### Derived User Characteristics
- **User embedding/latent factors** - Learned representation of what the user likes
- **Genre preferences** - User's historical preference for different genres
- **Mood preferences** - What moods/tempos the user typically listens to
- **Time-of-day patterns** - What users listen to at different times
- **Seasonal patterns** - Different music preferences in summer vs. winter

---

## Contextual Data

### When/Where/How
- **Time of day** - Morning commute vs. late night affects recommendations
- **Day of week** - Weekend vs. weekday listening patterns
- **Season** - Affects music taste (holiday music, beach music, etc.)
- **Device type** - What they're listening on (headphones vs. car speaker)
- **Previous songs in session** - Context from what they just listened to

---

## How These Factor Into the Math

### In Collaborative Filtering (Matrix Factorization)
```
R ≈ P × Qᵀ

Where R[user, song] = interaction strength, which could be:
- 1 (liked/saved)
- -1 (skipped)
- 0.5 (partially played)
- 0 (never heard/ignored)
```

The matrix learns that users who like songs with similar latent factor patterns will enjoy similar recommendations.

### In Content-Based Filtering
```
Song A similarity to Song B = correlation of their feature vectors

e.g., If you loved a song with:
  - Tempo: 120 BPM
  - Energy: 0.8
  - Valence (mood): 0.9
  - Genre: "Indie Pop"

The system recommends songs with similar values
```

### In Hybrid Systems
Both signals feed into a unified neural network that learns how to weight them. The system might learn:
- "This user loves high-energy, upbeat songs (high valence)" → use mood/energy features
- "This user follows indie artists religiously" → use collaborative patterns from similar users
- "New user with no history" → rely more heavily on audio features and mood tags

---

## Why Playlist Data is Powerful

Playlists are particularly valuable because they encode:
1. **Curator intent** - Playlists are intentionally organized by mood/use case
2. **Sequence information** - Song order in a playlist reveals relationships
3. **User expression** - Public playlists show what users want to be associated with
4. **Thematic coherence** - Songs in the same playlist share something meaningful

This is why platforms like Spotify heavily weight playlist co-occurrence in their recommendations.

---

## Key Factors in Recommendations

### Most Important for This Project
- **Likes and skips** - Core user interaction signals
- **Tempo and mood** - Crucial content features that help with:
  - Explaining why recommendations were made (content-based rationale)
  - Handling cold-start scenarios where user history is sparse
  - Providing interpretable recommendations to users

### Why Implicit Over Explicit
Most production systems weight implicit feedback (skips, play duration) even more heavily than explicit likes, since:
- Implicit behavior is less biased
- Happens at massive scale
- More natural user expression

---

## Summary

For a music recommendation simulation:
- **User interactions** (likes, skips, play history) drive collaborative filtering
- **Song features** (tempo, energy, mood, genre) drive content-based filtering
- **Playlists** encode thematic relationships and user preferences
- **Context** (time, season, device) helps personalize recommendations
- **Hybrid systems** combine all these signals for robust recommendations
