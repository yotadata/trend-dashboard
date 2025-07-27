from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def fetch_google_trends():
    """
    Seleniumを使ってGoogleトレンドの24時間集計ページをスクレイピングする
    """
    url = "https://trends.google.co.jp/trending?geo=JP&hours=24"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ヘッドレスモードで実行
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") # ウィンドウサイズ指定
    
    # プロジェクトルートからの相対パスでWebDriverを指定
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    driver_path = os.path.join(project_root, 'drivers', 'chromedriver')
    
    driver = None
    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)
        
        # ページが完全に読み込まれるまで待機（最大20秒）
        # 'div.search-card-title > span' というセレクタの要素が表示されるまで待つ
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.search-card-title > span')))
        
        # トレンドワードを取得
        trend_elements = driver.find_elements(By.CSS_SELECTOR, 'div.search-card-title > span')
        trends = [elem.text for elem in trend_elements if elem.text]
        
        return trends[:10]

    except Exception as e:
        print(f"An error occurred during scraping with Selenium: {e}")
        return []
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    # ローカルでテスト実行する場合、ChromeDriverのインストールとPATH設定が必要です
    # https://chromedriver.chromium.org/downloads
    trends = fetch_google_trends()
    if trends:
        print("Google Trends (Last 24 hours via Selenium):")
        for i, trend in enumerate(trends, 1):
            print(f"{i}. {trend}")
    else:
        print("Failed to fetch Google Trends with Selenium.")
