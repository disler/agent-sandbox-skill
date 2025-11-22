# Nano Banana Image Generator

Build a simple AI image generator powered by Gemini's Nano Banana API. Enter prompts, configure basic settings, generate images, and view your creations in a clean gallery.

## Prerequisites

**IMPORTANT**: Before starting, read the Nano Banana documentation:
```bash
Read ai_docs/gemini-3-nano-bannana.md
```

Focus on the basic text-to-image generation examples and configuration options.

**Environment Setup**:
- Validate that you have access to a Gemini API key - check the root `.env` file for `GEMINI_API_KEY` without exposing it
- The backend will load this key using `python-dotenv`

## Core Features

### 1. Image Generation
- Large text area for prompt input
- Model selector: Fast (gemini-2.5-flash-image) or Pro (gemini-3-pro-image-preview)
- Aspect ratio dropdown: 1:1, 16:9, 9:16, 4:3, 3:4
- Image count slider: 1-4 images
- Generate button with loading spinner
- Display all generated images in a grid
- Download button for each image

### 2. Image Gallery
- Grid view of all previously generated images
- Show prompt text on hover
- Click to view full-size
- Delete individual images
- Clear all images button
- Filter by model type (Fast/Pro)
- Sort by newest/oldest

### 3. Settings
- API key input (saved to database)
- Default model preference
- Default aspect ratio
- Default image count
- Save/reset settings

## Database Schema

```sql
-- Store generated images with metadata
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt TEXT NOT NULL,
    model TEXT NOT NULL,
    aspect_ratio TEXT NOT NULL,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- User settings
CREATE TABLE settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    api_key TEXT,
    default_model TEXT DEFAULT 'gemini-2.5-flash-image',
    default_aspect_ratio TEXT DEFAULT '1:1',
    default_count INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Backend API

**Generation:**
- `POST /api/generate` - Generate images from prompt
  - Body: `{ prompt, model, aspect_ratio, count }`
  - Returns: `{ images: [{ id, url, filename }] }`

**Gallery:**
- `GET /api/images` - List all images with optional filtering
  - Query params: `model`, `sort_by`
- `GET /api/images/{id}` - Get single image metadata
- `DELETE /api/images/{id}` - Delete image
- `DELETE /api/images/all` - Clear all images

**Settings:**
- `GET /api/settings` - Get current settings
- `PUT /api/settings` - Update settings

**Static Files:**
- `GET /static/images/{filename}` - Serve generated images

## Frontend Structure

**Pages:**
1. **Home/Generate** (/)
   - Prompt input area
   - Configuration controls (model, aspect ratio, count)
   - Generate button
   - Results display area

2. **Gallery** (/gallery)
   - Grid of all generated images
   - Filter by model
   - Sort controls
   - Delete actions

3. **Settings** (/settings)
   - API key input
   - Default preferences
   - Save button

**Components:**
- PromptInput (textarea with character count)
- ConfigPanel (dropdowns for model, aspect ratio, count slider)
- ImageGrid (responsive grid of images)
- ImageCard (thumbnail with prompt overlay and delete button)
- ImageModal (full-size viewer)
- SettingsForm (configuration inputs)

## Key Implementation Details

**Backend:**
1. Install `google-genai`, `python-dotenv`, and `pillow`
2. Store API key in environment variable or database (encrypted)
3. Save generated images to `/static/images/` directory
4. Generate unique filenames: `{timestamp}_{uuid}.png`
5. Handle multiple image generation in single request
6. Basic error handling for API failures

**Frontend:**
1. Install `axios` for API requests
2. Create Pinia store for images and settings state
3. Image lazy loading in gallery
4. Form validation for prompt input
5. Loading states during generation
6. Toast notifications for success/errors

**API Integration Example:**
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=settings.api_key)

# Generate images
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

# Save each generated image
for i, part in enumerate(response.parts):
    if part.inline_data is not None:
        image = part.as_image()
        filename = f"{timestamp}_{uuid}_{i}.png"
        image.save(f"static/images/{filename}")
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

- Generate 1-4 images from a single prompt
- Configure model and aspect ratio before generation
- View all generated images in organized gallery
- Download individual images
- Delete unwanted images
- Save API key and default preferences
- Images properly served from backend
- Fast, responsive UI with good UX
- Clear error messages for API failures

**Build time: ~25-30 minutes**
