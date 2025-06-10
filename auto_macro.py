import datetime
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# # --- 1. 예매 오픈 시간 설정 ---
# TARGET_YEAR = 2025
# TARGET_MONTH = 6
# TARGET_DAY = 9   # 예매 오픈 날짜
# TARGET_HOUR = 15    # 예매 오픈 시간 (24시간 기준, 오후 2시는 14)
# TARGET_MINUTE = 49   # 예매 오픈 분

# # --- 2. 예매할 티켓 정보 설정 ---
# # 예매 페이지에서 보이는 날짜와 요일 텍스트를 정확하게 입력해야 합니다.
# TARGET_DATE_TEXT = "06.15"  # 예매할 경기의 날짜 (예: "06.12")
# TARGET_DAY_TEXT = "일"      # 예매할 경기의 요일 (예: "목")

def get_ticketlink_server_time():
    """
    티켓링크 서버에 HEAD 요청을 보내고, 응답 헤더의 Date 값을 KST로 변환하여 반환합니다.
    """
    url = "https://www.ticketlink.co.kr/"
    resp = requests.head(url)
    date_str = resp.headers.get("Date")
    if date_str:
        from email.utils import parsedate_to_datetime
        dt_utc = parsedate_to_datetime(date_str)
        # KST 변환 후 tzinfo 제거
        kst = (dt_utc + datetime.timedelta(hours=9)).replace(tzinfo=None)
        return kst
    raise Exception("서버 시간 조회 실패")

def run_macro(open_date, open_time, game_date_text):
    global TARGET_YEAR, TARGET_MONTH, TARGET_DAY, TARGET_HOUR, TARGET_MINUTE, TARGET_DATE_TEXT

    # 예매 오픈 날짜/시간 파싱
    try:
        year, month, day = map(int, open_date.split('-'))
        hour, minute = map(int, open_time.split(':'))
    except Exception as e:
        return f"예매 오픈 날짜/시간 파싱 오류: {e}"

    # 전역 변수에 동적으로 할당
    TARGET_YEAR = year
    TARGET_MONTH = month
    TARGET_DAY = day
    TARGET_HOUR = hour
    TARGET_MINUTE = minute
    TARGET_DATE_TEXT = game_date_text

    # print(f"[DEBUG] run_macro에서 받은 값: {open_date} {open_time} (경기날짜: {game_date_text})")
    # print(f"[DEBUG] 전역 변수 설정: {TARGET_YEAR}-{TARGET_MONTH}-{TARGET_DAY} {TARGET_HOUR}:{TARGET_MINUTE}")

    main()
    return f"{open_date} {open_time} (경기날짜: {game_date_text}) 예매 시도 완료"

def main():
    """
    티켓팅 매크로 메인 함수
    """
    try:
        print("ChromeDriver를 설정합니다...")
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("ChromeDriver 설정 완료.")

        # 사이트 자동 이동
        driver.get("https://www.ticketlink.co.kr/sports/137/57")
        print("티켓링크 사이트로 자동 이동했습니다.")

        # --- 사용자 준비 단계 안내 및 대기 제거 ---
        # React에서 안내 및 대기 처리
        # 기존 print/input 부분 삭제

        # --- (0) 특정 시간까지 대기 ---
        target_open_time = datetime.datetime(TARGET_YEAR, TARGET_MONTH, TARGET_DAY, TARGET_HOUR, TARGET_MINUTE)
        print(f"[DEBUG] main에서 target_open_time: {target_open_time}")
        now = get_ticketlink_server_time()
        print(f"[DEBUG] main에서 now: {now}")
        
        if now >= target_open_time:
            raise Exception("예매 오픈 날짜/시간이 이미 지났습니다.")
        print(f"✅ 예매 오픈 시간({target_open_time.strftime('%Y-%m-%d %H:%M:%S')})까지 티켓링크 서버 기준으로 대기합니다...")

        # 최초 1회만 서버 시간과 내 시간의 차이(오프셋)를 구함
        server_now = get_ticketlink_server_time()
        local_now = datetime.datetime.now()
        offset = server_now - local_now

        # 이후에는 내 시간 + offset으로 서버 시간 추정
        while True:
            now = datetime.datetime.now() + offset
            if now >= target_open_time:
                break
            remain = (target_open_time - now).total_seconds()
            print(f"⏳ 남은 시간: {int(remain)}초", end='\r')
            time.sleep(0.2)

        print("\n✅ 예매 오픈 시간이 되었습니다! 매크로를 시작합니다.")

        # --- (1) 페이지 새로고침 ---
        print("페이지를 새로고침합니다...")
        driver.refresh()

        # --- (1-1) 예매 리스트 탭 클릭 (필요시) ---

        try:
            # '예매하기' 탭이 있다면 클릭 (id, 텍스트 등 실제 구조에 맞게 수정)
            tab_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//h4[contains(text(), '예매하기')]"))
            )
            tab_btn.click()
            print("✅ '예매하기' 탭을 클릭했습니다.")
        except Exception as e:
            print("ℹ️ '예매하기' 탭 클릭을 건너뜁니다. (이미 활성화되어 있을 수 있음)")

        # --- (1-2) 예매 리스트 로딩 대기 ---
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".reserve_lst_bx ul > li"))
            )
            print("✅ 예매 리스트가 로딩되었습니다.")
        except Exception as e:
            print("❌ 예매 리스트 로딩 대기 중 오류:", e)

        # --- (2) 목표 날짜의 '예매하기' 버튼 클릭 ---
        try:
            print(f"'{TARGET_DATE_TEXT}'가 포함된 li를 정확한 영역에서 루프 돌며 찾고, 같은 li의 '예매하기' 버튼을 누릅니다.")
            lis = driver.find_elements(By.CSS_SELECTOR, ".reserve_lst_bx ul > li")
            print(f"[디버그] 예매 리스트 li 개수: {len(lis)}")
            found = False
            for idx, li in enumerate(lis, start=1):
                try:
                    date_span = li.find_element(By.CSS_SELECTOR, "div.match_day > div.date > span")
                    date_text = date_span.text.strip()
                    # print(f"[디버그] li[{idx}]의 날짜 span: '{date_text}'")
                except Exception as e:
                    print(f"[디버그] li[{idx}]에서 날짜 span을 찾는 중 오류: {e}")
                    continue
                if TARGET_DATE_TEXT in date_text:
                    print(f"✅ '{TARGET_DATE_TEXT}'를 찾았습니다.")
                    try:
                        match_btn = li.find_element(By.CSS_SELECTOR, "div.match_btn > a")
                        # print(f"[디버그] li[{idx}]의 '예매하기' 버튼 텍스트: '{match_btn.text.strip()}'")
                        match_btn.click()
                        print(f"✅ '{TARGET_DATE_TEXT}'의 '예매하기' 버튼을 클릭했습니다.")
                        found = True
                        break
                    except Exception as btn_e:
                        print(f"[디버그] li[{idx}]에서 '예매하기' 버튼을 찾는 중 오류: {btn_e}")
            if not found:
                raise Exception("해당 날짜의 '예매하기' 버튼을 찾을 수 없습니다.")
        except Exception as e:
            print(f"❌ '예매하기' 버튼을 찾거나 클릭하는 중 오류 발생: {e}")
            driver.save_screenshot("error_screenshot_button_click.png")
            return

        
        # --- (3) 대기열 처리 ---
        print("대기열 발생 여부를 확인합니다...")
        time.sleep(1) # 페이지 전환을 위한 최소한의 대기

        try:
            wait_timeout = 300 # 최대 대기 시간 (초), 예: 5분
            wait_start_time = time.time()

            # 대기열 페이지에만 나타나는 특징적인 요소나 URL 키워드로 대기열 여부를 판단합니다.
            # 예시: URL에 'wait', 'queue'가 포함되거나, 페이지에 '대기' 관련 문구가 있는 경우
            while "wait" in driver.current_url.lower() or "queue" in driver.current_url.lower() or driver.find_elements(By.XPATH, "//*[contains(text(), '대기 중') or contains(text(), '잠시만 기다려주세요')]"):
                if time.time() - wait_start_time > wait_timeout:
                    print("❌ 대기열 최대 대기 시간을 초과했습니다.")
                    return
                print(f"대기열 대기 중... (경과 시간: {int(time.time() - wait_start_time)}초)")
                time.sleep(5) # 5초마다 상태를 다시 확인
            
            print("✅ 대기열을 통과했거나, 대기열이 발생하지 않았습니다.")
            
            # 이후 단계(보안문자 입력, 좌석 선택 등)는 여기에 이어서 구현하면 됩니다.
            print("\n🎉 1~3단계(새로고침, 버튼 클릭, 대기열 처리)가 성공적으로 완료되었습니다!")
            print("이제부터 수동으로 진행하시거나, 다음 단계 코드를 추가해주세요.")

        except Exception as e:
            print(f"❌ 대기열 처리 중 오류 발생: {e}")
            driver.save_screenshot("error_screenshot_queue.png")

    except Exception as e:
        print(f"❌ 매크로 실행 중 예기치 않은 오류가 발생했습니다: {e}")
    
    finally:
        print("="*60)
        input("매크로 작동이 완료되었습니다. Enter를 누르면 브라우저를 닫고 종료합니다.")
        # driver.quit() # 주석을 풀면 Enter 입력 시 브라우저가 자동으로 닫힙니다.


if __name__ == "__main__":
    main()