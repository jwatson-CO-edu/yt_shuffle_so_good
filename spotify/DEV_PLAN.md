# `DEV PLAN`
## Playlist Gardening
* 2024-08-09, Current State: **Satisfactory**
## New Music Discovery Automation
* `[Y]` **Search 01**, 2024-08-09, Current State: **Satisfactory**
### Search 02, Graded by Mini-Genre Proximity
* `[Y]` Cluster playlist songs into Micro-Genres, 2024-08-XX, Current State: **Satisfactory**
* `[Y]` Merge Micro-Genres into Mini-Genres, 2024-08-24: Tuned merge radius, Seems okay?
* `[Y]` Move Mini-Genre Outliers to Better Homes, 2024-08-24: If a mini-genre member is closer to a neighboring mini-genre than it is to its average sibling, then move to the neighboring mini-genre
* `[Y]` Sub-Searches, 2024-08-29: Individual searches have been tested
    - `[Y]` New Releases, 2024-08-24: New Albums
    - `[Y]` Spotify Recommendations by Genre, 2024-08-24: New Tracks
    - `[Y]` Artist Top Tracks, 2024-08-25: New Tracks
    - `[Y]` Related Artists, 2024-08-25: New Tracks
    - `[Y]` Featured Playlists, 2024-08-28: New Tracks
    - `[Y]` Sub-search 01, 2024-08-28: See Above
* `[>]` Combined Search
    - `[>]` Function
        * `[Y]` Perform sub-searches (request excess tracks), 2024-08-29: Multi-search needs testing
        * `[Y]` Populate extended metadata for all returned tracks, 2024-08-29: Multi-search needs testing
        * `[>]` Filter
            - `[>]` Not shorter than 1:45
            - `[>]` Not vocal (explicit)
            - `[ ]` Not in Collection
            - `[ ]` Not in Reviewed
        * `[ ]` Grade and Rank gathered results by Mini-Genre proximity
    - `[ ]` Add top results to probationary playlist
    - `[ ]` Update review IDs
    - `[ ]` Test Search 02
### `??` Search 03, ANN `??`
### Sources
#### Easy Difficulty
* Spotipy API
    - https://spotipy.readthedocs.io/en/2.24.0/#spotipy.client.Spotify.search
        * https://developer.spotify.com/documentation/web-api/reference/search
    - https://spotipy.readthedocs.io/en/2.24.0/index.html#spotipy.client.Spotify.recommendations
    - https://spotipy.readthedocs.io/en/2.24.0/index.html#spotipy.client.Spotify.recommendation_genre_seeds
* https://medium.com/@obielinda/building-a-spotify-recommendation-system-d4b67018eac2
* https://medium.com/@shruti.somankar/building-a-music-recommendation-system-using-spotify-api-and-python-f7418a21fa41

#### Medium Difficulty
* https://medium.com/geekculture/how-to-find-new-songs-on-spotify-using-machine-learning-d99bd8855a18
* https://github.com/Purefekt/Recommender-System-using-Personal-Spotify-Data
* https://jiading-zhu.medium.com/1-intro-1b6e3a4b2fb3

#### Hard Difficulty
* https://medium.com/@benalex/implement-your-own-music-recommender-with-graph-neural-networks-lightgcn-f59e3bf5f8f5
* https://arxiv.org/pdf/2312.10079
* https://arxiv.org/pdf/2310.06282v4
* https://hackernoon.com/ai-prompts-are-the-incantations-that-make-chatgpt-do-magical-things