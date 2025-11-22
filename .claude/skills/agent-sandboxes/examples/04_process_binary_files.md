# Example 4: Process Binary Files

## When to Use
Read this when you need to upload, process, or download binary files (images, PDFs, executables) in a sandbox.

## User Request Pattern
```
Resize this image in a sandbox
Process this PDF file
Convert this image format
Generate an image/PDF from data
```

## Workflow

### Step 1: Validate Environment
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
grep "E2B_API_KEY" ../../../../.env
```

### Step 2: Initialize Sandbox and Capture ID
```bash
uv run sbx init
# YOU capture and remember: sandbox_id = "sbx_img456resize"
```

### Step 3: Upload the Binary File
Use `sbx files upload` for binary files (images, PDFs, executables):
```bash
uv run sbx files upload sbx_img456resize ./input.jpg /home/user/input.jpg
```

**Important**: Use `upload`/`download` for binary files, not `write`/`read` (which are for text).

### Step 4: Install Processing Tools
Install uv and the required library (e.g., Pillow for images):
```bash
uv run sbx exec sbx_img456resize "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120
uv run sbx exec sbx_img456resize "/home/user/.local/bin/uv pip install --system pillow"
```

### Step 5: Write and Run Processing Script
```bash
uv run sbx files write sbx_img456resize /home/user/resize.py "from PIL import Image; img = Image.open('/home/user/input.jpg'); img.resize((800,600)).save('/home/user/output.jpg')"
uv run sbx exec sbx_img456resize "python3 /home/user/resize.py"
```

### Step 6: Download the Result
```bash
uv run sbx files download sbx_img456resize /home/user/output.jpg ./output.jpg
```

### Step 7: Clean Up
```bash
uv run sbx sandbox kill sbx_img456resize
```

## Key Points
- **Use `upload`/`download` for binary files** (images, PDFs, executables)
- **Use `write`/`read` for text files only**
- Upload source files before processing
- Install required libraries (PIL, reportlab, etc.)
- Download processed files back to local system
- Common libraries:
  - Images: `pillow` (PIL)
  - PDFs: `reportlab`, `pypdf2`
  - Data processing: `pandas`, `numpy`
- Always clean up the sandbox when done

## Binary File Types Supported
- Images: jpg, png, gif, bmp, tiff, webp
- Documents: pdf, docx, xlsx
- Archives: zip, tar, gz
- Executables: any binary format
