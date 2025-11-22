# Simple Nano Banana Generator

Build a minimal AI image generator. Enter a prompt, click generate, see your image. That's it.

## Prerequisites

**IMPORTANT**: Before starting, read the Nano Banana documentation:
```bash
Read ai_docs/gemini-3-nano-banana.md
```

Focus on the basic text-to-image generation example.

**Environment Setup**:
- Validate that you have access to a Gemini API key - check the root `.env` file for `GEMINI_API_KEY` without exposing it
- The backend will load this key using `python-dotenv`

## Core Features

### Single Page Interface
- Text input field for prompt (full width)
- Generate button
- Image display area (shows current generation only)
- Download button (appears after generation)
- Minimal settings in corner: model selector (Fast/Pro), aspect ratio dropdown

## Database Schema

```sql
-- Store only the current/most recent image
CREATE TABLE current_image (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    prompt TEXT NOT NULL,
    model TEXT NOT NULL,
    aspect_ratio TEXT NOT NULL,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Minimal settings
CREATE TABLE settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    api_key TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Backend API

- `POST /api/generate` - Generate image from prompt
  - Body: `{ prompt, model, aspect_ratio }`
  - Returns: `{ image_url, prompt }`
- `GET /api/current` - Get current image
- `GET /api/settings` - Get API key status
- `PUT /api/settings` - Set API key
- `GET /static/images/{filename}` - Serve image

## Frontend Structure

**Single Page:**
- Top: Image display area (large, centered)
- Bottom: Prompt input field + Generate button
- Corner: Small settings icon (opens modal for API key + model/aspect ratio)

**Layout:**
```
┌─────────────────────────────────┐
│    [Image Display Area]         │
│    (shows generated image)      │
│    [Download Button]             │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│ [Text Input: "Describe image"]  │
│ [Model: Fast ▾] [1:1 ▾] [Generate] │
└─────────────────────────────────┘
```

**Components:**
- ImageDisplay (shows current image or placeholder)
- PromptInput (text field)
- GenerateButton (with loading state)
- SettingsModal (API key input, opens on first use)

## Key Implementation Details

**Backend:**
1. Install `google-genai`, `python-dotenv`, and `pillow`
2. Store API key in database
3. Save only one image at a time to `/static/images/current.png`
4. Overwrite previous image on each generation
5. Basic error handling

**Frontend:**
1. Install `axios` for API requests
2. Single component for the entire UI
3. Show loading spinner during generation
4. Display image immediately after generation
5. Prompt for API key on first use

**API Integration:**
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=settings.api_key)

response = client.models.generate_content(
    model=model,
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio
        )
    )
)

# Save single image
for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("static/images/current.png")
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

- Enter prompt and generate image
- View generated image immediately
- Download current image
- Switch between Fast/Pro models
- Change aspect ratio (1:1, 16:9, 9:16)
- Set API key once
- Clean, minimal UI with no clutter
- Fast, responsive experience

**Build time: ~10-15 minutes**
