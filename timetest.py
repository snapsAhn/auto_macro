import requests
import datetime
from email.utils import parsedate_to_datetime

def get_ticketlink_server_time():
    url = "https://www.ticketlink.co.kr/"
    resp = requests.head(url)
    date_str = resp.headers.get("Date")
    if date_str:
        # Date 헤더는 항상 GMT(UTC) 기준입니다.
        dt_utc = parsedate_to_datetime(date_str)
        # 한국 시간(KST)으로 변환
        dt_kst = dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
        return dt_kst.replace(tzinfo=None)  # tzinfo 제거(기존 코드와 호환)
    else:
        raise Exception("서버시간(Date 헤더)을 찾을 수 없습니다.")

# 사용 예시
print(get_ticketlink_server_time())