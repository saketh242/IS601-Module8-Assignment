import pytest
from playwright.sync_api import sync_playwright
import subprocess
import time
import os
import requests

def wait_for_server(url, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except Exception:
            time.sleep(0.5)
    return False

def test_hello_world():
    process = subprocess.Popen(['python', '-m', 'uvicorn', 'main:app', '--port', '8000'])
    try:
        assert wait_for_server('http://localhost:8000'), 'Server did not start in time!'
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('http://localhost:8000')
            assert page.inner_text('h1') == 'Hello World'
            browser.close()
    finally:
        process.terminate()
        process.wait()

def test_calculator_add():
    process = subprocess.Popen(['python', '-m', 'uvicorn', 'main:app', '--port', '8000'])
    try:
        assert wait_for_server('http://localhost:8000'), 'Server did not start in time!'
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('http://localhost:8000')
            page.fill('#a', '10')
            page.fill('#b', '5')
            page.click('button:text("Add")')
            assert page.inner_text('#result') == 'Calculation Result: 15'
            browser.close()
    finally:
        process.terminate()
        process.wait()

def test_calculator_divide_by_zero():
    process = subprocess.Popen(['python', '-m', 'uvicorn', 'main:app', '--port', '8000'])
    try:
        assert wait_for_server('http://localhost:8000'), 'Server did not start in time!'
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('http://localhost:8000')
            page.fill('#a', '10')
            page.fill('#b', '0')
            page.click('button:text("Divide")')
            assert page.inner_text('#result') == 'Error: Cannot divide by zero💀'
            browser.close()
    finally:
        process.terminate()
        process.wait()
