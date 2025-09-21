
---

# 📌 진행한 작업

1. **가짜 로그 생성기 (`jobs/generate_fake_logs.py`)**
   - Faker + random으로 OTT 시청 로그 샘플 생성
   - JSON Lines 형식으로 `data/raw/`에 저장
   - 실행 예시:
     ```bash
     python jobs/generate_fake_logs.py --date 2025-09-12 --n 1000 --out data/raw
     ```

2. **Clean Job (`jobs/spark_clean.py`)**
   - Raw JSON → Parquet 변환
   - 정제 로직:
     - 음수/NULL `watch_time_sec` → 0
     - 허용되지 않은 국가/기기 값 → `"UNKNOWN"`, `"other"`
     - `event_date` 컬럼 추가
   - 결과: `data/clean/date=YYYY-MM-DD/` 폴더 생성

3. **Agg Job (`jobs/spark_agg.py`)**
   - Clean Parquet → 일자/국가/디바이스별 집계
   - 계산 지표:
     - `dau`: 일별 unique user 수
     - `total_watch_sec`: 총 시청 시간
     - `events`: 이벤트 수
   - 결과: `data/agg/date=YYYY-MM-DD/` 폴더 생성




---

# [base]
 - GitHub repo 생성 → clone → (로컬에서) 가상환경 만들고 라이브러리 설치 → requirements.txt & .gitignore → 폴더 구조 생성 → 첫 커밋/푸시



## 🔧 Step 2. Python 가상환경 만들기


```bash
python3 -m venv .venv #내 방에만 있는 작은 주방
source .venv/bin/activate #내 방 주방 불 켜기
```

👉 커맨드 실행 후 프롬프트 앞에 `(.venv)` 뜨면 가상환경이 켜진 상태예요.

---

## 🔧 Step 3. 기본 패키지 설치

```bash
pip install pyspark==3.5.1 pandas pyarrow boto3 faker requests # ETL
pip install "apache-airflow==2.9.*" apache-airflow-providers-slack #스케줄링
pip install great-expectations==0.18.16 #데이터품질
```

---

## requirements.txt 만들기 (버전 고정/재현성)

```bash
pip freeze > requirements.txt #현재 활성화된 가상환경(.venv)에 설치된 모든 패키지와 그 버전을 표준출력으로 > 오버라이트
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```
- 다음에 `pip install -r requirements.txt` 로 현재 환경과 완전히 똑같이 깔림 

## 🔧 Step 4. 폴더 구조 만들기

터미널에서:

```bash
mkdir -p infra/airflow/dags jobs dq sql dashboard
touch infra/airflow/dags/__init__.py
```

---

## 🔧 Step 5. 첫 커밋

```bash
git add .
git commit -m "Initial project setup: env, folder structure"
git push origin main
```




