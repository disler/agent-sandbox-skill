"""
Browser automation CLI commands.
Thin wrapper around modules.browser for CLI interface.
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Optional
from functools import wraps

import click
from rich.console import Console

from ..modules import browser as browser_module

console = Console()


def run_async(f):
    """Decorator to run async functions in a click command."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return asyncio.run(f(*args, **kwargs))
        except RuntimeError as e:
            if "This event loop is already running" in str(e):
                return f(*args, **kwargs)
            raise
    return wrapper


def ensure_initialized():
    """Check browser environment is initialized, exit with message if not."""
    if not browser_module.check_playwright_installed():
        console.print("[red]✗ Browser environment not initialized[/red]")
        console.print("\n[yellow]ERROR: Playwright is not installed[/yellow]")
        console.print("\nRun this command to initialize:")
        console.print("  [cyan]uv run sbx browser init[/cyan]")
        sys.exit(1)

    is_installed, path_or_dir = browser_module.check_chromium_installed()
    if not is_installed:
        console.print("[red]✗ Browser environment not initialized[/red]")
        console.print("\n[yellow]ERROR: Playwright Chromium not found[/yellow]")
        console.print(f"  Searched in: {path_or_dir}")
        console.print("\nRun this command to initialize:")
        console.print("  [cyan]uv run sbx browser init[/cyan]")
        sys.exit(1)

    return path_or_dir  # Return chromium path


@click.group()
def browser():
    """
    Browser automation tools for UI validation using Playwright's Chromium.

    Workflow:
        1. sbx browser init          # One-time setup
        2. sbx browser start         # Start Playwright Chromium
        3. sbx browser nav <url>     # Navigate to your app
        4. sbx browser screenshot    # Take screenshot
        5. sbx browser eval <js>     # Run JavaScript checks
        6. sbx browser close         # Close browser

    Use --port for parallel agents (e.g., --port 9223).
    """
    pass


@browser.command()
@run_async
async def init():
    """
    Initialize browser environment - install Playwright and Chromium.

    Run once before using other browser commands. Safe to run multiple times.
    """
    console.print("[bold]Initializing browser environment...[/bold]\n")

    # Check/install Playwright
    if browser_module.check_playwright_installed():
        console.print("[green]✓[/green] Playwright Python package installed")
    else:
        console.print("[yellow]Installing Playwright...[/yellow]")
        success, error = browser_module.install_playwright()
        if not success:
            console.print(f"[red]✗ Failed to install Playwright[/red]")
            console.print(f"  {error}")
            sys.exit(1)
        console.print("[green]✓[/green] Playwright installed")

    # Check/install Chromium
    is_installed, chromium_path = browser_module.check_chromium_installed()
    if is_installed:
        console.print(f"[green]✓[/green] Chromium installed")
        console.print(f"  [dim]{chromium_path}[/dim]")
    else:
        console.print("[yellow]Installing Chromium (this may take a minute)...[/yellow]")
        success, error = browser_module.install_chromium()
        if not success:
            console.print(f"[red]✗ Failed to install Chromium[/red]")
            console.print(f"  {error}")
            sys.exit(1)

        is_installed, chromium_path = browser_module.check_chromium_installed()
        if not is_installed:
            console.print(f"[red]✗ Chromium installation failed[/red]")
            sys.exit(1)
        console.print(f"[green]✓[/green] Chromium installed")
        console.print(f"  [dim]{chromium_path}[/dim]")

    # Verify
    console.print("\n[dim]Verifying installation...[/dim]")
    success, version = browser_module.verify_chromium(chromium_path)
    if success:
        console.print(f"[green]✓[/green] Chromium verified: {version}")
    else:
        console.print("[yellow]![/yellow] Could not verify Chromium version (may still work)")

    console.print("\n[green][bold]Browser environment ready![/bold][/green]")
    console.print("\nNext steps:")
    console.print("  [cyan]sbx browser start[/cyan]              # Start browser")
    console.print("  [cyan]sbx browser start --port 9223[/cyan]  # Custom port for parallel agents")


@browser.command()
@click.option("--profile", is_flag=True, help="Use your default Chrome profile")
@click.option("--user-data-dir", type=click.Path(), help="Custom profile directory")
@click.option("--headed", is_flag=True, help="Show browser window (default: headless)")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port (default: 9222)")
@click.option("--width", type=int, default=browser_module.DEFAULT_VIEWPORT_WIDTH, help="Viewport width (default: 1920)")
@click.option("--height", type=int, default=browser_module.DEFAULT_VIEWPORT_HEIGHT, help="Viewport height (default: 1080)")
@click.option("--mobile", is_flag=True, help="Mobile mode: iPhone viewport (390x844), touch events, mobile user agent")
@run_async
async def start(profile: bool, user_data_dir: Optional[str], headed: bool, port: int, width: int, height: int, mobile: bool):
    """
    Start Playwright's Chromium with remote debugging enabled.

    Use --port for parallel agents.
    Use --width and --height to set viewport size (default: 1920x1080 Full HD).
    Use --mobile for iPhone emulation (390x844, touch events, mobile UA).
    """
    chromium_path = ensure_initialized()

    if browser_module.is_port_in_use(port):
        console.print(f"[red]✗ Port {port} is already in use[/red]")
        console.print(f"\n[yellow]Options:[/yellow]")
        console.print(f"  1. Use different port: [cyan]sbx browser start --port {port + 1}[/cyan]")
        console.print(f"  2. Close existing: [cyan]sbx browser close --port {port}[/cyan]")
        sys.exit(1)

    # Determine profile directory
    if user_data_dir:
        profile_dir = Path(user_data_dir)
    elif profile:
        import shutil
        if sys.platform == "darwin":
            default_profile = Path.home() / "Library/Application Support/Google/Chrome"
        elif sys.platform == "win32":
            default_profile = Path.home() / "AppData/Local/Google/Chrome/User Data"
        else:
            default_profile = Path.home() / ".config/google-chrome"

        profile_dir = Path.home() / ".cache/playwright-browser-profile"
        profile_dir.mkdir(parents=True, exist_ok=True)
        if not (profile_dir / "Default").exists():
            console.print("Copying Chrome profile (first time only)...")
            shutil.copytree(default_profile, profile_dir, dirs_exist_ok=True)
    else:
        profile_dir = Path.home() / f".cache/playwright-browser-{port}"
        profile_dir.mkdir(parents=True, exist_ok=True)

    mode = "headed" if headed else "headless"
    device_mode = "mobile (iPhone)" if mobile else "desktop"
    viewport = f"{browser_module.MOBILE_VIEWPORT_WIDTH}x{browser_module.MOBILE_VIEWPORT_HEIGHT}" if mobile else f"{width}x{height}"

    console.print(f"Starting Playwright Chromium ({mode}, {device_mode}) on port {port}...")
    console.print(f"  [dim]Using: {chromium_path}[/dim]")
    console.print(f"  [dim]Viewport: {viewport}[/dim]")
    if mobile:
        console.print(f"  [dim]Touch events: enabled[/dim]")
        console.print(f"  [dim]User agent: iPhone/Safari[/dim]")

    browser_module.start_browser_process(chromium_path, port, headed, profile_dir, width, height, mobile)

    if await browser_module.wait_for_browser(port):
        profile_msg = " with your profile" if profile or user_data_dir else ""
        console.print(f"[green]✓ Playwright Chromium started on port {port} ({mode}){profile_msg}[/green]")
        console.print(f"[dim]Your Chrome browser is unaffected[/dim]")
    else:
        console.print(f"\n[red]✗ Failed to start browser on port {port}[/red]")
        console.print(f"\n[yellow]Troubleshooting:[/yellow]")
        console.print(f"  1. Verify init: [cyan]sbx browser init[/cyan]")
        console.print(f"  2. Try different port: [cyan]sbx browser start --port {port + 1}[/cyan]")
        sys.exit(1)


@browser.command()
@click.argument("url")
@click.option("--new", is_flag=True, help="Open in new tab")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def nav(url: str, new: bool, port: int):
    """Navigate to a URL."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            await browser_module.navigate(browser_conn, url, new_tab=new)
            action = "Opened" if new else "Navigated to"
            console.print(f"[green]✓ {action}: {url}[/green]")
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        console.print(f"\n  Run: [cyan]sbx browser start --port {port}[/cyan]")
        sys.exit(1)


@browser.command()
@click.argument("code")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def eval(code: str, port: int):
    """Execute JavaScript in the active page."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            result = await browser_module.evaluate_js(browser_conn, code)
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
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        console.print(f"\n  Run: [cyan]sbx browser start --port {port}[/cyan]")
        sys.exit(1)


@browser.command()
@click.option("--path", type=click.Path(), help="Save to specific path")
@click.option("--full", is_flag=True, help="Full page screenshot")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def screenshot(path: Optional[str], full: bool, port: int):
    """Take a screenshot of the active page."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            filepath = await browser_module.take_screenshot(browser_conn, path, full)
            console.print(f"[green]✓ Screenshot saved:[/green] {filepath}")
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        console.print(f"\n  Run: [cyan]sbx browser start --port {port}[/cyan]")
        sys.exit(1)


@browser.command(name="click")
@click.argument("selector")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def click_cmd(selector: str, port: int):
    """Click an element matching the selector."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            await browser_module.click_element(browser_conn, selector)
            console.print(f"[green]✓ Clicked:[/green] {selector}")
        except Exception as e:
            console.print(f"[red]✗ Failed to click '{selector}'[/red]")
            console.print(f"  Error: {e}")
            sys.exit(1)
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        sys.exit(1)


@browser.command(name="type")
@click.argument("selector")
@click.argument("text")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def type_cmd(selector: str, text: str, port: int):
    """Type text into an input field."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            await browser_module.type_text(browser_conn, selector, text)
            console.print(f"[green]✓ Typed into '{selector}':[/green] {text}")
        except Exception as e:
            console.print(f"[red]✗ Failed to type into '{selector}'[/red]")
            console.print(f"  Error: {e}")
            sys.exit(1)
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        sys.exit(1)


@browser.command(name="press")
@click.argument("key")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def press_cmd(key: str, port: int):
    """Press a keyboard key."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            await browser_module.press_key(browser_conn, key)
            console.print(f"[green]✓ Pressed:[/green] {key}")
        except Exception as e:
            console.print(f"[red]✗ Failed to press '{key}'[/red]")
            console.print(f"  Error: {e}")
            sys.exit(1)
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        sys.exit(1)


@browser.command()
@click.argument("direction", type=click.Choice(["up", "down", "top", "bottom"]))
@click.option("--amount", type=int, default=500, help="Amount to scroll (pixels)")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def scroll(direction: str, amount: int, port: int):
    """Scroll the page."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            await browser_module.scroll_page(browser_conn, direction, amount)
            console.print(f"[green]✓ Scrolled {direction}[/green]")
        except Exception as e:
            console.print(f"[red]✗ Failed to scroll[/red]")
            console.print(f"  Error: {e}")
            sys.exit(1)
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        sys.exit(1)


@browser.command()
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def cookies(port: int):
    """Get cookies from the active page as JSON."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            data = await browser_module.get_cookies(browser_conn)
            click.echo(json.dumps(data, indent=2))
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        sys.exit(1)


@browser.command()
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def a11y(port: int):
    """Get the accessibility tree snapshot."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            snapshot = await browser_module.get_accessibility_tree(browser_conn)
            click.echo(json.dumps(snapshot, indent=2))
        except Exception as e:
            console.print(f"[red]✗ Failed to get accessibility snapshot[/red]")
            console.print(f"  Error: {e}")
            sys.exit(1)
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        sys.exit(1)


@browser.command()
@click.option("--full", is_flag=True, help="Return full HTML instead of simplified")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def dom(full: bool, port: int):
    """Get the DOM structure."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            structure = await browser_module.get_dom(browser_conn, full)
            if isinstance(structure, str):
                click.echo(structure)
            else:
                click.echo(json.dumps(structure, indent=2))
        except Exception as e:
            console.print(f"[red]✗ Failed to get DOM[/red]")
            console.print(f"  Error: {e}")
            sys.exit(1)
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        sys.exit(1)


@browser.command()
@click.argument("message")
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def pick(message: str, port: int):
    """Interactive element picker - click elements to inspect them."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            result = await browser_module.pick_element(browser_conn, message)
            if result is None:
                console.print("[yellow]Cancelled[/yellow]")
                return
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
            await pw.stop()
    except browser_module.BrowserConnectionError as e:
        console.print(f"[red]✗ {e}[/red]")
        sys.exit(1)


@browser.command()
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def status(port: int):
    """Check if browser is running and accessible."""
    try:
        pw, browser_conn = await browser_module.connect(port)
        try:
            contexts = browser_conn.contexts
            if contexts:
                pages = contexts[0].pages
                console.print(f"[green]✓ Browser is running on port {port}[/green]")
                console.print(f"  Open tabs: {len(pages)}")
                if pages:
                    current_page = pages[-1]
                    console.print(f"  Current URL: {current_page.url}")
        finally:
            await browser_conn.close()
            await pw.stop()
    except browser_module.BrowserConnectionError:
        console.print(f"[red]✗ Browser not running on port {port}[/red]")
        console.print(f"  Run: [cyan]sbx browser start --port {port}[/cyan]")


@browser.command()
@click.option("--port", type=int, default=browser_module.DEFAULT_PORT, help="CDP port")
@run_async
async def close(port: int):
    """Close the browser and terminate the process."""
    try:
        # First try graceful disconnect
        pw, browser_conn = await browser_module.connect(port)
        await browser_conn.close()
        await pw.stop()
    except browser_module.BrowserConnectionError:
        pass

    # Kill the actual process
    if browser_module.kill_browser_on_port(port):
        console.print(f"[green]✓ Browser on port {port} closed[/green]")
    else:
        console.print(f"[green]✓ No browser running on port {port}[/green]")


if __name__ == "__main__":
    browser()
