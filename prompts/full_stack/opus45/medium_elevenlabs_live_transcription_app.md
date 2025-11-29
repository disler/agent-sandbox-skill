Build a **Voice Notes App with Live Transcription** that lets users capture thoughts by speaking, with real-time speech-to-text powered by ElevenLabs.

## Read This First

- `ai_docs/eleven_labs_realtime_speech_to_text.md`

**Core Features:**
1. **Notes List**: Display all notes sorted by most recent, with search/filter functionality.
2. **Voice Recording**: A prominent "Record" button that activates the microphone and begins transcription immediately.
3. **Live Transcription**: Show partial transcript in real-time as the user speaks, committed transcript becomes note content on stop.
4. **CRUD Operations**: Create, read, update, and delete notes. Auto-generate title from first line if not provided.
5. **Token Endpoint**: Backend endpoint to generate single-use ElevenLabs tokens (never expose API key to client).

**Database Schema:**
```
notes
  - id: INTEGER PRIMARY KEY
  - title: TEXT (nullable, auto-generate from first 50 chars of content if empty)
  - content: TEXT NOT NULL
  - created_at: DATETIME DEFAULT CURRENT_TIMESTAMP
  - updated_at: DATETIME DEFAULT CURRENT_TIMESTAMP
```

**Technical Requirements:**
- Install `@elevenlabs/client` for WebSocket-based realtime transcription using Scribe v2 Realtime model.
- Use VAD (Voice Activity Detection) commit strategy for automatic speech segmentation.
- Backend must proxy token generation via `/v1/single-use-token/realtime_scribe` endpoint.
- Requires `ELEVENLABS_API_KEY` environment variable.

## UI Design
Build a modern, professional interface with:
- Clean, minimal design with proper spacing
- Modern color palette (primary/secondary/accent colors)
- Responsive layout that works on mobile and desktop
- Professional typography (readable fonts, clear hierarchy)
- Smooth transitions and hover effects
- Consistent component styling throughout
- Proper form validation with user feedback
- Loading states for async operations
- Visual recording indicator (pulsing dot or waveform) during transcription
