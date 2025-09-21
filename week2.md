## 🚀 Airflow 연동 작업 (오늘 한 부분)

1. **Airflow DAG 작성 (`infra/airflow/dags/pipeline_local.py`)**
   - 태스크 순서:
     1. `generate_raw` → 하루치 raw 로그 생성
     2. `spark_clean` → JSON → Clean parquet 변환
     3. `data_quality_check` → 간단 DQ (row count > 0 확인)
     4. `spark_agg` → 일자/국가/디바이스별 집계
   - Airflow UI에서 DAG 실행하면 전체 파이프라인 자동 실행됨.

2. **상대경로 문제 해결**
   - Airflow 실행 시 working dir이 달라져서 `PATH_NOT_FOUND` 발생
   - 해결 방법:
     - Spark job(`spark_clean.py`, `spark_agg.py`)에서 `project.root` conf를 받아 절대경로 사용
     - DAG의 `bash_command`에 `--conf project.root={{ var.value.PROJECT_ROOT }}` 전달
     - Airflow Variable에 `PROJECT_ROOT=/Users/.../data-pipeline-ott` 저장

3. **수동 리허설 → DAG 실행 검증**
   - 수동으로 `spark-submit` 실행 시 정상 작동 확인
   - DAG에서도 절대경로 전달 후 실행 가능하도록 수정
   - 현재는 `generate_raw → spark_clean → dq → agg` 순서까지 실행 확인 완료 (단, UTC/KST 차이에 따른 날짜 주의 필요)

---

## ✅ 성과
- 로컬 PySpark 파이프라인을 Airflow DAG으로 연결 성공  
- DAG에서 실행 시 발생한 경로 문제를 절대경로/Variable 방식으로 해결  
- 간단한 데이터 품질 체크(DQ) 태스크까지 포함한 end-to-end 파이프라인 구축  

---

## 🔮 다음 단계 (Week 3 예정)
- Great Expectations로 데이터 품질 체크 고도화  
- Slack 알림 연동 (태스크 실패 시 알림)  
- Streamlit 대시보드 초안 만들기 (DAU/국가/디바이스 breakdown)




## 일부 작업 코드

### 4) Airflow 웹서버 & 스케줄러 실행

터미널 2개를 열어서 각각 아래처럼 실행합니다.
(두 터미널 모두 가상환경 .venv가 켜져 있어야 spark-submit을 찾습니다!)

```
터미널 A:

source .venv/bin/activate
export AIRFLOW_HOME="$(pwd)/infra/airflow"
airflow webserver --port 8080


터미널 B:

source .venv/bin/activate
export AIRFLOW_HOME="$(pwd)/infra/airflow"
airflow scheduler
```


### 5) DAG 실행

브라우저 열고: http://localhost:8080
로그인: admin / admin
DAGs 목록에서 local_data_pipeline 토글 On
오른쪽 Play ▶️ (Trigger DAG) 클릭
그래프 뷰에서 generate_raw → spark_clean → data_quality_check → spark_agg 순서로 실행되는지 확인


### 6) 결과 확인

파일들이 잘 생겼는지 체크

```
ls -lah data/raw | head
ls -lah data/clean/date=2025-09-12
ls -lah data/agg/date=2025-09-12
```

빠르게 내용 보기 (PySpark 인터랙티브)
```
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
spark.read.parquet("data/agg/date=2025-09-12").show(truncate=False)
```