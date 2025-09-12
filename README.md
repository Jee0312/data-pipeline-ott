# data-pipeline-ott
가상의 Netflix·왓챠 같은 시청 로그 데이터를 처리하고, 유저별 시청 통계/추천용 피처를 생성하는 파이프라인 구축


## 🎯 프로젝트 목표

* **Hadoop/클라우드 기반 대용량 데이터 처리 경험**
* **데이터 품질 관리 & 파이프라인 운영 경험**
* **Airflow 트러블슈팅 및 DAG 운영 경험**
* **SQL & Python 실무 코드 작성 경험**

---

## 🛠 추천 토이 프로젝트:

### **“OTT/영화 로그 데이터 파이프라인 구축 & 품질 모니터링”**

#### 📌 시나리오

“영화 OTT 서비스가 있다고 가정하고,
사용자 시청 로그(수백만 건 가상 데이터)를 **수집 → 적재 → 가공 → 품질 검증 → 분석 → 대시보드**까지 이어지는 파이프라인을 만든다.”

---

## 📅 6주 로드맵

### **1주차: 데이터 수집 & 환경 세팅**

* AWS/GCP 중 하나 선택 (또는 로컬 Hadoop/Spark 환경 docker로도 OK)
* 가상 로그 데이터 생성 (Python faker 라이브러리, Spark 데이터프레임)

* 예: `user_id`, `title_id`, `watch_time`, `device`, `country`, `timestamp`
* 저장소: S3 or HDFS

### **2주차: 데이터 적재 & 기본 분석**

* Raw 데이터를 S3/HDFS → Hive 테이블 or BigQuery 테이블로 적재
* 기본 SQL 쿼리 작성:

* “일자별 시청 유저 수”, “Top N 인기 콘텐츠”, “Retention 계산”

### **3주차: ETL 파이프라인 구축**

* Spark SQL / PySpark로 ETL 작성

* 예: raw → clean (null 제거, type casting)
* clean → agg (일자별/국가별/디바이스별 통계)
* 결과를 parquet 형식으로 저장 → downstream에서 활용

### **4주차: Airflow DAG 작성**

* DAG 구조:

1. 데이터 ingest (raw → staging)
2. 데이터 transform (staging → clean)
3. 데이터 quality check (row count, null 비율, schema check)
4. 결과 적재 후 Slack 알림

* Airflow에서 스케줄링 & retry, SLA 세팅

### **5주차: 데이터 품질 관리**

* dbt test 또는 Great Expectations 활용

* 예: `row_count > 0`, `country in [KR, US, JP]`
* Airflow 태스크 실패 시 Slack/이메일 알림 연동
* 데이터 품질 리포트 자동 생성

### **6주차: 분석 & 대시보드**

* SQL 최적화 경험 → 윈도우 함수, CTE 활용
* Streamlit/Metabase/Redash로 간단한 대시보드 제작

* “국가별 DAU 추이”
* “Top 10 콘텐츠”
* “신규 vs 복귀 유저 비율”
* 프로젝트 문서화 (README + 아키텍처 다이어그램)

---

## 🚀 얻을 수 있는 경험

* **Hadoop/클라우드 경험**: Spark + S3/HDFS + Hive/BigQuery
* **CS 지식 적용**: 대용량 데이터 처리 시 join 최적화, partition 설계
* **품질 관리 경험**: Airflow + Great Expectations/dbt tests
* **SQL 상급 연습**: 집계, 윈도우 함수, 최적화
* **Python 중급 연습**: PySpark, API ingestion 스크립트
* **Airflow 운영 경험**: DAG 설계, SLA 설정, 알림 연동, 트러블슈팅