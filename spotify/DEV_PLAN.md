# `DEV PLAN`
## Playlist Gardening
* 2024-08-09, Current State: **Satisfactory**
## New Music Discovery Automation
* `[Y]` **Search 01**, 2024-08-09, Current State: **Satisfactory**
### Search 02, Graded by Mini-Genre Proximity
* `[Y]` Cluster playlist songs into Micro-Genres, 2024-08-XX, Current State: **Satisfactory**
* `[Y]` Merge Micro-Genres into Mini-Genres, 2024-08-24: Tuned merge radius, Seems okay?
* `[Y]` Move Mini-Genre Outliers to Better Homes, 2024-08-24: If a mini-genre member is closer to a neighboring mini-genre than it is to its average sibling, then move to the neighboring mini-genre
* `[>]` Sub-Searches
    - `[Y]` New Releases, 2024-08-24: New Albums
    - `[Y]` Spotify Recommendations by Genre, 2024-08-24: New Tracks
    - `[Y]` Artist Top Tracks, 2024-08-25: New Tracks
    - `[Y]` Related Artists, 2024-08-25: New Tracks
    - `[>]` Featured Playlists
    - `[ ]` Sub-search 01
* `[ ]` Determine a total population to gather, Then sub-divide into above sub-searches
* `[ ]` Grade and Rank gathered results by Mini-Genre proximity
* `[ ]` Add top results to probationary playlist
* `[ ]` Test Search 02
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