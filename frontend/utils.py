"""
🌿 ZenFeed — API utility helpers
Handles Render free-tier cold starts gracefully.
"""

import requests
import streamlit as st

# How long to wait after the first fast attempt fails (cold start window)
_COLD_START_TIMEOUT = 70   # Render free tier can take up to ~60s to wake


def api_get(url: str, wake_msg: str = "Waking up the server — first visit takes ~30 s…", **kwargs):
    """
    GET with cold-start awareness.
    1. Quick attempt (5 s) — returns immediately if server is warm.
    2. On timeout/connection error: shows a spinner and retries with a 70 s timeout.
    Raises the underlying exception if the second attempt also fails.
    """
    try:
        return requests.get(url, timeout=5, **kwargs)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        pass  # server is cold — fall through to the warm-up attempt

    with st.spinner(f"🌿 {wake_msg}"):
        return requests.get(url, timeout=_COLD_START_TIMEOUT, **kwargs)


def api_post(url: str, wake_msg: str = "Waking up the server — first visit takes ~30 s…", **kwargs):
    """
    POST with cold-start awareness.
    1. Quick attempt (10 s) — returns immediately if server is warm.
    2. On timeout/connection error: shows a spinner and retries with a 70 s timeout.
    Raises the underlying exception if the second attempt also fails.
    """
    try:
        return requests.post(url, timeout=10, **kwargs)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        pass

    with st.spinner(f"🌿 {wake_msg}"):
        return requests.post(url, timeout=_COLD_START_TIMEOUT, **kwargs)
