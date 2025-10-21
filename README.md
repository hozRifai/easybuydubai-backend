# EasyBuy Dubai Backend API

A FastAPI-based backend service for the EasyBuy Dubai property assistant chatbot.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key

### Installation

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure Environment Variables**

Edit the `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
```

⚠️ **IMPORTANT**: You must replace `your_openai_api_key_here` with your actual OpenAI API key for the chat to work.

Get your API key from: https://platform.openai.com/api-keys

3. **Run the Server**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📋 API Endpoints

### Health Check
```bash
GET http://localhost:8000/api/health
```

### Chat Endpoints

**Send Message**
```bash
POST http://localhost:8000/api/chat/message
Content-Type: application/json

{
  "message": "I'm looking for a 2-bedroom apartment in Dubai Marina",
  "session_id": null  // Optional, will create new session if not provided
}
```

**Create Session**
```bash
POST http://localhost:8000/api/chat/session/create
```

**Get Session**
```bash
GET http://localhost:8000/api/chat/session/{session_id}
```

**Clear Session**
```bash
DELETE http://localhost:8000/api/chat/session/{session_id}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | gpt-3.5-turbo |
| `PORT` | Server port | 8000 |
| `ENVIRONMENT` | Environment mode | development |
| `FRONTEND_URL` | Frontend URL for CORS | http://localhost:3000 |

### Available Models

- `gpt-3.5-turbo` - Fast and cost-effective (default)
- `gpt-4` - More capable but slower and more expensive

Note: o1-mini is not yet available via the OpenAI API

## 🐳 Docker Deployment

### Build the Image
```bash
docker build -t easybuydubai-backend .
```

### Run the Container
```bash
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  -e ENVIRONMENT=production \
  --name easybuydubai-backend \
  easybuydubai-backend
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── models.py         # Pydantic models
│   ├── routers/          # API endpoints
│   │   ├── chat.py       # Chat endpoints
│   │   └── health.py     # Health check
│   └── services/         # Business logic
│       ├── openai_service.py  # OpenAI integration
│       └── chat_service.py    # Chat management
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
└── run.py              # Development server runner
```

## 🧪 Testing

Test the API with curl:

```bash
# Health check
curl http://localhost:8000/api/health

# Send a chat message
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I need help finding a property"}'
```

## 📝 API Documentation

When running in development mode, interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔒 Security Notes

- Never commit your `.env` file with real API keys
- Use environment-specific configurations
- Enable CORS only for trusted origins in production
- Implement rate limiting for production use

## 🛠️ Development

### Running with Auto-reload
```bash
python run.py
```

### Code Structure
- Services handle business logic
- Routers define API endpoints
- Models define data structures
- Config manages settings

## 📦 Production Deployment

For production deployment:

1. Set `ENVIRONMENT=production` in `.env`
2. Use a proper ASGI server (uvicorn with workers)
3. Set up SSL/TLS termination
4. Configure proper logging
5. Set up monitoring and alerts

### Production Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🆘 Troubleshooting

### "No module named 'app'"
Make sure you're running from the backend directory.

### "OpenAI API key not found"
Check your `.env` file and ensure `OPENAI_API_KEY` is set correctly.

### CORS Issues
Ensure your frontend URL is added to the CORS configuration in `app/main.py`.

### Port Already in Use
Change the port in `.env` or use a different port when running:
```bash
python -m uvicorn app.main:app --port 8001
```