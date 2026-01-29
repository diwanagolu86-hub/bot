import time
import random
from playwright.sync_api import sync_playwright

# --- CONFIG ---
TARGET_URL = "https://nanolinks.in/WBxwh"
FINAL_DESTINATION = "bot.free.nf"
REFERRERS = ["https://t.me/", "https://google.com/"]

def safe_js_click(page, text_target):
    try:
        found = page.evaluate(f"""
            () => {{
                const elements = Array.from(document.querySelectorAll('a, button, div, span, input'));
                const target = elements.find(el => el.innerText.trim().toUpperCase() === "{text_target}".toUpperCase());
                if (target) {{
                    target.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                    target.click();
                    return true;
                }}
                return false;
            }}
        """)
        return found
    except: return False

def run_bot():
    print("🚀 Starting Bot on GitHub Cloud Server...")
    
    with sync_playwright() as p:
        try:
            # Proxy hata diya, ab direct GitHub ka fast internet use hoga
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--ignore-certificate-errors"]
            )
            
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                extra_http_headers={"Referer": random.choice(REFERRERS)}
            )
            page = context.new_page()

            # --- 1. IP CHECK (Proof ke liye) ---
            try:
                page.goto("http://httpbin.org/ip", timeout=15000)
                print(f"🔥 Current Cloud IP: {page.content()}")
            except: pass

            # --- 2. OPEN TARGET ---
            print(f"🌍 Opening URL: {TARGET_URL}")
            page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
            print("✅ Page Loaded. Waiting 15s...")
            time.sleep(15)

            # --- 3. BYPASS LOGIC ---
            # Step 1
            if safe_js_click(page, "CONTINUE"):
                print("✅ Step 1: Continue clicked.")
                time.sleep(10)

            # Step 2
            page.mouse.wheel(0, 1000)
            time.sleep(2)
            if safe_js_click(page, "CLICK HERE TO PROCEED") or safe_js_click(page, "PROCEED"):
                print("✅ Step 2: Proceed clicked.")
            
            # Step 3: Timer
            print("⏳ Waiting for Timer (30s)...")
            time.sleep(30)

            # Step 4: Final Click
            page.mouse.wheel(0, 500)
            if safe_js_click(page, "GET LINK"):
                print("✅ Step 3: Get Link clicked.")
                time.sleep(5)
                
                # Check Final URL
                curr = page.url
                if FINAL_DESTINATION in curr:
                    print(f"\n🎉 SUCCESS! Reached: {curr}\n")
                else:
                    print(f"⚠️ Reached somewhere else: {curr}")
            else:
                print("❌ Get Link button not found.")

            browser.close()

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_bot()
