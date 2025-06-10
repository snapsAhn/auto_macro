import requests
import re
import datetime

def get_navyism_time():
    url = "https://time.navyism.com/?host=www.ticketlink.co.kr"
    resp = requests.get(url)
    # "2025년 06월 09일 15시 12분 55초" 형태 추출
    match = re.search(r'(\d{4})년\s*(\d{2})월\s*(\d{2})일\s*(\d{2})시\s*(\d{2})분\s*(\d{2})초', resp.text)
    if match:
        year, month, day, hour, minute, second = map(int, match.groups())
        return datetime.datetime(year, month, day, hour, minute, second)
    else:
        raise Exception("서버시간을 찾을 수 없습니다.")

if __name__ == "__main__":
    try:
        now = get_navyism_time()
        print(f"네이비즘에서 불러온 티켓링크 서버 시간: {now}")
    except Exception as e:
        print(f"시간 불러오기 실패: {e}")