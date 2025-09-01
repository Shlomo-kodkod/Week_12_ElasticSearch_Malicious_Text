# Elastic malicious text system

## A system to detect and analyze antisemitic content.

### This project use FastAPI for the REST API, Elasticsearch for data storage and search, and custom text processing to identify antisemitic content and weapon mentions.

## Features

- Loads tweet data from CSV files into Elasticsearch
- Processes text data to calculate sentiment analysis
- Detects weapon mentions using a blacklist
- Filters and manages antisemitic content based on weapons count
- Provides REST API endpoints using FastAPI
- Clean data based on sentiment and content 

## Project Structure

```
├── app/
│ ├── api.py          # API endpoints
│ ├── elastic.py      # Elasticsearch operations
│ ├── loader.py       # CSV and text file loader 
│ ├── processor.py    # text processing 
│ ├── manager.py      # data loading, processing, and management
│ └── config.py       # configuration
├── data/
│ ├── weapon_list.txt       # blacklist 
│ └── tweets_injected 3.csv # tweet data
│
├── scripts/            # OS scripts 
│
├── Dockerfile
├── requirements.txt
└── README.md
```

## API Endpoints

### GET `/antisemitic-1-weapons`
Returns antisemitic content with at least 1 weapon mention.

### GET `/antisemitic-2-weapons`
Returns antisemitic content with at least 2 weapon mentions.

