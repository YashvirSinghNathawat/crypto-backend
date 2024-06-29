# FastAPI Crypto App

This project demonstrates a FastAPI application that fetches cryptocurrency prices using the CoinGecko API, deployed with Docker.

## Features

- Fetches cryptocurrency prices using CoinGecko API.
- Dockerized for easy deployment and scalability.

## Prerequisites

Before running the application, ensure you have the following installed:

- Docker Desktop: [Download Docker](https://www.docker.com/products/docker-desktop)
- Python 3.x: [Download Python](https://www.python.org/downloads/)

## Setup

1. **Clone the repository:**

   ```bash
   git clone git@github.com:YashvirSinghNathawat/crypto-backend.git
   cd crypto-backend

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

3. **Setup Environment Variables**
    Create a .env file in the root directory and define environment variables 
    ```plaintext
    COINGECKO_API_KEY=your_coingecko_api_key

4. **Run with Docker**
    ```bash
    docker-compose up --build

5. **Access the application**
    ```bash
    http://localhost:8000