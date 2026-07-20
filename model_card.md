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

**Profiles Tested:**
1. Chill Lofi (genre=lofi, mood=chill, energy=0.40, acousticness=0.75) — well-represented in data
2. High-Energy Pop (genre=pop, mood=happy, energy=0.85, acousticness=0.20) — well-represented in data
3. Deep Intense Rock (genre=rock, mood=intense, energy=0.90, acousticness=0.10) — rock: 1 song only
4. Melancholic Jazz (genre=jazz, mood=melancholic, energy=0.45, acousticness=0.85) — jazz: 1 song only

**Surprising Findings:**

The most striking surprise was how differently the system behaves based on dataset representation. Well-represented users (lofi, pop) received diverse top-5 recommendations with clear reasoning. Underrepresented users (rock, jazz) hit hard walls—Jazz user's #1 recommendation was the only jazz song available, forcing a compromise: they got coffee shop stories (jazz/relaxed) instead of matching mood.

**Profile Comparison 1: Chill Lofi vs High-Energy Pop**

Both profiles are well-represented (3 lofi songs, 2 pop songs) and both ranked their target genre first. However, the energy preference created a clear split: Chill Lofi received low-energy songs (0.35-0.42 energy range), while High-Energy Pop received high-energy songs (0.76-0.93 energy). This makes perfect sense—the system correctly identified that "chill" mood requires relaxing music while "happy" mood pairs with energetic tracks. The continuous energy attribute worked as designed to differentiate within genres.

**Profile Comparison 2: High-Energy Pop vs Deep Intense Rock**

Both users want high energy (0.85 vs 0.90) and low acousticness (0.20 vs 0.10), suggesting they prefer processed, synthesized sounds. However, their outputs diverged completely. Pop user got 5 diverse songs; Rock user got 1 rock song (Storm Runner) then fell back to pop/hip-hop songs. This reveals the dataset imbalance: only 1 rock song exists, so even with matching preferences, rock users cannot escape their genre island. Pop user never encounters this problem because pop has 2 songs minimum.

**Profile Comparison 3: Chill Lofi vs Melancholic Jazz**

Both target low-to-moderate energy (0.40 vs 0.45) and high acousticness (0.75 vs 0.85), but different moods: chill vs melancholic. The rankings flipped: Chill user got "Midnight Coding" (lofi/chill) at top because mood matched perfectly. Jazz user got "Desert Blues" (blues/melancholic) at top because mood matched, not genre. This demonstrates that the mood feature enables cross-genre discovery—Jazz user found a non-jazz song that better matched their emotional preference. Without mood matching, this would not happen.

**What Surprised Us:**

The feature removal experiment proved that mood is load-bearing. Removing the +1.0 mood bonus caused Desert Blues to drop from 4.93 to 3.93 points, losing ranking to a genre-matched song with wrong mood. This showed that without mood, recommendations collapse into pure genre sorting—exactly the echo chamber we were trying to avoid.

**Simple Test Results:**

We ran two systematic experiments: (1) Weight investigation comparing original (Genre=2.0) vs refined (Genre=1.5) showed that lowering genre weight enabled better mood/energy matching without sacrificing satisfaction for well-represented users. (2) Feature removal (no mood) on Jazz profile showed 100% ranking change—proving mood is essential for system behavior.

---

## 8. Future Work  

(1) **Genre Expansion:** Add 3-5 songs per genre to eliminate single-song filter bubbles.  
(2) **Fuzzy Mood Matching:** Replace exact mood matching with semantic similarity (e.g., "peaceful" ≈ "relaxed").  
(3) **Collaborative Filtering:** Use user-user similarity to handle cold start and discover cross-genre tastes.  
(4) **Hybrid Scoring:** Combine audio features with collaborative signals for better diversity.

---

## 9. Personal Reflection  

Building this recommender revealed that data quality matters as much as algorithm design. Even with refined weights, a 13:1 genre imbalance creates hard walls that no weighting scheme can overcome. I learned that "fairness" in recommendations isn't about treating all users equally—it's about having enough representation for all user preferences in the data. The experiments showed that features (like mood) that seem minor can be essential for system behavior. The most surprising finding was how much the mood feature enables serendipity—without it, the system becomes a genre filter, not a recommender. This experience changed how I evaluate real-world recommenders like Spotify: I now notice dataset representation issues and think critically about which features drive recommendations.
