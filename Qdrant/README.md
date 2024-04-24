## Curious-Bees

## Qdrant Client and Transformers Integration

## Overview
This repository contains code snippets demonstrating the integration of Qdrant Client for similarity search and Transformers for text embedding in Python. The integration allows for efficient similarity search over a collection of documents based on their embeddings generated using Transformers.

## Setup

### Installation
Make sure you have the required packages installed:
```bash
!pip install qdrant-client
!pip install -U transformers
!pip install torch
```

### Environment Variables
Set up the necessary environment variables:
- `QDRANT_HOST`: The host link for Qdrant.
- `QDRANT_API_KEY`: Your Qdrant API key.
- `QDRANT_COLLECTION`: The name of the collection in Qdrant.

### Free Custom Tier Setup
To create a free custom tier in Qdrant, follow these steps:
1. Sign up or log in to [Qdrant](https://qdrant.io/).
2. Go to the "Billing" section in the dashboard.
3. Select the "Custom" tier and proceed with the free plan.
4. Once your custom tier is created, note down your API key and configure the environment variables accordingly.

- jupyter notebook is attached for references
