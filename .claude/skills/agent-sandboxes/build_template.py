#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "e2b",
#   "python-dotenv",
# ]
# ///

"""
Build full-stack template - optimized for Vite + Vue + TypeScript + Pinia frontend,
FastAPI backend, and SQLite database with Node.js 22 and uv pre-installed.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from e2b import Template

# Load .env from project root
# Path from build_template.py: agent-sandboxes -> skills -> .claude -> root (3 parents)
root_dir = Path(__file__).parent.parent.parent.parent
load_dotenv(root_dir / ".env")

TEMPLATE_NAME = "fullstack-vue-fastapi-node22"

print("=== Building Full-Stack Template ===\n")
print("Stack: Vite + Vue 3 + TypeScript + Pinia + FastAPI + SQLite")
print("Optimizations: Node.js 22, uv, compatible Vite 5.x\n")

# Define the template with pre-installed tools
print("📝 Defining template...")
template = (
    Template()
    .from_node_image('22')  # Start with Node.js 22 base image (globally available)
    .apt_install(['sqlite3'])  # Install SQLite3 CLI for database operations
    .run_cmd("curl -LsSf https://astral.sh/uv/install.sh | sh")  # Install uv
    .run_cmd("sudo ln -sf /home/user/.local/bin/uv /usr/local/bin/uv")  # Global uv access
    # Verify tools are installed correctly
    .run_cmd("node --version && npm --version && sqlite3 --version")
)

print(f"   ✓ Template defined: {TEMPLATE_NAME}")
print("   Base: Node.js 22 (from official E2B Node.js 22 image)")
print("   Tools installed:")
print("     - Node.js 22.x (globally available as default)")
print("     - npm (pre-installed with Node.js)")
print("     - sqlite3 (CLI for database operations)")
print("     - uv (Python package manager, globally accessible)")
print("")
print("   Note: Projects will install their own dependencies via npm install")
print("   This ensures version consistency and proper node_modules structure")

# Build the template
print(f"\n🏗️  Building template '{TEMPLATE_NAME}'...")
print("   (This may take a few minutes...)\n")

try:
    Template.build(
        template,
        alias=TEMPLATE_NAME,
        cpu_count=2,
        memory_mb=2048,  # 2GB for building frontend + backend
    )
    print(f"   ✅ Template built successfully: {TEMPLATE_NAME}")
    print(f"\n💡 Use this template in your workflow:")
    print(f"   sbx init --template {TEMPLATE_NAME} --timeout 3600")
    print(f"\n📦 Pre-installed tools:")
    print(f"   • Node.js 22.x (globally available)")
    print(f"   • npm (latest for Node.js 22)")
    print(f"   • sqlite3 (CLI for database operations)")
    print(f"   • uv (Python package manager)")
    print(f"\n🚀 Benefits:")
    print(f"   • Node.js 22 eliminates Vite 7 compatibility issues")
    print(f"   • SQLite3 CLI ready for database creation/debugging")
    print(f"   • Projects install their own dependencies (proper version control)")
    print(f"   • uv + sqlite3 pre-installed saves ~45 seconds per build")
    print(f"   • Consistent, tested environment")
    print(f"   • Template builds in ~2-3 minutes (minimal, focused setup)")
except Exception as e:
    print(f"   ❌ Build failed: {e}")
    print("\n   Troubleshooting:")
    print("   - Ensure E2B_API_KEY is set in .env")
    print("   - Check your E2B account has template build permissions")
    print("   - Try reducing cpu_count or memory_mb if resource limits exceeded")
