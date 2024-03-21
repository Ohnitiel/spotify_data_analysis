import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("spotify_top_songs_audio_features.csv")
attributes = [
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "loudness",
    "tempo",
]

# What really is a catchy song?


# Check correlation between song attributes and stream
df[
    [
        "danceability",
        "energy",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "loudness",
        "tempo",
        "duration_ms",
        "streams",
    ]
].corr()

# PS: There is little to no correlation using any common method (Pearson,
# Spearman or Kendall)

# The analysis shows that no single attribute has a reasonable impact to
# determine the song as a top stream one

# So we head to another method of analysis

# What do most played artists have in common?
most_played_artist = (
    df.groupby("artist_names").streams.sum().sort_values(ascending=False).head(50)
)

df.query("artist_names.isin(@most_played_artist.index)").describe()


# Let's filter songs that have their attributes above the average of top played
# artists
top_played_filters = df.query("artist_names.isin(@most_played_artist.index)")[
    attributes
].mean()
query = ""
for el in top_played_filters.items():
    query += f"{el[0]} >= {el[1]} &"
query = query.strip(" &")

df.query(query)

# Seems like there are no songs that meet the criteria
# let's go for another type of analysis
# Lets check the attributes of most played songs
df.sort_values(by=["streams", "weeks_on_chart"], ascending=False).head(100).describe()

# Top 100 songs by streams and time on chart seems to be the best bet on
# catchy songs. Doing a quick analysis, it's clear they are not instrumental,
# acoustic, live or speechy songs


# Given we are looking for most danceable songs, let's analyze songs with danceability above average
danceability_filter = round(df.danceability.mean(), 2)
sort_by = ["streams", "weeks_on_chart", "danceability"]
danceable = (
    df.query("danceability => @danceability_filter").sort_values(by=sort_by).head(100)
)

# Top 100 songs in this category have quite a lot of similarities with the
# previous analysis, so much that it's very likely that a top 100 song is
# a danceable song

# Draw correlation chart between danceability and streams
correlation_chart = go.Figure(
    go.Scatter(
        x=df.danceability,
        y=df.streams,
    )
)

bar_chart = go.Figure(go.Bar(
    labels=df.track_name,
    values=df.streams
))
