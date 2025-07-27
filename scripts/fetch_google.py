from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def fetch_google_trends():
    """
    Seleniumとwebdriver-managerを使ってGoogleトレンドの24時間集計ページをスクレイピングする
    """
    url = "https://trends.google.co.jp/trending?geo=JP&hours=24"
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = None
    try:
        # webdriver-managerが適切なChromeDriverを自動でダウンロード・セットアップする
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)
        
        # CSSセレクタの要素が表示されるまで待機（最大20秒）
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody:last-of-type > tr > td')))
        
        # トレンドワードを取得
        trend_elements = driver.find_elements(By.CSS_SELECTOR, 'tbody:last-of-type > tr > td:nth-of-type(2)')
        trends = [elem.text for elem in trend_elements if elem.text]
        
        return trends

    except Exception as e:
        print(f"An error occurred during scraping with Selenium: {e}")
        return []
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    trends = fetch_google_trends()
    if trends:
        print("Google Trends (Last 24 hours via Selenium):")
        for i, trend in enumerate(trends, 1):
            print(f"{i}. {trend}")
    else:
        print("Failed to fetch Google Trends with Selenium.")