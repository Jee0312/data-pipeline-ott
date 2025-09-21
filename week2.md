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