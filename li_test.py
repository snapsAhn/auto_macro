from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

TARGET_DATE_TEXT = "06.15"

def main():
    # 크롬 드라이버 실행
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # 티켓링크 예매 페이지로 이동 (직접 URL 입력 또는 수동 이동)
    url = input("테스트할 예매 페이지 URL을 입력하세요: ")
    driver.get(url)
    input("페이지가 완전히 로드되고, 원하는 영역이 보이면 Enter를 누르세요...")

    # li 요소들 전체 탐색 및 날짜 span, 예매하기 버튼 정보 출력
    lis = driver.find_elements(By.TAG_NAME, "li")
    print(f"li 개수(전체): {len(lis)}")
    for idx, li in enumerate(lis, start=1):
        try:
            # 날짜 span 시도
            date_span = li.find_element(By.XPATH, "./div[1]/div[1]/span")
            date_text = date_span.text.strip()
        except Exception:
            date_text = "(날짜 span 없음)"
        try:
            reserve_btn = li.find_element(By.XPATH, "./div[3]/a")
            btn_text = reserve_btn.text.strip()
        except Exception:
            btn_text = "(예매하기 버튼 없음)"
        print(f"li[{idx}] 날짜: {date_text} / 버튼: {btn_text}")

        # 원하는 날짜가 있으면 안내
        if TARGET_DATE_TEXT in date_text:
            print(f"👉 li[{idx}]에서 '{TARGET_DATE_TEXT}'를 찾았습니다!")
    input("테스트가 끝났으면 Enter를 눌러 브라우저를 닫으세요.")
    driver.quit()

if __name__ == "__main__":
    main()