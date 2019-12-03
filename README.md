# Introduction

In this world where corporations own all of your data there is a movement for
people to gain control over their data and selectively give access to it. In a similar
vein, this project creates a Music Pod -- a repository for your own music collection
that is tagged with MusicBrainz IDs.

The Music Pod scans your collection, extracts the metdata, creates a search index
and then makes the music available via a private API so that you can access your music
collection in whatever tools or web pages you'd like to use them in.

Music Pods could also be created for artists to make their music available to the
public and to services like AcousticBrainz that aim to analyze music files.

# Current features

While the current setup isn't very polished and not easy to set up, one of the next
steps is to wrap the whole pod into a docker setup, complete with HTTPs support 
and some form of authentication.

So far, this project can scan your music collection, make a SQLite database,
find duplicates in your music collection and create a search index. API endpoints
expose the metadata, the audio files and a rudimentary search mechanism to search 
the collection.

# API definition

## Search

`http://localhost:5000/api/search?q=boards`

This returns an array of search hits that looks roughly like:

```
{

    "artist": "Boards of Canada",
    "artist_mbid": "69158f97-4c07-4c4e-baf8-4e4ab1ed666e",
    "duration": 365450,
    "mbid": "4766bc28-ef32-3d35-ab7a-429acbf072bb",
    "name": "Aquarius",
    "release": "Aquarius",
    "release_mbid": "69158f97-4c07-4c4e-baf8-4e4ab1ed666e",
    "tnum": 1

}
```

## Metadata lookup:

`http://localhost:5000/api/recording/e9a1a724-d632-38b9-bf6c-42ec278d6766/metadata`

returns the metadata for a track or 404:

```
{

    "artist_mbid": "69158f97-4c07-4c4e-baf8-4e4ab1ed666e",
    "artist_name": "Boards of Canada",
    "duration": 75266,
    "mbid": "e9a1a724-d632-38b9-bf6c-42ec278d6766",
    "name": "Dandelion",
    "release_mbid": "69158f97-4c07-4c4e-baf8-4e4ab1ed666e",
    "release_name": "Geogaddi",
    "tnum": 5

}
```

## Fetching audio:

`localhost:5000/api/recording/e9a1a724-d632-38b9-bf6c-42ec278d6766`

returns the audio file or 404.
