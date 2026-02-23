# Aignosis Coding Assignment

This project consists of a FastAPI backend and a React (Vite) frontend. The main functionality revolves around secure video streaming, where the backend decrypts AES-encrypted video files using an RSA private key and streams the result to the client.

## Project Structure

- `backend/`: Python FastAPI application handling secure video decryption and streaming using `cryptography`.
- `frontend/`: React application (powered by Vite) for the user interface.

## Prerequisites

- [Node.js](https://nodejs.org/) (for the frontend)
- [Python 3.x](https://www.python.org/) (for the backend)

## Getting Started

### 1. Backend Setup

Navigate to the backend directory, install dependencies, and start the development server:

```sh
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend server will typically run on `http://localhost:8000` (or the port specified by FastAPI).

### 2. Frontend Setup

Navigate to the frontend directory, install the required packages, and start the development server:

```sh
cd frontend
npm install
npm run dev
```

The frontend will start on `http://localhost:5173`. Open this URL in your browser to view the application.

## Core Mechanisms
- **Cryptography**: The backend stores AES-encrypted videos and RSA-encrypted AES keys. It securely decrypts the AES key using an RSA private key, then streams the decrypted video on the fly.

## API Endpoints

### `GET /video/stream`
Streams the decrypted video to the client in chunks.
- **Query Parameters**: 
  - `uid` (string): User ID
  - `tid` (string): Transaction ID
- **Response**: `video/mp4` stream

## Testing with UID and TID

The streaming endpoint expects a User ID (`uid`) and a Transaction ID (`tid`). For demonstration and testing purposes, the application includes a built-in example mechanism:

- **Frontend**: The `VideoPlayer` component includes a **Try Example!!!** button. When clicked, it automatically populates the `uid` input with `123` and the `tid` input with `456`.
- **Backend**: Inside the `/video/stream` route in `main.py`, the `uid` and `tid` variables are explicitly hardcoded to `123` and `456` respectively, effectively overriding any arbitrary query parameters sent from the client. 

**Why was this done?**
Since there is currently **only one sample video** stored on the backend, this hardcoding ensures that the specific sample encrypted files (`123_456_encrypted.bin` and `123_456_encrypted_key.bin`) located in the `storage/` directory are always accessed correctly regardless of user input. This perfectly demonstrates the complete AES/RSA decryption logic without requiring custom uploads.
