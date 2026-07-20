# VibeFinder 1.0 - Model Card

## 1. Model Name

**VibeFinder 1.0** — A point-weighted music recommender that finds personalized song suggestions based on user genre, mood, and audio preferences.

---

## 2. Goal / Task

VibeFinder recommends the top 5 songs a user will likely enjoy based on their favorite genre, mood, and target audio characteristics (energy, valence, tempo, acousticness). It tries to balance what users explicitly prefer (genre/mood) with how songs actually sound (continuous audio features).

---

## 3. Data Used

**Dataset:** 18 songs across 15 genres with 10 different moods. Each song has: title, artist, genre, mood, energy (0-1), tempo (bpm), valence (0-1), danceability (0-1), acousticness (0-1).

**Key limitations:** 13 out of 15 genres have only 1 song each. "Intense" mood is 22% of data while "peaceful" is 5.6%. Dataset is Western music-focused with no world music or non-English vocals. Only 27.8% of songs fall in mid-energy range (0.4-0.6).

---

## 4. Algorithm Summary

VibeFinder scores each song by comparing it to the user's preferences:
- **Genre match** gets +1.5 points if it matches favorite genre
- **Mood match** gets +1.0 points if it matches favorite mood  
- **Audio attributes** (energy, acousticness, tempo, valence) each get partial credit based on how close they are to target values—each can earn up to 0.8-1.5 points depending on attribute

All scores are added together. Songs with highest total scores rank first, and the top 5 are returned with explanations of why they scored well.

---

## 5. Observed Behavior / Biases

**Critical filter bubble:** Users who prefer rock, jazz, metal, or classical music get locked into a single song because each genre has only 1 song in the catalog. No matter what their other preferences are, they'll keep getting that same song in top recommendations.

**Mood imbalance:** The system uses exact mood matching (chill must match chill exactly). A user wanting "peaceful" music cannot get a "relaxed" song as alternative, even though they're emotionally similar. Users seeking underrepresented moods like "peaceful" (5.6% of data) have far fewer good matches than users wanting "intense" (22%).

**Energy clustering:** Users wanting mid-range energy (0.4-0.6) are disadvantaged because only 27.8% of songs fall in this range. Extreme energy preferences (very high or very low) have better catalog coverage.

---

## 6. Evaluation Process

We tested 4 different user profiles:
- **Chill Lofi:** Well-represented, got diverse lofi recommendations ranking low-energy songs correctly
- **High-Energy Pop:** Well-represented, got diverse pop recommendations with high-energy songs
- **Deep Intense Rock:** Only 1 rock song exists, got stuck recommending the same song multiple times
- **Melancholic Jazz:** Only 1 jazz song exists, but mood matching allowed cross-genre discovery (blues song ranked higher than jazz song because mood matched better)

We ran two experiments: (1) tested whether lowering genre weight from 2.0 to 1.5 would reduce echo chambers (it did), and (2) tested what happens if we remove mood matching entirely (recommendations collapsed back to pure genre sorting). The mood experiment revealed that mood is load-bearing—it's the feature that enables cross-genre discovery.

---

## 7. Intended Use and Non-Intended Use

**Intended use:** Classroom exploration of recommender system tradeoffs and bias. Testing recommendations for users who have clear genre and mood preferences. Understanding how data imbalance affects recommendations.

**NOT intended for:** Production music streaming (too small dataset). Users without clear genre preference. Real-world deployment without significant data expansion. Users who want diverse cross-genre exploration (the system prioritizes genre too heavily). Users seeking recommendations based on artist history or social graphs.

---

## 8. Ideas for Improvement

1. **Expand dataset:** Add 3-5 more songs per genre to eliminate single-song filter bubbles. Every genre should have at least 3 options.

2. **Fuzzy mood matching:** Replace exact mood matching with semantic similarity (e.g., treat "peaceful" and "relaxed" as similar). Add computational cost but enables better substitutes.

3. **Add collaborative filtering:** Track what songs users actually like and recommend based on user-user similarity. Solves cold-start problem and discovers cross-genre patterns real users enjoy together.
