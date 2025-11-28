# 🚀 WhatsApp Automation System — EggsInvest

A production-ready real estate automation platform that transforms WhatsApp into an intelligent agent for property distribution, buyer-deal matching, and CRM management. Built with FastAPI, Twilio, MySQL, and AI-powered message classification.

**Status:** Early Beta (Days 0-4 Complete) | **Grade:** B+ | **Production Ready:** Partial (Security hardening in progress)

---

## 🎯 What This Does

This system automates the entire real estate workflow:

- **🤖 Agent Onboarding**: Automatically welcome and manage agent profiles via WhatsApp
- **📨 Inbound Processing**: Receive and classify agent responses (interested/not interested/follow-up)
- **🔄 CRM Integration**: Update agent status automatically based on responses
- **🏠 Buyer Database**: Maintain buyer profiles with budgets, locations, and investment strategies
- **🎯 Deal Matching**: Intelligently match properties with qualified buyers
- **📢 Deal Broadcasting**: Auto-notify matching buyers of new properties
- **📊 Message Logging**: Complete conversation history for analytics

**Real-World Flow:**
```
Agent joins via WhatsApp
    ↓
System classifies their interest level
    ↓
CRM status updates automatically
    ↓
New property added (e.g., £450K Manchester house)
    ↓
System finds matching buyers (£400K-£500K budget, Manchester)
    ↓
Auto-sends property details to matching buyers
    ↓
Buyers reply with interest
    ↓
Complete audit trail in database
```

---

## ⚡ Key Features

### ✅ Completed (Days 0-4)

| Feature | Day | Status | Description |
|---------|-----|--------|-------------|
| **FastAPI Backend** | 0 | ✅ | Production framework with async support |
| **Outbound Messaging** | 1 | ✅ | Send templated WhatsApp messages to agents |
| **Message Logging** | 1 | ✅ | Persist all messages in MySQL |
| **Webhook Integration** | 2 | ✅ | Receive inbound messages via Twilio webhook |
| **Message Classification** | 3 | ✅ | AI-style intent detection (interested/not interested/follow-up) |
| **Agent CRM Update** | 3 | ✅ | Auto-update agent status based on replies |
| **Buyer Database** | 4 | ✅ | Import and manage buyer profiles |
| **Deal Matching** | 4 | ✅ | Intelligently match properties to qualified buyers |

### 🔜 In Progress (Days 5-7)

- [ ] **Day 5**: Deal broadcasting system with throttling
- [ ] **Day 6**: Interactive dashboard (React/Vue)
- [ ] **Day 7**: AI-powered lead scoring and buyer recommendations

### 🏗️ Infrastructure (Parallel)

- [ ] Webhook signature validation
- [ ] Rate limiting & message queue
- [ ] Input validation (Pydantic models)
- [ ] Comprehensive error handling
- [ ] Test suite (pytest)
- [ ] Production deployment (AWS/Railway)

---

## 📦 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend Framework** | FastAPI | Latest |
| **Web Server** | Uvicorn | Latest |
| **WhatsApp API** | Twilio | Cloud API |
| **Database** | MySQL | 8.0+ |
| **Environment** | Python | 3.8+ |
| **Public URL** | Ngrok | For development |
| **Deployment** | AWS/Railway/Render | TBD |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MySQL database (local or cloud)
- Twilio account with WhatsApp sandbox enabled
- Ngrok (for local testing)

### 1. Clone & Setup

```bash
# Clone repository
git clone https://github.com/Anshul-ui-beast/WhatsApp-Automation.git
cd WhatsApp-Automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-dotenv mysql-connector-python twilio python-multipart
```

### 2. Configure Environment

Create `.env` file in project root:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=eggs_invest

# Application
LOG_LEVEL=INFO
```

**Get Twilio Credentials:**
1. Go to [Twilio Console](https://console.twilio.com)
2. Find Account SID and Auth Token
3. Set up WhatsApp sandbox at https://www.twilio.com/console/sms/whatsapp

### 3. Setup Database

```bash
# Create MySQL database
mysql -u root -p < database/schema.sql
```

**Database Schema:**
```sql
CREATE TABLE agents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20) UNIQUE,
    name VARCHAR(100),
    status ENUM('active', 'interested', 'not_interested', 'follow_up'),
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE buyers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    phone VARCHAR(20),
    budget DECIMAL(12, 2),
    location VARCHAR(100),
    strategy VARCHAR(50),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20),
    message_type ENUM('inbound', 'outbound'),
    body TEXT,
    message_sid VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Import Data

```bash
# Import agents from CSV
python import_agents.py

# Import buyers from CSV
python import_buyers.py
```

**CSV Format:**

`data/agents.csv`:
```csv
phone,name
whatsapp:+441234567890,John Smith
whatsapp:+441234567891,Jane Doe
```

`data/buyers.csv`:
```csv
name,phone,budget,location,strategy
Alice Johnson,whatsapp:+441234567892,500000,Manchester,Buy-to-let
Bob Wilson,whatsapp:+441234567893,750000,London,House flip
```

### 5. Start Development Server

```bash
# Terminal 1: FastAPI
uvicorn backend.app:app --reload

# Terminal 2: Ngrok (in separate terminal)
ngrok http 8000
```

You'll see:
```
Forwarding   http://abc123.ngrok.io -> http://localhost:8000
```

### 6. Configure Twilio Webhook

1. Go to [Twilio Console](https://console.twilio.com/sms/whatsapp)
2. Under **Sandbox Settings**, set webhook URL:
   ```
   https://YOUR_NGROK_URL/whatsapp-webhook
   ```
3. Save

### 7. Test It!

Send a WhatsApp message to your Twilio sandbox number. You should see:
- Message logged in MySQL
- Auto-response sent back
- Agent status updated

---

## 📂 Project Structure

```
WhatsApp-Automation/
├── backend/
│   ├── __init__.py
│   ├── app.py                    # Main FastAPI application
│   ├── whatsapp_client.py        # Twilio integration
│   ├── db_client.py              # Database operations (agents, buyers, messages)
│   ├── classifier.py             # Message intent classification
│   └── config.py                 # Configuration management
├── database/
│   └── schema.sql                # MySQL database schema
├── data/
│   ├── agents.csv                # Agent list for import
│   └── buyers.csv                # Buyer list for import
├── import_agents.py              # Import agents from CSV
├── import_buyers.py              # Import buyers from CSV
├── tests/
│   ├── test_classifier.py        # Classifier unit tests
│   ├── test_endpoints.py         # API endpoint tests
│   └── test_db.py                # Database operation tests
├── .env                          # Environment variables (not in git)
├── .env.example                  # Template for .env
├── .gitignore
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🔌 API Endpoints

### Health Check
```
GET /
```
**Response:** `{"status": "ok"}`

### Send Message
```
POST /send-message
Content-Type: application/json

{
    "phone": "whatsapp:+441234567890",
    "message": "Hello, interested in properties?"
}
```

### Incoming Webhook (Auto-Called by Twilio)
```
POST /whatsapp-webhook
From: +441234567890
Body: "Yes, I'm interested!"
MessageSid: SM1234567890
```

**Process:**
1. Extract message from form data
2. Classify intent (interested/not_interested/follow_up)
3. Update agent status in MySQL
4. Send appropriate follow-up message

### Match Buyers to Property
```
POST /match-buyers
Content-Type: application/json

{
    "price": 500000,
    "location": "Manchester",
    "strategy": "Buy-to-let"
}
```

**Response:**
```json
{
    "matched_buyers": [
        {
            "id": 1,
            "name": "Alice Johnson",
            "phone": "whatsapp:+441234567892",
            "budget": 500000,
            "location": "Manchester"
        }
    ],
    "count": 1
}
```

### Get Agent Stats
```
GET /agents/stats
```

**Response:**
```json
{
    "total_agents": 50,
    "active": 35,
    "interested": 10,
    "not_interested": 5
}
```

---

## 🧠 Message Classification

The classifier detects buyer intent with three categories:

| Intent | Keywords | Example |
|--------|----------|---------|
| **Interested** | Yes, Sure, Interested, Tell me more | "Yes, tell me more about this property" |
| **Not Interested** | No, Not now, Stop, Not interested | "No thanks, not right now" |
| **Follow Up** | Maybe, Later, More info, Remind me | "Maybe later, send me more details" |

**How it works:**

```python
# backend/classifier.py
def classify_message(text: str) -> str:
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['yes', 'sure', 'interested', 'tell me more']):
        return 'interested'
    elif any(word in text_lower for word in ['no', 'not now', 'stop', 'not interested']):
        return 'not_interested'
    else:
        return 'follow_up'
```

**Future Enhancement:** Replace with NLP model (OpenAI, Hugging Face)

---

## 🗄️ Database Schema

### agents table
```
id (PK)
phone (UNIQUE)
name
status (interested | not_interested | follow_up | active)
joined_date
```

### buyers table
```
id (PK)
name
phone
budget (decimal)
location
strategy (buy-to-let | house-flip | etc)
created_date
```

### messages table
```
id (PK)
phone
message_type (inbound | outbound)
body (text)
message_sid (Twilio reference)
timestamp
```

### deals table (Coming in Day 5)
```
id (PK)
property_address
price
location
roi (estimated)
yield (estimated)
created_date
```

---

## 🔐 Security Checklist

### ⚠️ Current Status (TODO Before Production)

- [ ] **Webhook Signature Validation**: Verify Twilio signature on incoming webhooks
- [ ] **Rate Limiting**: Prevent abuse and WhatsApp blocks
- [ ] **Input Validation**: Use Pydantic models for all endpoints
- [ ] **Error Handling**: Graceful failures with logging
- [ ] **API Authentication**: JWT or API key for protected endpoints
- [ ] **Database Security**: Connection pooling, parameterized queries
- [ ] **Secrets Management**: No hardcoded credentials
- [ ] **HTTPS Only**: Enforce HTTPS in production
- [ ] **Logging & Monitoring**: Sentry, CloudWatch integration

### Quick Security Win (Add This Now)

```python
# backend/app.py
from twilio.request_validator import RequestValidator

VALIDATOR = RequestValidator(os.getenv("TWILIO_AUTH_TOKEN"))

@app.post("/whatsapp-webhook")
async def webhook(request: Request):
    # Validate request came from Twilio
    url = str(request.url)
    params = await request.form()
    signature = request.headers.get("X-Twilio-Signature", "")
    
    if not VALIDATOR.validate(url, params, signature):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Process message...
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test
pytest tests/test_classifier.py -v
```

### Test Classifier

```python
# tests/test_classifier.py
from backend.classifier import classify_message

def test_interested():
    assert classify_message("Yes") == "interested"
    assert classify_message("SURE!") == "interested"
    assert classify_message("I'm interested") == "interested"

def test_not_interested():
    assert classify_message("No") == "not_interested"
    assert classify_message("Not now") == "not_interested"

def test_follow_up():
    assert classify_message("Maybe") == "follow_up"
    assert classify_message("Send me more info") == "follow_up"
```

---

## 📊 Performance & Scalability

### Current Limits

- ✅ Handles ~100 agents
- ✅ Supports 50 buyers
- ⚠️ Twilio sandbox: 50 WhatsApp messages/day
- ⚠️ No rate limiting (risky)
- ⚠️ Synchronous processing (slow for bulk sends)

### Scaling to Production

**Coming in Day 5:**
- Message queue (Celery, RabbitMQ)
- Async bulk processing
- Rate limiting (5 messages/second)
- Database connection pooling
- Caching layer (Redis)

---

## 🚀 Deployment

### Option 1: AWS EC2

```bash
# SSH into instance
ssh -i key.pem ubuntu@instance-ip

# Setup
git clone https://github.com/Anshul-ui-beast/WhatsApp-Automation.git
cd WhatsApp-Automation
pip install -r requirements.txt

# Start with systemd
sudo systemctl start whatsapp-automation
```

### Option 2: Railway

```bash
# Install Railway CLI
npm i -g railway

# Login and deploy
railway login
railway init
railway up
```

### Option 3: Render

1. Push to GitHub
2. Connect Render to repo
3. Set environment variables
4. Deploy (auto)

**Update Twilio Webhook** to production URL:
```
https://your-production-domain.com/whatsapp-webhook
```

---

## 📈 Roadmap

### Week 1 (Days 0-4) ✅ COMPLETE
- [x] FastAPI backend setup
- [x] Twilio WhatsApp integration
- [x] Inbound/outbound messaging
- [x] Message classification
- [x] Buyer database & matching

### Week 2 (Days 5-7) 🚧 IN PROGRESS
- [ ] **Day 5**: Deal broadcasting system
- [ ] **Day 6**: Interactive dashboard
- [ ] **Day 7**: AI lead scoring

### Week 3+ (Production Ready)
- [ ] Security hardening (JWT, validation)
- [ ] Error handling & retry logic
- [ ] Message queue & throttling
- [ ] Monitoring & alerting
- [ ] Performance optimization

### Phase 2 (Advanced Features)
- [ ] Property scraper integration (Rightmove, Zoopla)
- [ ] Auto-calculate ROI & yield
- [ ] Buyer preference learning
- [ ] Multi-language support
- [ ] Call scheduling integration
- [ ] Payment gateway

---

## 🐛 Troubleshooting

### Issue: "No module named 'twilio'"
```bash
pip install twilio
```

### Issue: Webhook not receiving messages
1. Check Ngrok URL is active: `ngrok http 8000`
2. Update Twilio webhook URL in console
3. Send test message from Twilio sandbox
4. Check logs: `tail -f server.log`

### Issue: Database connection failed
```bash
# Check MySQL is running
mysql -u root -p -e "SELECT 1"

# Verify credentials in .env
# Check DB exists: SHOW DATABASES;
```

### Issue: WhatsApp messages not sending
- Check Twilio account has credit
- Verify phone number format: `whatsapp:+441234567890`
- Check sandbox is active
- Review Twilio logs for errors

### Issue: Getting "Max retries exceeded"
- Likely rate limiting from WhatsApp
- Add delays between sends
- Use message queue (coming Day 5)

---

## 📚 Documentation

### API Documentation (Auto-Generated)

Once running, visit:
```
http://localhost:8000/docs        # Swagger UI
http://localhost:8000/redoc       # ReDoc
```

### Code Documentation

Each module has docstrings:
```python
# backend/whatsapp_client.py
def send_whatsapp_message(phone: str, message: str) -> dict:
    """
    Send a WhatsApp message via Twilio.
    
    Args:
        phone: Recipient phone in format whatsapp:+1234567890
        message: Message text to send
        
    Returns:
        dict with message_sid and status
        
    Raises:
        TwilioException: If API call fails
    """
```

---

## 🤝 Contributing

We welcome contributions! 

1. Fork the repo
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes
4. Add tests
5. Submit PR

**Development Checklist:**
- [ ] Code follows PEP 8
- [ ] Tests pass: `pytest`
- [ ] No hardcoded secrets
- [ ] Docstrings added
- [ ] PR description clear

---

## 📞 Support & Issues

- **Issues**: Open a GitHub issue with detailed description
- **Questions**: Check existing issues first
- **Bugs**: Include reproduction steps and error logs

---

## 📄 License

MIT License - see LICENSE file for details

---

## 👨‍💻 Author

**Anshul** - Real estate automation enthusiast  
- GitHub: [@Anshul-ui-beast](https://github.com/Anshul-ui-beast)
- Projects: Instant Scraper Tool, WhatsApp Automation

---

## ⭐ Show Your Support

If this project helped you, please give it a star! ⭐

---

## 🎓 Learning Resources

- [Twilio WhatsApp API Docs](https://www.twilio.com/docs/whatsapp/api)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [MySQL Guide](https://dev.mysql.com/doc/)
- [Ngrok Documentation](https://ngrok.com/docs)
- [AsyncIO Guide](https://docs.python.org/3/library/asyncio.html)

---

**Built with ❤️ for real estate automation**

*Last Updated: November 2025 | Status: Beta | Production ETA: 1 week*