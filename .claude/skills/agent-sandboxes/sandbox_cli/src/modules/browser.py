"""
Browser automation module.
Provides core functionality for Playwright Chromium browser control.
"""

import sys
import subprocess
import time
import tempfile
from pathlib import Path
from typing import Optional, Any, Tuple

# Playwright is loaded dynamically to avoid import errors if not installed
try:
    from playwright.async_api import async_playwright, Browser, Page

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = None  # type: ignore
    Page = None  # type: ignore

DEFAULT_PORT = 9222


def kill_browser_on_port(port: int) -> bool:
    """
    Kill the browser process listening on the specified port.
    Returns True if a process was killed, False otherwise.
    """
    import signal

    try:
        # Find PID using lsof
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    os_pid = int(pid)
                    import os
                    os.kill(os_pid, signal.SIGTERM)
                except (ValueError, ProcessLookupError):
                    pass
            return True
    except Exception:
        pass
    return False


# --- Exceptions ---


class BrowserNotInitializedError(Exception):
    """Raised when browser environment is not properly set up."""
    pass


class BrowserConnectionError(Exception):
    """Raised when browser connection fails."""
    pass


# --- Environment Checks ---


def check_playwright_installed() -> bool:
    """Check if Playwright Python package is installed."""
    return PLAYWRIGHT_AVAILABLE


def check_chromium_installed() -> Tuple[bool, str]:
    """
    Check if Playwright Chromium is installed.
    Returns (is_installed, path_or_cache_dir).
    """
    import platform
    import glob

    system = platform.system()
    home = Path.home()

    if system == "Darwin":
        cache_dir = home / "Library/Caches/ms-playwright"
        chromium_pattern = "chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium"
    elif system == "Windows":
        cache_dir = home / "AppData/Local/ms-playwright"
        chromium_pattern = "chromium-*/chrome-win/chrome.exe"
    else:
        cache_dir = home / ".cache/ms-playwright"
        chromium_pattern = "chromium-*/chrome-linux/chrome"

    chromium_paths = sorted(glob.glob(str(cache_dir / chromium_pattern)), reverse=True)

    if chromium_paths:
        return True, chromium_paths[0]
    return False, str(cache_dir)


def get_chromium_path() -> str:
    """Get Chromium executable path. Raises BrowserNotInitializedError if not found."""
    is_installed, path_or_dir = check_chromium_installed()
    if is_installed:
        return path_or_dir
    raise BrowserNotInitializedError(f"Chromium not found in {path_or_dir}")


def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("localhost", port)) == 0
    sock.close()
    return result


# --- Installation ---


def install_playwright() -> Tuple[bool, str]:
    """
    Install Playwright Python package.
    Returns (success, error_message).
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "playwright"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return False, result.stderr
        return True, ""
    except Exception as e:
        return False, str(e)


def install_chromium() -> Tuple[bool, str]:
    """
    Install Playwright Chromium.
    Returns (success, error_message).
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return False, result.stderr
        return True, ""
    except Exception as e:
        return False, str(e)


def verify_chromium(chromium_path: str) -> Tuple[bool, str]:
    """
    Verify Chromium installation by checking version.
    Returns (success, version_or_error).
    """
    try:
        result = subprocess.run(
            [chromium_path, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            return True, version
        return False, "Version check failed"
    except Exception as e:
        return False, str(e)


# --- Browser Connection ---


async def try_connect(port: int = DEFAULT_PORT) -> Browser:
    """
    Try to connect to running Playwright Chromium instance.
    Raises BrowserConnectionError on failure.
    """
    # Use 127.0.0.1 explicitly to avoid IPv6 issues
    browser_url = f"http://127.0.0.1:{port}"
    async with async_playwright() as pw:
        try:
            browser = await pw.chromium.connect_over_cdp(browser_url)
            return browser
        except Exception as e:
            raise BrowserConnectionError(f"Could not connect to port {port}: {e}")


async def connect(port: int = DEFAULT_PORT) -> Tuple[Any, Browser]:
    """
    Connect to running browser and return (playwright, browser) tuple.
    Raises BrowserConnectionError on failure.
    """
    browser_url = f"http://127.0.0.1:{port}"
    pw = await async_playwright().start()
    try:
        browser = await pw.chromium.connect_over_cdp(browser_url)
        return pw, browser
    except Exception as e:
        await pw.stop()
        raise BrowserConnectionError(f"Could not connect to port {port}: {e}")


async def get_active_page(browser: Browser) -> Page:
    """Get the most recently active page from browser."""
    contexts = browser.contexts
    if not contexts:
        raise RuntimeError("No browser contexts found")

    pages = contexts[0].pages
    if not pages:
        raise RuntimeError("No pages found")

    return pages[-1]


# --- Browser Lifecycle ---


DEFAULT_VIEWPORT_WIDTH = 1920
DEFAULT_VIEWPORT_HEIGHT = 1080

# iPhone 14/15 standard viewport
MOBILE_VIEWPORT_WIDTH = 390
MOBILE_VIEWPORT_HEIGHT = 844
MOBILE_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)


def start_browser_process(
    chromium_path: str,
    port: int,
    headed: bool = False,
    profile_dir: Optional[Path] = None,
    width: int = DEFAULT_VIEWPORT_WIDTH,
    height: int = DEFAULT_VIEWPORT_HEIGHT,
    mobile: bool = False,
) -> subprocess.Popen:
    """
    Start Chromium process with remote debugging.
    Returns the Popen process object.
    """
    if profile_dir is None:
        profile_dir = Path.home() / ".cache/playwright-browser-temp"
        profile_dir.mkdir(parents=True, exist_ok=True)

    # Override dimensions for mobile
    if mobile:
        width = MOBILE_VIEWPORT_WIDTH
        height = MOBILE_VIEWPORT_HEIGHT

    cmd = [
        chromium_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_dir}",
        f"--window-size={width},{height}",
        "--no-first-run",
        "--no-default-browser-check",
    ]

    # Mobile-specific settings
    if mobile:
        cmd.extend([
            f"--user-agent={MOBILE_USER_AGENT}",
            "--enable-touch-events",
            "--force-device-scale-factor=3",
        ])

    if not headed:
        cmd.extend([
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
        ])

    if sys.platform == "win32":
        process = subprocess.Popen(cmd, creationflags=subprocess.DETACHED_PROCESS)
    else:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

    return process


async def wait_for_browser(port: int, max_attempts: int = 30) -> bool:
    """
    Wait for browser to be ready on port.
    Returns True if connected, False if timeout.
    """
    # Initial delay to let browser process start
    time.sleep(1)

    for attempt in range(max_attempts):
        try:
            async with async_playwright() as pw:
                browser_url = f"http://127.0.0.1:{port}"
                browser = await pw.chromium.connect_over_cdp(browser_url)
                await browser.close()
                return True
        except Exception:
            if attempt == max_attempts - 1:
                return False
            time.sleep(0.5)

    return False


# --- Page Operations ---


async def navigate(browser: Browser, url: str, new_tab: bool = False) -> str:
    """
    Navigate to URL. Returns the final URL.
    """
    if new_tab:
        context = browser.contexts[0]
        page = await context.new_page()
    else:
        page = await get_active_page(browser)

    await page.goto(url, wait_until="domcontentloaded")
    return page.url


async def take_screenshot(
    browser: Browser,
    path: Optional[str] = None,
    full_page: bool = False,
) -> str:
    """
    Take screenshot. Returns the filepath.
    """
    page = await get_active_page(browser)

    if path:
        filepath = Path(path)
    else:
        filename = f"screenshot-{int(time.time())}.png"
        filepath = Path(tempfile.gettempdir()) / filename

    await page.screenshot(path=str(filepath), full_page=full_page)
    return str(filepath)


async def evaluate_js(browser: Browser, code: str) -> Any:
    """
    Execute JavaScript in the active page.
    Returns the result.
    """
    page = await get_active_page(browser)
    return await page.evaluate(f"(async () => {{ return ({code}); }})()")


async def click_element(browser: Browser, selector: str) -> None:
    """Click an element matching the selector."""
    page = await get_active_page(browser)
    await page.click(selector)


async def type_text(browser: Browser, selector: str, text: str) -> None:
    """Type text into an input field."""
    page = await get_active_page(browser)
    await page.fill(selector, text)


async def press_key(browser: Browser, key: str) -> None:
    """Press a keyboard key."""
    page = await get_active_page(browser)
    await page.keyboard.press(key)


async def scroll_page(browser: Browser, direction: str, amount: int = 500) -> None:
    """Scroll the page in specified direction."""
    page = await get_active_page(browser)
    if direction == "top":
        await page.evaluate("window.scrollTo(0, 0)")
    elif direction == "bottom":
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    elif direction == "up":
        await page.mouse.wheel(0, -amount)
    elif direction == "down":
        await page.mouse.wheel(0, amount)


async def get_cookies(browser: Browser) -> list:
    """Get all cookies from the browser context."""
    context = browser.contexts[0]
    return await context.cookies()


async def get_accessibility_tree(browser: Browser) -> dict:
    """Get the accessibility tree snapshot."""
    page = await get_active_page(browser)
    return await page.accessibility.snapshot()


async def get_dom(browser: Browser, full: bool = False) -> Any:
    """Get DOM structure. Returns full HTML if full=True, else simplified structure."""
    page = await get_active_page(browser)

    if full:
        return await page.content()

    # Simplified DOM extraction
    js = """
    () => {
        function isVisible(el) {
            if (!el) return false;
            const style = window.getComputedStyle(el);
            return style.display !== 'none' &&
                   style.visibility !== 'hidden' &&
                   style.opacity !== '0';
        }

        function clean(node) {
            if (node.nodeType === Node.TEXT_NODE) {
                const text = node.textContent.trim();
                return text ? text : null;
            }
            if (node.nodeType !== Node.ELEMENT_NODE) return null;

            const el = node;
            if (!isVisible(el)) return null;

            const tag = el.tagName.toLowerCase();
            if (['script', 'style', 'noscript', 'meta', 'link', 'svg', 'path'].includes(tag)) return null;

            const attrs = {};
            ['id', 'name', 'class', 'role', 'type', 'placeholder', 'aria-label', 'href', 'value'].forEach(attr => {
                if (el.hasAttribute(attr)) attrs[attr] = el.getAttribute(attr);
            });

            const children = [];
            el.childNodes.forEach(child => {
                const cleaned = clean(child);
                if (cleaned) {
                    if (typeof cleaned === 'string' && children.length > 0 && typeof children[children.length-1] === 'string') {
                        children[children.length-1] += ' ' + cleaned;
                    } else {
                        children.push(cleaned);
                    }
                }
            });

            if (Object.keys(attrs).length === 0 && children.length === 0) {
                if (!['p', 'div', 'span', 'h1','h2','h3','h4','h5','h6', 'li', 'td'].includes(tag)) return null;
            }

            return { tag, attrs, children };
        }

        return clean(document.body);
    }
    """
    return await page.evaluate(js)


# --- Element Picker JavaScript ---

PICKER_JS = """
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


async def pick_element(browser: Browser, message: str) -> Any:
    """
    Run interactive element picker.
    Returns element info dict, list of dicts, or None if cancelled.
    """
    page = await get_active_page(browser)
    return await page.evaluate(PICKER_JS, message)
