from faker import Faker         # 가짜 데이터 생성을 도와주는 라이브러리
import random                   # 랜덤 값 생성을 도와주는 라이브러리
import json                      # 로그를 JSON 형식으로 저장하기 위해 사용
import argparse                  # 터미널에서 날짜, 생성 건수 등을 입력받기 위함
from pathlib import Path          # 파일/폴더 경로 다룰 때 편리한 모듈
import datetime as dt             # 날짜/시간 처리

def main(date: str, n:int, out_dir:str):
    fake = Faker()                # Faker 객체 생성 (가짜 데이터 만들어줌)
    Faker.seed(42)                # 시드 고정 → 매번 실행해도 같은 랜덤 결과 (재현성)
    random.seed(42)

    # 가짜 데이터에 넣을 후보값들
    countries = ["KR","US","JP","TW","TH"]
    devices = ["ios","android","web","tv"]
    titles = [f"t_{i:05d}" for i in range(1, 101)]  # 콘텐츠 ID 100개 정도

    # 파일 경로 설정
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True) # 폴더 없으면 생성

    # 저장 파일 이름 예: watch_logs_2025-09-12.json
    fn = path / f"watch_logs_{date}.json"

    # 날짜를 datetime 객체로 변환
    d = dt.datetime.fromisoformat(date)

    with fn.open("w") as f:
        for _ in range(n):
            rec = {
                "user_id": f"u_{random.randint(1, 1000000)}", # 유저 ID
                "title_id": random.choice(titles), # 시청한 콘텐츠 ID
                "watch_time_sec": max(0, int(random.gauss(900, 300))), # 시청 시간 (초)
                "device": random.choice(devices), # 디바이스
                "country": random.choice(countries), # 국가
                "ts": (
                    d + dt.timedelta(seconds=random.randint(0, 86399)) # 하루 중 랜덤 시간
                ).isoformat(), # 시간 (ISO 형식)
                
            }
            f.write(json.dumps(rec) + "\n") # JSON 한 줄씩 기록
    print( f"✅ 로그 {n}건 생성 완료 -> {fn}")

if __name__=="__main__":
    # 터미널에서 실행 시 받을 인자 정의
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="생성할 날짜 (예: 2025-09-12)")
    ap.add_argument("--n", type=int, default=1000, help="생성할 로그 건수")
    ap.add_argument("--out", default="data/raw", help="저장 폴더 경로")
    args = ap.parse_args()

    main(args.date, args.n, args.out)