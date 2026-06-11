# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Clone & Install
```bash
git clone https://github.com/Arnav-On-Top/Personal-Knowledge-Navigator-
cd Personal-Knowledge-Navigator-
pip install -r requirements.txt
```

### Step 2: Run the Server
```bash
python main.py
```

You should see:
```
✅ Navigator initialized successfully
✅ Application ready to serve requests
Starting Personal Knowledge Navigator API on 0.0.0.0:8000
```

### Step 3: Open in Browser
```
http://localhost:8000/docs
```

---

## 📝 Try Your First Query

### Using Swagger UI (Browser)
1. Go to http://localhost:8000/docs
2. Click on "POST /query"
3. Click "Try it out"
4. Replace the example with:
```json
{
  "question": "What are the latest architecture decisions?",
  "user": {
    "user_id": "user@example.com",
    "roles": ["analyst"],
    "organization": "engineering"
  },
  "top_k": 5
}
```
5. Click "Execute"

### Using cURL
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the latest architecture decisions?",
    "user": {
      "user_id": "user@example.com",
      "roles": ["analyst"],
      "organization": "engineering"
    },
    "top_k": 5
  }'
```

### Expected Response
```json
{
  "answer": "Based on the retrieved documents...",
  "citations": [
    {
      "source_id": "mock_source",
      "source_name": "Mock Knowledge Base",
      "document_id": "doc_001",
      "document_title": "System Architecture Principles",
      "confidence_score": 0.92
    }
  ],
  "confidence_score": 0.88,
  "hallucination_risk": "low",
  "sources_used": ["mock_source"]
}
```

---

## 🧪 Run Examples

### Basic Query
```bash
python -m examples.basic_query
```

### Agent Chat (Multi-turn)
```bash
python -m examples.agent_integration
```

### Permission Demo
```bash
python -m examples.multi_source_retrieval
```

---

## ✅ Verify Everything Works

### 1. Check Health
```bash
curl http://localhost:8000/health
```

✅ Expected: `{"status": "healthy", "sources_connected": 1, "version": "1.0.0"}`

### 2. View Sources
```bash
curl http://localhost:8000/sources
```

✅ Expected: List of connected data sources

### 3. Check Permissions
```bash
curl "http://localhost:8000/permissions/check?user_id=user@example.com&role=analyst&resource=document"
```

✅ Expected: `{"has_access": true}`

---

## 🔧 Optional: Connect Your Own Database

1. Create `.env` file:
```env
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
```

2. Restart the server:
```bash
python main.py
```

---

## 📚 Next Steps

- Read [DEVELOPMENT.md](DEVELOPMENT.md) for detailed guide
- Check [README.md](README.md) for full documentation
- Explore [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details

---

## ❌ Troubleshooting

### Port 8000 already in use?
```bash
# Use a different port
API_PORT=8001 python main.py
```

### Module not found errors?
```bash
# Ensure you're in the right directory
cd Personal-Knowledge-Navigator-

# Reinstall dependencies
pip install -r requirements.txt
```

### Tests failing?
```bash
# Make sure pytest is installed
pip install pytest pytest-asyncio

# Run tests
pytest
```

---

## 🎉 You're All Set!

The application is ready to use with mock data. You can:
- Query the knowledge base
- Check permissions
- Run multi-turn conversations
- Connect to real databases (see DEVELOPMENT.md)

**Happy exploring! 🚀**
