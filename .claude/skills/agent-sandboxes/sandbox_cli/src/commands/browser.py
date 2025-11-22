#!/usr/bin/env python3
"""
Browser automation tools for sandbox validation.

Provides commands to control a Chrome instance for visual validation of sandbox applications.
"""

import sys
import json
import subprocess
import time
import tempfile
import asyncio
from pathlib import Path
from typing import Optional, Any
from functools import wraps

import click
from rich.console import Console

# Playwright is loaded dynamically to avoid import errors if not installed
try:
    from playwright.async_api import async_playwright, Browser, Page

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    # Type stubs for when Playwright is not installed
    Browser = None  # type: ignore
    Page = None  # type: ignore

console = Console()

DEFAULT_PORT = 9222


def run_async(f):
    """Decorator to run async functions in a click command."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return asyncio.run(f(*args, **kwargs))
        except RuntimeError as e:
            if "This event loop is already running" in str(e):
                # If we're already in a loop, just return the coroutine
                # This handles cases where click might be running in a loop (unlikely here but good practice)
                return f(*args, **kwargs)
            raise

    return wrapper


def get_playwright_chromium_path() -> str:
    """Find Playwright's Chromium executable."""
    import platform
    import glob

    system = platform.system()
    home = Path.home()

    # Playwright cache locations by platform
    if system == "Darwin":  # macOS
        cache_dir = home / "Library/Caches/ms-playwright"
        chromium_pattern = "chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium"
    elif system == "Windows":
        cache_dir = home / "AppData/Local/ms-playwright"
        chromium_pattern = "chromium-*/chrome-win/chrome.exe"
    else:  # Linux
        cache_dir = home / ".cache/ms-playwright"
        chromium_pattern = "chromium-*/chrome-linux/chrome"

    # Find the most recent Chromium installation
    chromium_paths = sorted(glob.glob(str(cache_dir / chromium_pattern)), reverse=True)

    if chromium_paths:
        return chromium_paths[0]

    # Fallback error message
    console.print("[red]✗ Playwright Chromium not found[/red]")
    console.print("\nInstall it with:")
    console.print("  [cyan]uv run playwright install chromium[/cyan]")
    raise RuntimeError(
        "Playwright Chromium not installed. Run: uv run playwright install chromium"
    )


def ensure_playwright():
    """Ensure Playwright is installed."""
    if not PLAYWRIGHT_AVAILABLE:
        console.print("[red]✗ Playwright is not installed[/red]")
        console.print("\nInstall it with:")
        console.print("  [cyan]uv pip install playwright[/cyan]")
        console.print("  [cyan]uv run playwright install chromium[/cyan]")
        sys.exit(1)


async def connect_browser(playwright, port: int = DEFAULT_PORT) -> Browser:
    """Connect to running Playwright Chromium instance on specified port."""
    browser_url = f"http://localhost:{port}"
    try:
        browser = await playwright.chromium.connect_over_cdp(browser_url)
        return browser
    except Exception as e:
        console.print(f"[red]✗ Could not connect to Chromium on port {port}[/red]")
        console.print(f"  Error: {e}")
        console.print(f"\n  Run: [cyan]sbx browser start --port {port}[/cyan]")
        sys.exit(1)


async def get_active_page(browser: Browser) -> Page:
    """Get the most recently active page."""
    contexts = browser.contexts
    if not contexts:
        raise RuntimeError("No browser contexts found")

    pages = contexts[0].pages
    if not pages:
        raise RuntimeError("No pages found")

    return pages[-1]  # Most recent page


@click.group()
def browser():
    """
    Browser automation tools for UI validation using Playwright's Chromium.

    Start Playwright's isolated Chromium with remote debugging to validate
    sandbox applications visually. This uses a separate Chromium instance
    and will NOT interfere with your Chrome browser.

    Workflow:
        1. sbx browser start         # Start Playwright Chromium
        2. sbx browser nav <url>     # Navigate to your app
        3. sbx browser screenshot    # Take screenshot
        4. sbx browser eval <js>     # Run JavaScript checks
        5. sbx browser close         # Close browser

    All commands connect to Chromium on port 9222 by default.
    Use --port for parallel agents (e.g., --port 9223).
    """
    pass


@browser.command()
@click.option("--profile", is_flag=True, help="Use your default Chrome profile")
@click.option("--user-data-dir", type=click.Path(), help="Custom profile directory")
@click.option("--headed", is_flag=True, help="Show browser window (default: headless)")
@click.option(
    "--port", type=int, default=DEFAULT_PORT, help=f"CDP port (default: {DEFAULT_PORT})"
)
@run_async
async def start(profile: bool, user_data_dir: Optional[str], headed: bool, port: int):
    """
    Start Playwright's Chromium with remote debugging enabled (headless by default).

    Examples:
        # Start headless on default port 9222
        sbx browser start

        # Start on custom port (for parallel agents)
        sbx browser start --port 9223

        # Start with visible browser window
        sbx browser start --headed

        # Start with your Chrome profile
        sbx browser start --profile
    """
    ensure_playwright()

    # NOTE: We do NOT kill Chrome processes anymore - this uses Playwright's isolated Chromium
    # Your Chrome browser will continue to work normally

    # Check if port is already in use BEFORE starting
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_in_use = sock.connect_ex(("localhost", port)) == 0
    sock.close()

    if port_in_use:
        console.print(f"[red]✗ Port {port} is already in use[/red]")
        console.print(
            f"\n[yellow]Another browser instance is running on port {port}.[/yellow]"
        )
        console.print(f"[yellow]Try using a different port:[/yellow]")
        console.print(f"  [cyan]sbx browser start --port {port + 1}[/cyan]")
        sys.exit(1)

    # Determine profile directory
    if user_data_dir:
        profile_dir = Path(user_data_dir)
    elif profile:
        # Copy default profile to temp location (Chrome doesn't allow debugging on default)
        import shutil

        if sys.platform == "darwin":
            default_profile = Path.home() / "Library/Application Support/Google/Chrome"
        elif sys.platform == "win32":
            default_profile = Path.home() / "AppData/Local/Google/Chrome/User Data"
        else:
            default_profile = Path.home() / ".config/google-chrome"

        profile_dir = Path.home() / ".cache/playwright-browser-profile"
        profile_dir.mkdir(parents=True, exist_ok=True)

        # Only copy if not already copied
        if not (profile_dir / "Default").exists():
            console.print("Copying Chrome profile (first time only)...")
            shutil.copytree(default_profile, profile_dir, dirs_exist_ok=True)
    else:
        # Fresh profile for Playwright Chromium
        profile_dir = Path.home() / ".cache/playwright-browser-temp"
        profile_dir.mkdir(parents=True, exist_ok=True)

    # Start Playwright's Chromium (not your system Chrome!)
    chromium_path = get_playwright_chromium_path()
    cmd = [
        chromium_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
    ]

    # Add headless flags unless --headed is specified
    if not headed:
        cmd.extend(
            [
                "--headless=new",  # New headless mode (Chrome 109+)
                "--disable-gpu",  # Recommended for headless
                "--no-sandbox",  # Sometimes needed in containerized environments
            ]
        )

    # Start detached
    if sys.platform == "win32":
        subprocess.Popen(cmd, creationflags=subprocess.DETACHED_PROCESS)
    else:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

    # Wait for Chromium to be ready
    mode = "headed" if headed else "headless"
    console.print(f"Starting Playwright Chromium ({mode}) on port {port}...")

    for i in range(30):
        try:
            async with async_playwright() as playwright:
                # Try to connect to the browser
                browser_conn = await connect_browser(playwright, port)
                await browser_conn.close()

            profile_msg = " with your profile" if profile or user_data_dir else ""
            console.print(
                f"[green]✓ Playwright Chromium started on port {port} ({mode}){profile_msg}[/green]"
            )
            console.print(
                f"[dim]Your Chrome browser is unaffected and can be used normally[/dim]"
            )
            return
        except Exception:
            if i == 29:  # Last attempt
                raise
            time.sleep(0.5)

    console.print(f"[red]✗ Failed to start Playwright Chromium on port {port}[/red]")
    sys.exit(1)


@browser.command()
@click.argument("url")
@click.option("--new", is_flag=True, help="Open in new tab")
@click.option(
    "--port", type=int, default=DEFAULT_PORT, help=f"CDP port (default: {DEFAULT_PORT})"
)
@run_async
async def nav(url: str, new: bool, port: int):
    """
    Navigate to a URL.

    Examples:
        # Navigate in current tab
        sbx browser nav https://example.com

        # Navigate using custom port
        sbx browser nav https://example.com --port 9223

        # Open in new tab
        sbx browser nav https://example.com --new
    """
    async with async_playwright() as playwright:
        browser_conn = await connect_browser(playwright, port)

        try:
            if new:
                context = browser_conn.contexts[0]
                page = await context.new_page()
                await page.goto(url, wait_until="domcontentloaded")
                console.print(f"[green]✓ Opened: {url}[/green]")
            else:
                page = await get_active_page(browser_conn)
                await page.goto(url, wait_until="domcontentloaded")
                console.print(f"[green]✓ Navigated to: {url}[/green]")
        finally:
            await browser_conn.close()


@browser.command()
@click.argument("code")
@click.option(
    "--port", type=int, default=DEFAULT_PORT, help=f"CDP port (default: {DEFAULT_PORT})"
)
@run_async
async def eval(code: str, port: int):
    """
    Execute JavaScript in the active page.

    Examples:
        # Get page title
        sbx browser eval "document.title"

        # Get all button texts
        sbx browser eval "Array.from(document.querySelectorAll('button')).map(b => b.textContent)"

        # Check for errors
        sbx browser eval "window.errors || []"
    """
    async with async_playwright() as playwright:
        browser_conn = await connect_browser(playwright, port)

        try:
            page = await get_active_page(browser_conn)
            result = await page.evaluate(f"(async () => {{ return ({code}); }})()")

            # Format output
            if isinstance(result, list):
                for i, item in enumerate(result):
                    if i > 0:
                        click.echo()
                    if isinstance(item, dict):
                        for key, value in item.items():
                            click.echo(f"{key}: {value}")
                    else:
                        click.echo(item)
            elif isinstance(result, dict):
                for key, value in result.items():
                    click.echo(f"{key}: {value}")
            else:
                click.echo(result)
        finally:
            await browser_conn.close()


@browser.command()
@click.option("--path", type=click.Path(), help="Save to specific path")
@click.option("--full", is_flag=True, help="Full page screenshot")
@click.option(
    "--port", type=int, default=DEFAULT_PORT, help=f"CDP port (default: {DEFAULT_PORT})"
)
@run_async
async def screenshot(path: Optional[str], full: bool, port: int):
    """
    Take a screenshot of the active page.

    Examples:
        # Screenshot to temp directory
        sbx browser screenshot

        # Screenshot to specific path
        sbx browser screenshot --path /tmp/my-app.png

        # Full page screenshot
        sbx browser screenshot --full
    """
    async with async_playwright() as playwright:
        browser_conn = await connect_browser(playwright, port)

        try:
            page = await get_active_page(browser_conn)

            if path:
                filepath = Path(path)
            else:
                filename = f"screenshot-{int(time.time())}.png"
                filepath = Path(tempfile.gettempdir()) / filename

            await page.screenshot(path=str(filepath), full_page=full)
            console.print(f"[green]✓ Screenshot saved:[/green] {filepath}")
        finally:
            await browser_conn.close()


@browser.command()
@click.argument("message")
@click.option(
    "--port", type=int, default=DEFAULT_PORT, help=f"CDP port (default: {DEFAULT_PORT})"
)
@run_async
async def pick(message: str, port: int):
    """
    Interactive element picker - click elements to inspect them.

    Examples:
        sbx browser pick "Select the submit button"
        sbx browser pick "Click the navigation menu"

    Controls:
        - Click: Select single element (finishes)
        - Cmd/Ctrl+Click: Multi-select (continue selecting)
        - Enter: Finish with current selections
        - ESC: Cancel
    """
    async with async_playwright() as playwright:
        browser_conn = await connect_browser(playwright, port)

        try:
            page = await get_active_page(browser_conn)

            # Inject picker JavaScript
            picker_js = """
            (message) => {
                return new Promise((resolve) => {
                    const selections = [];
                    const selectedElements = new Set();

                    const overlay = document.createElement("div");
                    overlay.style.cssText = "position:fixed;top:0;left:0;width:100%;height:100%;z-index:2147483647;pointer-events:none";

                    const highlight = document.createElement("div");
                    highlight.style.cssText = "position:absolute;border:2px solid #3b82f6;background:rgba(59,130,246,0.1);transition:all 0.1s";
                    overlay.appendChild(highlight);

                    const banner = document.createElement("div");
                    banner.style.cssText = "position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1f2937;color:white;padding:12px 24px;border-radius:8px;font:14px sans-serif;box-shadow:0 4px 12px rgba(0,0,0,0.3);pointer-events:auto;z-index:2147483647";
                    banner.textContent = `${message} (${selections.length} selected, Cmd/Ctrl+click for multi, Enter to finish, ESC to cancel)`;

                    document.body.append(banner, overlay);

                    const cleanup = () => {
                        document.removeEventListener("mousemove", onMove, true);
                        document.removeEventListener("click", onClick, true);
                        document.removeEventListener("keydown", onKey, true);
                        overlay.remove();
                        banner.remove();
                        selectedElements.forEach(el => el.style.outline = "");
                    };

                    const buildElementInfo = (el) => {
                        const parents = [];
                        let current = el.parentElement;
                        while (current && current !== document.body) {
                            parents.push(current.tagName.toLowerCase() +
                                    (current.id ? `#${current.id}` : "") +
                                    (current.className ? `.${current.className.trim().replace(/\\s+/g, ".")}` : ""));
                            current = current.parentElement;
                        }
                        return {
                            tag: el.tagName.toLowerCase(),
                            id: el.id || null,
                            class: el.className || null,
                            text: el.textContent?.trim().slice(0, 200) || null,
                            html: el.outerHTML.slice(0, 500),
                            parents: parents.join(" > ")
                        };
                    };

                    const onMove = (e) => {
                        const el = document.elementFromPoint(e.clientX, e.clientY);
                        if (!el || overlay.contains(el) || banner.contains(el)) return;
                        const r = el.getBoundingClientRect();
                        highlight.style.cssText = `position:absolute;border:2px solid #3b82f6;background:rgba(59,130,246,0.1);top:${r.top}px;left:${r.left}px;width:${r.width}px;height:${r.height}px`;
                    };

                    const onClick = (e) => {
                        if (banner.contains(e.target)) return;
                        e.preventDefault();
                        e.stopPropagation();
                        const el = document.elementFromPoint(e.clientX, e.clientY);
                        if (!el || overlay.contains(el) || banner.contains(el)) return;

                        if (e.metaKey || e.ctrlKey) {
                            if (!selectedElements.has(el)) {
                                selectedElements.add(el);
                                el.style.outline = "3px solid #10b981";
                                selections.push(buildElementInfo(el));
                                banner.textContent = `${message} (${selections.length} selected, Enter to finish)`;
                            }
                        } else {
                            cleanup();
                            resolve(selections.length > 0 ? selections : buildElementInfo(el));
                        }
                    };

                    const onKey = (e) => {
                        if (e.key === "Escape") {
                            cleanup();
                            resolve(null);
                        } else if (e.key === "Enter" && selections.length > 0) {
                            cleanup();
                            resolve(selections);
                        }
                    };

                    document.addEventListener("mousemove", onMove, true);
                    document.addEventListener("click", onClick, true);
                    document.addEventListener("keydown", onKey, true);
                });
            }
            """

            result = await page.evaluate(picker_js, message)

            if result is None:
                console.print("[yellow]Cancelled[/yellow]")
                return

            # Output results
            if isinstance(result, list):
                for i, item in enumerate(result):
                    if i > 0:
                        click.echo()
                    for key, value in item.items():
                        click.echo(f"{key}: {value}")
            else:
                for key, value in result.items():
                    click.echo(f"{key}: {value}")
        finally:
            await browser_conn.close()


@browser.command()
@click.option(
    "--port", type=int, default=DEFAULT_PORT, help=f"CDP port (default: {DEFAULT_PORT})"
)
@run_async
async def cookies(port: int):
    """
    Get cookies from the active page.

    Returns all cookies as JSON.
    """
    async with async_playwright() as playwright:
        browser_conn = await connect_browser(playwright, port)

        try:
            context = browser_conn.contexts[0]
            cookies_data = await context.cookies()
            click.echo(json.dumps(cookies_data, indent=2))
        finally:
            await browser_conn.close()


@browser.command()
@click.option(
    "--port", type=int, default=DEFAULT_PORT, help=f"CDP port (default: {DEFAULT_PORT})"
)
@run_async
async def close(port: int):
    """
    Close the browser.

    Closes all tabs and shuts down the Chrome instance.
    """
    try:
        async with async_playwright() as playwright:
            browser_conn = await connect_browser(playwright, port)
            await browser_conn.close()
            console.print(f"[green]✓ Browser on port {port} closed[/green]")
    except Exception:
        console.print(f"[green]✓ No browser running on port {port}[/green]")


@browser.command()
@click.option(
    "--port", type=int, default=DEFAULT_PORT, help=f"CDP port (default: {DEFAULT_PORT})"
)
@run_async
async def status(port: int):
    """Check if browser is running and accessible."""
    try:
        async with async_playwright() as playwright:
            browser_conn = await connect_browser(playwright, port)
            contexts = browser_conn.contexts
            if contexts:
                pages = contexts[0].pages
                console.print(f"[green]✓ Browser is running on port {port}[/green]")
                console.print(f"  Open tabs: {len(pages)}")
                if pages:
                    current_page = pages[-1]
                    console.print(f"  Current URL: {current_page.url}")
            await browser_conn.close()
    except Exception as e:
        console.print(f"[red]✗ Browser not running on port {port}[/red]")
        console.print(f"  Run: [cyan]sbx browser start --port {port}[/cyan]")


if __name__ == "__main__":
    browser()
