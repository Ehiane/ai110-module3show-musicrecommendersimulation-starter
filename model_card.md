# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0** — A point-weighted music recommendation system that scores songs based on genre, mood, and audio feature similarity.

---

## 2. Intended Use  

VibeFinder generates top-5 personalized song recommendations for users based on their favorite genre, mood preference, and target audio characteristics (energy, valence, tempo, acousticness). It is designed for classroom exploration of recommender system biases and design tradeoffs, not production use. The system assumes users have a clear primary genre preference and can articulate their mood and energy targets.

---

## 3. How the Model Works  

VibeFinder scores each song by comparing it to the user's preferences using a point-weighting algorithm:
- **Genre Match** (+1.5): Exact match to favorite genre
- **Mood Match** (+1.0): Exact match to favorite mood
- **Continuous Attributes** (+1.5-0.8): Distance-based scores for energy, acousticness, tempo, and valence
- Songs are ranked by total score and top 5 are returned with explanations

The system started with genre weight +2.0 but was reduced to +1.5 after experiments showed it created echo chambers. The mood feature proved critical—removing it caused recommendations to collapse into pure genre sorting.

---

## 4. Data  

The dataset contains 18 songs across 15 genres with 10 moods represented. Each song includes: title, artist, genre, mood, energy (0-1), tempo_bpm, valence (0-1), danceability (0-1), and acousticness (0-1). 

**Data characteristics:**
- Total songs: 18
- Unique genres: 15 (13 genres have only 1 song)
- Dominant mood: "intense" (22%), followed by "happy"/"chill" (16.7% each)
- Energy range: 0.25-0.95 (avg 0.62)
- Acousticness range: 0.05-0.95 (avg 0.49)

No songs were added or removed from the provided dataset. The data represents an imbalanced, Western-centric catalog with heavy representation of electronic/pop and under-representation of world music genres.

---

## 5. Strengths  

The system works well for users whose preferences align with well-represented moods (intense, happy, chill) and has moderate genre diversity (lofi, pop, rock genres). The point-weighting approach successfully balances categorical preferences (genre/mood) with continuous audio features. Recommendations are interpretable—each suggestion includes a breakdown of why it scored well. The refined weights enable cross-genre discovery (e.g., blues songs for melancholic mood despite not being the favorite genre).

---

## 6. Limitations and Bias 

**Critical Filter Bubble: 13 out of 15 genres have only 1 song each.** Users who prefer rock, jazz, metal, or classical music are locked into single-song recommendations despite genre weight being reduced to +1.5. Once they get one recommendation from their genre, there are no alternatives. This violates basic recommender diversity principles.

**Mood Imbalance:** "Intense" mood represents 22% of the dataset while peaceful, relaxed, and energetic moods have only 5.6% each. Users seeking peaceful music are severely disadvantaged with limited recommendations. The exact-match mood system cannot find semantically similar alternatives (e.g., "peaceful" user cannot get "relaxed" song substitutes).

**Energy Clustering Gap:** Only 27.8% of songs fall in the mid-energy range (0.4-0.6). Users targeting moderate energy face algorithmic disadvantage—they have fewer songs to match against, resulting in lower scores and less diverse recommendations. Extreme energy preferences (very low/high) have better catalog coverage.

**Cold Start Problem:** New users without a history cannot be scored on liked_songs similarity. They can only be matched on explicit preferences, limiting recommendation quality until they rate multiple songs.

**Acoustic Preference Blindness:** The system ignores user's acousticness preference during exact mood matching. A user wanting "chill + acoustic" might get an electronic "chill" song with 0.05 acousticness just because it has the mood match.

---

## 7. Evaluation  

We tested four diverse user profiles: Chill Lofi (well-represented), High-Energy Pop (well-represented), Deep Intense Rock (single song bottleneck), and Melancholic Jazz (single song bottleneck). The system performed well for lofi/pop users but failed gracefully for rock/jazz users by returning the single available song. 

We ran two experiments: (1) Weight investigation showing genre=2.0 caused echo chambers, justifying reduction to 1.5, and (2) Feature removal showing mood matching is critical—removing it flipped rankings back to pure genre sorting. Surprising finding: even at weight 1.5, genre still dominates for users with underrepresented preferences.

---

## 8. Future Work  

(1) **Genre Expansion:** Add 3-5 songs per genre to eliminate single-song filter bubbles.  
(2) **Fuzzy Mood Matching:** Replace exact mood matching with semantic similarity (e.g., "peaceful" ≈ "relaxed").  
(3) **Collaborative Filtering:** Use user-user similarity to handle cold start and discover cross-genre tastes.  
(4) **Hybrid Scoring:** Combine audio features with collaborative signals for better diversity.

---

## 9. Personal Reflection  

Building this recommender revealed that data quality matters as much as algorithm design. Even with refined weights, a 13:1 genre imbalance creates hard walls that no weighting scheme can overcome. I learned that "fairness" in recommendations isn't about treating all users equally—it's about having enough representation for all user preferences in the data. The experiments showed that features (like mood) that seem minor can be essential for system behavior. The most surprising finding was how much the mood feature enables serendipity—without it, the system becomes a genre filter, not a recommender. This experience changed how I evaluate real-world recommenders like Spotify: I now notice dataset representation issues and think critically about which features drive recommendations.
