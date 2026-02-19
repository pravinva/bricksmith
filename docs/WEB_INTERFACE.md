# Bricksmith Architect Web Interface

Collaborative web interface for architecture diagram design powered by AI. Deploy as a Databricks App for team-wide access.

## Features

- 🎨 **Interactive Diagram Design**: Natural language to architecture diagrams
- 💬 **Real-time Chat Interface**: Iterative refinement through conversation
- 📊 **Session Management**: Track and resume diagram projects
- 🔄 **Live Previews**: See diagrams as they generate
- 👥 **Collaborative**: Share sessions with team members
- 🗄️ **Persistent Storage**: Lakebase PostgreSQL backend
- 🔐 **Databricks Auth**: Secure, workspace-integrated authentication

## Architecture

```
┌─────────────────────────────────────────────────┐
│  React Frontend (Vite + TypeScript)             │
│  - Chat Interface                               │
│  - Diagram Visualization                        │
│  - Session Management                           │
└────────────────┬────────────────────────────────┘
                 │ REST API
                 ▼
┌─────────────────────────────────────────────────┐
│  FastAPI Backend                                │
│  - /api/sessions    Session CRUD                │
│  - /api/chat        Chat endpoint               │
│  - /api/architect   AI generation               │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────┐
│  Lakebase    │  │  Gemini API  │
│  PostgreSQL  │  │  (via nano_  │
│  (Sessions)  │  │   banana)    │
└──────────────┘  └──────────────┘
```

## Deployment

### Prerequisites

- Databricks workspace with Apps enabled
- Lakebase instance (or SQLite for local dev)
- Gemini API key configured

### Deploy to Databricks Apps

1. **Install dependencies**:
   ```bash
   uv pip install -e ".[web]"
   ```

2. **Configure Lakebase** (optional, falls back to SQLite):
   ```bash
   # Create Lakebase database
   databricks lakebase create architect-db \
     --catalog main \
     --schema architect
   ```

3. **Deploy app**:
   ```bash
   databricks apps deploy
   ```

4. **Access the app**:
   ```bash
   databricks apps open bricksmith-architect
   ```

### Local Development

Run locally for testing:

```bash
# Start backend
cd /path/to/bricksmith
uv run python -m uvicorn bricksmith.web.main:app --reload

# In another terminal, start frontend
cd frontend
npm install
npm run dev
```

Access at: http://localhost:5173

## Configuration

### Environment Variables

**Backend (app.yaml)**:
- `DATABRICKS_LAKEBASE_URL`: PostgreSQL connection string
- `DATABRICKS_HOST`: Workspace URL (auto-injected)
- `DATABRICKS_TOKEN`: Auth token (auto-injected)
- `DSPY_MODEL`: Model for AI architect (default: databricks-claude-opus-4-5)

**Frontend (.env)**:
- `VITE_API_URL`: Backend API URL (default: /api)

### Database Configuration

**Lakebase (Production)**:
```yaml
resourceReferences:
  - name: architect-db
    type: postgresql
    database: architect_sessions
```

**SQLite (Development)**:
Automatically used when `DATABRICKS_LAKEBASE_URL` not set.
Database file: `~/.bricksmith/sessions.db`

## API Endpoints

### Sessions

**Create Session**:
```http
POST /api/sessions
Content-Type: application/json

{
  "name": "My Architecture",
  "description": "E-commerce platform design"
}

Response: 201 Created
{
  "id": "session-123",
  "name": "My Architecture",
  "created_at": "2026-02-04T10:00:00Z"
}
```

**List Sessions**:
```http
GET /api/sessions?limit=20&offset=0

Response: 200 OK
{
  "sessions": [
    {
      "id": "session-123",
      "name": "My Architecture",
      "updated_at": "2026-02-04T10:30:00Z"
    }
  ],
  "total": 1
}
```

**Get Session**:
```http
GET /api/sessions/{session_id}

Response: 200 OK
{
  "id": "session-123",
  "name": "My Architecture",
  "turns": [
    {
      "iteration": 1,
      "prompt": "Create a microservices architecture...",
      "image_url": "/api/sessions/session-123/images/1.png",
      "score": 4
    }
  ]
}
```

### Chat

**Send Message**:
```http
POST /api/chat
Content-Type: application/json

{
  "session_id": "session-123",
  "message": "Add authentication service",
  "score": null  // Optional: provide score for previous iteration
}

Response: 200 OK (streaming)
{
  "type": "status",
  "message": "Generating diagram..."
}
{
  "type": "image",
  "url": "/api/sessions/session-123/images/2.png"
}
{
  "type": "complete",
  "turn": {
    "iteration": 2,
    "prompt": "...",
    "image_url": "..."
  }
}
```

### Architect

**Generate Specification**:
```http
POST /api/architect/generate
Content-Type: application/json

{
  "description": "Design a data lakehouse architecture with Unity Catalog"
}

Response: 200 OK
{
  "spec": {
    "components": [...],
    "connections": [...]
  },
  "reasoning": "Created 5 components based on lakehouse pattern..."
}
```

## Frontend Components

### ArchitectureViz

Displays generated diagrams with zoom, pan, and full-screen support.

```tsx
import { ArchitectureViz } from './components/ArchitectureViz';

<ArchitectureViz 
  imageUrl="/api/sessions/123/images/1.png"
  iteration={1}
/>
```

### Chat

Interactive chat interface for diagram refinement.

```tsx
import { Chat } from './components/Chat';

<Chat 
  sessionId="session-123"
  onNewTurn={(turn) => console.log('New diagram:', turn)}
/>
```

### SessionList

Browse and manage diagram sessions.

```tsx
import { SessionList } from './components/SessionList';

<SessionList 
  onSelectSession={(id) => navigate(`/session/${id}`)}
/>
```

## Database Schema

### Sessions Table

```sql
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by TEXT,  -- Databricks username
  config JSONB      -- ConversationConfig
);
```

### Turns Table

```sql
CREATE TABLE turns (
  id TEXT PRIMARY KEY,
  session_id TEXT REFERENCES sessions(id),
  iteration INTEGER NOT NULL,
  prompt TEXT NOT NULL,
  image_path TEXT,
  score INTEGER,
  feedback TEXT,
  refinement_reasoning TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  metadata JSONB
);
```

## Customization

### Branding

Customize colors in `frontend/tailwind.config.js`:

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#FF3621',      // Databricks red
        secondary: '#00A972',    // Green
        accent: '#1B3139',       // Navy
      }
    }
  }
}
```

### Models

Change AI models in `app.yaml`:

```yaml
env:
  - name: DSPY_MODEL
    value: databricks-claude-sonnet-4  # Or other model
```

### Authentication

Adjust access control in `app.yaml`:

```yaml
ingress:
  authentication:
    type: databricks  # Options: databricks, none, custom
```

## Monitoring

### Health Check

```http
GET /api/health

Response: 200 OK
{
  "status": "healthy",
  "database": "connected",
  "model": "available"
}
```

### Logs

View application logs:

```bash
databricks apps logs bricksmith-architect --tail
```

### Metrics

Monitor via Databricks Apps dashboard:
- Request latency
- Error rates
- Database connections
- Active sessions

## Troubleshooting

### Backend Won't Start

**Symptom**: App deployment fails or crashes

**Solutions**:
1. Check Lakebase connection:
   ```bash
   databricks lakebase list
   ```

2. Verify resource allocation:
   ```yaml
   resources:
     cpu: "2"      # Increase if needed
     memory: 4Gi   # Increase if needed
   ```

3. Check logs:
   ```bash
   databricks apps logs bricksmith-architect --tail
   ```

### Frontend Not Loading

**Symptom**: Blank page or CORS errors

**Solutions**:
1. Check API URL in frontend:
   ```bash
   # Verify VITE_API_URL points to correct backend
   cat frontend/.env
   ```

2. Rebuild frontend:
   ```bash
   cd frontend
   npm run build
   ```

3. Check ingress configuration in `app.yaml`

### Slow Generation

**Symptom**: Diagrams take >60s to generate

**Solutions**:
1. Use faster model:
   ```yaml
   env:
     - name: DSPY_MODEL
       value: databricks-claude-sonnet-4  # Faster than opus
   ```

2. Increase timeout:
   ```python
   # In web/api/chat.py
   GENERATION_TIMEOUT = 120  # Increase from 60
   ```

3. Check Gemini API quota

### Database Connection Errors

**Symptom**: "Cannot connect to Lakebase" errors

**Solutions**:
1. Verify Lakebase instance is running:
   ```bash
   databricks lakebase get architect-db
   ```

2. Check resource reference in `app.yaml`:
   ```yaml
   resourceReferences:
     - name: architect-db
       type: postgresql
       database: architect_sessions  # Must match Lakebase DB name
   ```

3. Falls back to SQLite if Lakebase unavailable (dev mode only)

## Performance Optimization

### Caching

Enable session caching:

```python
# In web/services/session_store.py
CACHE_TTL = 300  # 5 minutes
```

### Connection Pooling

Configure PostgreSQL pool:

```python
# In web/db/lakebase.py
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### Frontend Optimization

Build production bundle:

```bash
cd frontend
npm run build
# Outputs to frontend/dist/
```

## Security

### Authentication

Databricks Apps automatically inject authentication. Users must be workspace members.

### Authorization

Implement per-session authorization:

```python
# In web/api/sessions.py
def check_access(session_id: str, user: str):
    session = get_session(session_id)
    if session.created_by != user:
        raise HTTPException(403, "Access denied")
```

### Secrets

Never commit secrets. Use Databricks Secrets:

```yaml
env:
  - name: GEMINI_API_KEY
    valueFrom:
      secretRef:
        name: gemini-api-key
        key: value
```

## Best Practices

1. **Session Naming**: Use descriptive names for easy discovery
2. **Regular Cleanup**: Archive old sessions to free database space
3. **Error Handling**: Always provide user feedback on errors
4. **Rate Limiting**: Implement per-user rate limits for API calls
5. **Logging**: Log all generation requests for debugging
6. **Backup**: Regular backup of Lakebase database
7. **Testing**: Test with different user personas and workflows

## Roadmap

Planned enhancements:

- **Collaborative editing**: Multiple users in same session
- **Version control**: Diagram versioning and branching
- **Export options**: SVG, PDF, PowerPoint export
- **Template library**: Pre-built architecture patterns
- **Comments**: Inline comments and annotations
- **Permissions**: Fine-grained access control
- **Analytics**: Usage metrics and popular patterns

## Support

- **Documentation**: See [docs/](../docs/)
- **Issues**: Report bugs via project issue tracker
- **Chat**: Use #bricksmith Slack channel
- **Email**: Contact maintainers for urgent issues

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup and contribution guidelines.
