# Bricksmith Architect - Frontend

Repository acknowledgement: includes material and inputs from David O'Keefe.

React + TypeScript frontend for collaborative architecture diagram design.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Tech Stack

- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Styling
- **React Query**: Data fetching and caching

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API client and types
│   │   └── client.ts     # Backend API client
│   ├── components/       # React components
│   │   ├── ArchitectureViz.tsx  # Diagram viewer
│   │   ├── Chat.tsx             # Chat interface
│   │   ├── SessionList.tsx      # Session browser
│   │   └── StatusPanel.tsx      # Status display
│   ├── hooks/            # Custom React hooks
│   │   └── useArchitect.ts      # Architect state management
│   ├── types/            # TypeScript types
│   │   └── index.ts      # Shared type definitions
│   ├── App.tsx           # Main app component
│   ├── main.tsx          # Entry point
│   └── index.css         # Global styles
├── public/               # Static assets
├── index.html            # HTML template
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # Tailwind configuration
└── tsconfig.json         # TypeScript configuration
```

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Environment Variables

Create `.env` file:

```bash
# Backend API URL (default: /api for production)
VITE_API_URL=http://localhost:8000/api  # For local backend
```

### Running Locally

**With local backend**:

1. Start backend in another terminal:
   ```bash
   cd ..
   uv run python -m uvicorn bricksmith.web.main:app --reload
   ```

2. Start frontend:
   ```bash
   npm run dev
   ```

3. Access at: http://localhost:5173

**With deployed backend**:

```bash
# Point to deployed Databricks App
export VITE_API_URL=https://your-workspace.databricks.com/apps/bricksmith-architect/api
npm run dev
```

## Components

### ArchitectureViz

Displays architecture diagrams with interaction controls.

**Props**:
- `imageUrl`: URL to diagram image
- `iteration`: Current iteration number
- `onZoomIn?`: Zoom in callback
- `onZoomOut?`: Zoom out callback
- `onReset?`: Reset view callback

**Example**:
```tsx
<ArchitectureViz 
  imageUrl="/api/sessions/123/images/1.png"
  iteration={1}
/>
```

### Chat

Interactive chat for diagram refinement.

**Props**:
- `sessionId`: Active session ID
- `onNewTurn`: Callback when new diagram generated

**Example**:
```tsx
<Chat 
  sessionId={sessionId}
  onNewTurn={(turn) => {
    console.log('New diagram:', turn);
  }}
/>
```

### SessionList

Browse and manage sessions.

**Props**:
- `onSelectSession`: Callback when session selected
- `onCreateSession?`: Callback to create new session

**Example**:
```tsx
<SessionList 
  onSelectSession={(id) => router.push(`/session/${id}`)}
/>
```

### StatusPanel

Display status messages and loading states.

**Props**:
- `status`: Current status message
- `loading`: Loading state
- `error?`: Error message

## Styling

Uses Tailwind CSS with custom theme:

```js
// tailwind.config.js
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

## API Integration

All API calls use the centralized client:

```typescript
// src/api/client.ts
import { apiClient } from './api/client';

// List sessions
const sessions = await apiClient.listSessions();

// Get session
const session = await apiClient.getSession(sessionId);

// Send chat message
const response = await apiClient.sendMessage(sessionId, message);
```

## Type Safety

All API responses are fully typed:

```typescript
// src/types/index.ts
export interface Session {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
  turns: Turn[];
}

export interface Turn {
  iteration: number;
  prompt: string;
  image_url: string;
  score?: number;
  feedback?: string;
}
```

## Building for Production

```bash
# Build optimized bundle
npm run build

# Output goes to dist/
# - dist/index.html
# - dist/assets/
```

The build output can be:
1. Served by the FastAPI backend
2. Deployed to CDN
3. Served as static files

## Deployment

### With Databricks Apps

Frontend is automatically bundled and served by the backend when deploying:

```bash
# From project root
databricks apps deploy
```

### Standalone Deployment

Deploy to Vercel, Netlify, or similar:

1. Build production bundle:
   ```bash
   npm run build
   ```

2. Configure API URL:
   ```bash
   VITE_API_URL=https://your-backend.com/api npm run build
   ```

3. Deploy `dist/` directory

## Testing

```bash
# Run tests (when configured)
npm test

# Run with coverage
npm test -- --coverage

# Run linter
npm run lint

# Fix linting issues
npm run lint -- --fix
```

## Code Style

- **ESLint**: Configured with React and TypeScript rules
- **Prettier**: Auto-formatting on save (if configured)
- **TypeScript**: Strict mode enabled

## Performance

### Optimization Tips

1. **Code splitting**: Vite automatically splits code
2. **Lazy loading**: Use `React.lazy()` for routes
3. **Image optimization**: Use WebP format when possible
4. **Caching**: API responses cached with React Query
5. **Bundle size**: Monitor with `npm run build -- --analyze`

### Bundle Size

Target sizes:
- JavaScript: < 200KB gzipped
- CSS: < 50KB gzipped
- Total: < 300KB gzipped

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### Development Server Won't Start

**Check**:
1. Node version: `node --version` (18+ required)
2. Dependencies: `rm -rf node_modules && npm install`
3. Port conflict: Change port in `vite.config.ts`

### API Calls Failing

**Check**:
1. Backend is running
2. `VITE_API_URL` is correct
3. CORS is configured on backend
4. Network tab in browser devtools

### Build Errors

**Common issues**:
1. TypeScript errors: `npm run type-check`
2. Missing dependencies: `npm install`
3. Outdated dependencies: `npm update`

## Contributing

1. Create feature branch
2. Make changes
3. Test locally
4. Run linter: `npm run lint`
5. Build: `npm run build`
6. Submit PR

## Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Query](https://tanstack.com/query/latest)
