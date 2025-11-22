# Nano Banana Image Studio

Build a professional image generation, management, and editing studio powered by Gemini's Nano Banana (image generation) API. Create, edit, organize, and iterate on AI-generated images with multi-turn conversations and advanced controls.

## Prerequisites

**IMPORTANT**: Before starting, read the complete Nano Banana documentation:
```bash
Read ai_docs/gemini-3-nano-bannana.md
```

This contains essential API details, code examples, configuration options, and best practices for image generation and editing.

**Environment Setup**:
- Validate that you have access to a Gemini API key - check the root `.env` file for `GEMINI_API_KEY` without exposing it
- The backend will load this key using `python-dotenv`

## Core Features

### 1. Image Generation (Text-to-Image)
- Text prompt input with multi-line support
- Model selection: `gemini-2.5-flash-image` (fast, 1K) or `gemini-3-pro-image-preview` (advanced, up to 4K)
- Aspect ratio selector: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
- Resolution selector for Pro model: 1K, 2K, 4K
- Response modality toggle: Text + Image OR Image only
- Google Search grounding toggle (Pro model only)
- Generate button with loading state
- Display generated image with download option
- Show generation metadata (model used, resolution, aspect ratio, token count)

### 2. Image Editing (Image + Text-to-Image)
- Upload existing image for editing
- Text prompt to describe desired changes
- Support for multiple editing modes:
  - Add/remove elements
  - Inpainting (semantic masking)
  - Style transfer
  - Color grading adjustments
- Preserve original composition option
- Side-by-side comparison (before/after)
- Apply edits and generate new version

### 3. Multi-Turn Conversations
- Create persistent chat sessions for iterative refinement
- Display conversation history with image thumbnails
- Continue editing from any point in conversation
- Send follow-up prompts to refine images
- Auto-handle thought signatures (for Pro model)
- Show "thinking process" images (Pro model)
- Session management (save, load, delete sessions)

### 4. Image Gallery & Management
- Grid view of all generated images
- Filter by:
  - Model (Flash vs Pro)
  - Resolution (1K, 2K, 4K)
  - Aspect ratio
  - Date range
  - Has edits (original vs edited)
  - Session/conversation
- Sort by: newest, oldest, most edited
- Bulk operations: download, delete
- Full-screen image viewer with metadata overlay
- Image versioning (track edits/iterations)

### 5. Settings & Configuration
- API Key management (secure storage)
- Default model preference
- Default aspect ratio
- Default resolution (for Pro model)
- Enable/disable Google Search grounding by default
- Response modality preference
- Auto-save conversations toggle
- Storage limits and cleanup rules
- Export format preferences (PNG, JPG, WEBP)

### 6. Advanced Features
- Multi-image composition (up to 14 reference images for Pro model)
- Batch generation from prompt list
- Prompt templates library (photorealistic, illustration, product, minimalist, etc.)
- Prompt history and favorites
- Image metadata viewer (full response data, grounding sources, thought process)
- Cost calculator (token usage tracking)
- Export conversation as markdown with embedded images

## Technical Requirements

### Database Schema

```sql
-- Store generated images with metadata
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    prompt TEXT NOT NULL,
    model TEXT NOT NULL,
    aspect_ratio TEXT NOT NULL,
    resolution TEXT,
    response_modality TEXT NOT NULL,
    google_search_enabled BOOLEAN DEFAULT 0,
    token_count INTEGER,
    thought_signature TEXT,
    grounding_metadata TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- Track conversation sessions for multi-turn editing
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    model TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Store conversation history for each session
CREATE TABLE conversation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    message TEXT,
    image_id INTEGER,
    thought_signature TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE SET NULL
);

-- User settings and configuration
CREATE TABLE settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    api_key TEXT,
    default_model TEXT DEFAULT 'gemini-2.5-flash-image',
    default_aspect_ratio TEXT DEFAULT '1:1',
    default_resolution TEXT DEFAULT '1K',
    default_response_modality TEXT DEFAULT 'TEXT_IMAGE',
    google_search_default BOOLEAN DEFAULT 0,
    auto_save_conversations BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Prompt templates for quick generation
CREATE TABLE prompt_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    template TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Track image edits and versions
CREATE TABLE image_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_image_id INTEGER NOT NULL,
    edited_image_id INTEGER NOT NULL,
    edit_prompt TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (original_image_id) REFERENCES images(id) ON DELETE CASCADE,
    FOREIGN KEY (edited_image_id) REFERENCES images(id) ON DELETE CASCADE
);
```

### Backend API

**Image Generation:**
- `POST /api/generate` - Generate image from text prompt
  - Body: `{ prompt, model, aspect_ratio, resolution?, response_modality, google_search_enabled }`
  - Returns: `{ image_id, image_url, metadata, text_response?, grounding_data? }`

**Image Editing:**
- `POST /api/edit` - Edit existing image with text prompt
  - Body: `{ image_id, prompt, model, aspect_ratio?, resolution? }`
  - Returns: `{ new_image_id, image_url, metadata }`

**Session Management:**
- `POST /api/sessions` - Create new conversation session
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{id}` - Get session with conversation history
- `PUT /api/sessions/{id}` - Update session name
- `DELETE /api/sessions/{id}` - Delete session and images
- `POST /api/sessions/{id}/message` - Send message in session (multi-turn)

**Image Management:**
- `GET /api/images` - List all images with filtering/sorting
  - Query params: `model, aspect_ratio, resolution, session_id, start_date, end_date, sort_by`
- `GET /api/images/{id}` - Get single image with full metadata
- `GET /api/images/{id}/versions` - Get all versions/edits of an image
- `GET /api/images/{id}/download` - Download image file
- `DELETE /api/images/{id}` - Delete image
- `DELETE /api/images/bulk` - Bulk delete images

**Settings:**
- `GET /api/settings` - Get current settings
- `PUT /api/settings` - Update settings
- `POST /api/settings/api-key` - Set/update API key (encrypted storage)

**Templates:**
- `GET /api/templates` - List all prompt templates
- `POST /api/templates` - Create new template
- `DELETE /api/templates/{id}` - Delete template

**File Serving:**
- `GET /static/images/{filename}` - Serve generated image files
- Configure proper CORS and cache headers for image serving
- Implement secure path traversal prevention

### Frontend Structure

**Pages:**
1. **Generate Page** (/)
   - Main prompt input area
   - Configuration panel (model, aspect ratio, resolution, etc.)
   - Generate button
   - Results display area with image and metadata

2. **Sessions Page** (/sessions)
   - List of all conversation sessions
   - Create new session button
   - Session cards with preview images
   - Click to open session detail

3. **Session Detail Page** (/sessions/:id)
   - Conversation history (messages and images)
   - New message input
   - Continue conversation controls
   - Image gallery for this session
   - Download conversation report

4. **Gallery Page** (/gallery)
   - Grid of all generated images
   - Advanced filters sidebar
   - Sort controls
   - Bulk selection mode
   - Image cards with hover preview

5. **Image Detail Page** (/images/:id)
   - Full-size image display
   - Complete metadata panel
   - Edit button (opens editor)
   - Version history
   - Download options
   - Delete confirmation

6. **Editor Page** (/edit/:id)
   - Original image display
   - Edit prompt input
   - Before/after comparison slider
   - Apply and generate new version

7. **Settings Page** (/settings)
   - API key input (masked)
   - Default preferences
   - Storage management
   - Template library

**Components:**
- ImageCard (thumbnail with metadata)
- GenerationForm (prompt input + configs)
- ConversationThread (chat-like interface)
- ImageViewer (full-screen with controls)
- FilterPanel (advanced filtering UI)
- SettingsPanel (configuration forms)
- PromptTemplateSelector (template library)
- MetadataDisplay (show generation details)
- LoadingSpinner (generation in progress)
- ErrorBoundary (API error handling)

### Key Implementation Details

**Backend:**
1. Install `google-genai`, `python-dotenv`, and `pillow`
2. Store API key securely in environment variable: `GEMINI_API_KEY`
3. Save generated images to `/static/images/` directory
4. Generate unique filenames using UUID + timestamp
5. Parse inline_data from response and save as PNG
6. Handle thought signatures for Pro model multi-turn conversations
7. Implement proper error handling for API failures
8. Add rate limiting to prevent API quota exhaustion
9. Implement image cleanup service for storage management

**Frontend:**
1. Install `axios`, `vue-router`, and `pinia` for state management
2. Create Pinia store for:
   - Images state
   - Sessions state
   - Settings state
   - UI state (loading, errors)
3. Implement image lazy loading for gallery
4. Add image caching strategy
5. Use FormData for image uploads
6. Implement optimistic UI updates
7. Add toast notifications for generation events
8. Create responsive grid layout for gallery

**API Integration:**
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Text-to-Image
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K"
        )
    )
)

# Extract and save image
for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save(f"static/images/{filename}.png")
```

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

## Success Criteria

- Generate images from text prompts with all configuration options
- Edit images conversationally with multi-turn refinement
- View all generated images in organized gallery
- Filter and search images by metadata
- Save and resume conversation sessions
- Configure settings and defaults
- Download images individually or in bulk
- Track image versions and edits
- Images properly exposed and viewable from frontend
- Secure API key storage and usage
- Professional, polished UI with smooth UX
- Proper error handling and user feedback

**Build time: ~45-60 minutes**
