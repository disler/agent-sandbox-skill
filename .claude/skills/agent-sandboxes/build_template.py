#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "e2b",
#   "python-dotenv",
#   "click",
# ]
# ///

"""
Build full-stack template - optimized for Vite + Vue + TypeScript + Pinia frontend,
FastAPI backend, and SQLite database with Node.js 22 and uv pre-installed.

Supports 5 resource tiers:
  --tier super-lite  (default) 2 vCPU / 2GB  - Simple apps, sequential tasks
  --tier lite                  2 vCPU / 4GB  - More RAM for browser tests
  --tier standard              4 vCPU / 4GB  - Parallel builds, Playwright
  --tier heavy                 4 vCPU / 8GB  - Multi-browser, complex apps
  --tier max                   8 vCPU / 8GB  - Everything parallel, fastest
"""

import click
from pathlib import Path
from dotenv import load_dotenv
from e2b import Template

# Load .env from project root
# Path from build_template.py: agent-sandboxes -> skills -> .claude -> root (3 parents)
root_dir = Path(__file__).parent.parent.parent.parent
load_dotenv(root_dir / ".env")

BASE_TEMPLATE_NAME = "fullstack-vue-fastapi-node22"

# Tier configurations: (cpu_count, memory_mb, description, hourly_cost)
TIERS = {
    "super-lite": (2, 2048, "Simple apps, sequential tasks", "$0.13/hr"),
    "lite": (2, 4096, "More RAM for browser tests", "$0.15/hr"),
    "standard": (4, 4096, "Parallel builds, Playwright", "$0.27/hr"),
    "heavy": (4, 8192, "Multi-browser, complex apps", "$0.33/hr"),
    "max": (8, 8192, "Everything parallel, fastest", "$0.44/hr"),
}

def print_tier_table():
    """Print available tiers with their configurations."""
    print("\n📊 Available Tiers:")
    print("   ┌─────────────┬───────┬────────┬─────────┬────────────────────────────────┐")
    print("   │ Tier        │ vCPU  │ RAM    │ Cost    │ Best For                       │")
    print("   ├─────────────┼───────┼────────┼─────────┼────────────────────────────────┤")
    for tier_name, (cpu, ram, desc, cost) in TIERS.items():
        ram_gb = ram // 1024
        default = " (default)" if tier_name == "super-lite" else ""
        print(f"   │ {tier_name:<11} │ {cpu:<5} │ {ram_gb}GB    │ {cost:<7} │ {desc:<30} │")
    print("   └─────────────┴───────┴────────┴─────────┴────────────────────────────────┘")


@click.command()
@click.option(
    "--tier",
    type=click.Choice(list(TIERS.keys())),
    default="super-lite",
    help="Resource tier for the template (default: super-lite)",
)
@click.option(
    "--list-tiers",
    is_flag=True,
    help="List available tiers and exit",
)
def build_template(tier: str, list_tiers: bool):
    """Build a full-stack E2B template with configurable resource tiers."""

    if list_tiers:
        print_tier_table()
        return

    cpu_count, memory_mb, description, hourly_cost = TIERS[tier]
    ram_gb = memory_mb // 1024

    # Template name includes tier for non-default tiers
    if tier == "super-lite":
        template_name = BASE_TEMPLATE_NAME
    else:
        template_name = f"{BASE_TEMPLATE_NAME}-{tier}"

    print("=== Building Full-Stack Template ===\n")
    print("Stack: Vite + Vue 3 + TypeScript + Pinia + FastAPI + SQLite")
    print("Optimizations: Node.js 22, uv, compatible Vite 5.x\n")

    print(f"⚙️  Resource Tier: {tier}")
    print(f"   • vCPU: {cpu_count}")
    print(f"   • RAM: {ram_gb}GB")
    print(f"   • Cost: {hourly_cost}")
    print(f"   • Best for: {description}")

    # Define the template with pre-installed tools
    print("\n📝 Defining template...")
    template = (
        Template()
        .from_node_image("22")  # Start with Node.js 22 base image (globally available)
        .apt_install(["sqlite3"])  # Install SQLite3 CLI for database operations
        .run_cmd("curl -LsSf https://astral.sh/uv/install.sh | sh")  # Install uv
        .run_cmd(
            "sudo ln -sf /home/user/.local/bin/uv /usr/local/bin/uv"
        )  # Global uv access
        # Verify tools are installed correctly
        .run_cmd("node --version && npm --version && sqlite3 --version")
    )

    print(f"   ✓ Template defined: {template_name}")
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
    print(f"\n🏗️  Building template '{template_name}'...")
    print("   (This may take a few minutes...)\n")

    try:
        Template.build(
            template,
            alias=template_name,
            cpu_count=cpu_count,
            memory_mb=memory_mb,
        )
        print(f"   ✅ Template built successfully: {template_name}")
        print(f"\n💡 Use this template in your workflow:")
        print(f"   sbx init --template {template_name}")
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
        print(f"\n💰 Cost Estimate:")
        print(f"   • Per hour: {hourly_cost}")
        print(f"   • Per day (24h): ${float(hourly_cost.replace('$','').replace('/hr','')) * 24:.2f}")
    except Exception as e:
        print(f"   ❌ Build failed: {e}")
        print("\n   Troubleshooting:")
        print("   - Ensure E2B_API_KEY is set in .env")
        print("   - Check your E2B account has template build permissions")
        print("   - Try reducing tier if resource limits exceeded")


if __name__ == "__main__":
    build_template()
