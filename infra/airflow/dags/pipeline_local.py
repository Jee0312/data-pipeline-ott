# infra/airflow/dags/pipeline_local.py


from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime, timedelta

# Airflow Variable에서 프로젝트 루트 절대경로 읽기
PROJECT_ROOT = Variable.get("PROJECT_ROOT")

# DAG 공통 설정
DEFAULT_ARGS = {
    "owner": "you",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="local_data_pipeline",
    default_args=DEFAULT_ARGS,
    description="Raw → Clean → DQ → Agg (local files)",
    schedule_interval="@daily",           # 매일 1회 실행
    start_date=datetime(2025, 9, 1),      # 시작 날짜
    catchup=False,                        # 과거 날짜 몰아 실행 안 함
    tags=["local", "pipeline"],
) as dag:

    # 1) Raw 데이터 생성
    # gen_raw = BashOperator( 
    #     task_id="generate_raw",
    #     bash_command=(
    #         "python /opt/airflow/jobs/generate_fake_logs.py " #Python 스크립트(generate_fake_logs.py) 실행
    #         "--date {{ ds }} --n 1000 --out /opt/airflow/data/raw" # 날짜는 {{ ds }} (Airflow가 DAG 실행일자 자동 전달) 생성할 로그 건수는 1000건, 저장 폴더는 /opt/airflow/data/raw
    #     ),
    # )

    gen_raw = BashOperator(
        task_id="generate_raw",
        bash_command=(
            f"python {PROJECT_ROOT}/jobs/generate_fake_logs.py "
            "--date {{ ds }} --n 1000 "
            f"--out {PROJECT_ROOT}/data/raw"
        ),
    )



    # 2) Clean 변환
    # clean = BashOperator(
    #     task_id="spark_clean", #spark-submit으로 Spark 잡(spark_clean.py) 실행
    #     bash_command=(
    #         "spark-submit --conf spark.run.date={{ ds }} " #날짜는 {{ ds }} (Airflow가 DAG 실행일자 자동 전달)
    #         "/opt/airflow/jobs/spark_clean.py"
    #     ),
    # )
    clean = BashOperator(
        task_id="spark_clean",
        bash_command=(
            "spark-submit --conf spark.run.date={{ ds }} "
            f"{PROJECT_ROOT}/jobs/spark_clean.py"
        ),
    )


    # 3) 간단 DQ 체크 (row count > 0 확인)
    # dq = BashOperator(
    #     task_id="data_quality_check", # 최소한의 품질 확인용
    #     bash_command=(
    #         "python -c \"import sys, pyarrow.parquet as pq;" #PyArrow로 parquet 읽고, row 수 확인
    #         "import glob;"
    #         "files=glob.glob('/opt/airflow/data/clean/date={{ ds }}/*.parquet');"
    #         "table=pq.read_table(files[0]);"
    #         "rows=table.num_rows;"
    #         "print(f'Row count: {rows}');"
    #         "sys.exit(0 if rows > 0 else 1)\"" #> 0이면 성공(코드 0), 아니면 실패(코드 1) 
    #     ),
    # )
    dq = BashOperator(
        task_id="data_quality_check",
        bash_command=(
            "python -c \"import sys,glob,pyarrow.parquet as pq;"
            f"files=glob.glob('{PROJECT_ROOT}/data/clean/date={{" + " ds " + "}}/*.parquet');"
            "import os;"
            "print('CLEAN files:', files);"
            "table=pq.read_table(files[0]) if files else None;"
            "rows=(table.num_rows if table else 0);"
            "print(f'Row count: {rows}');"
            "sys.exit(0 if rows>0 else 1)\""
        ),
    )

    # 4) Agg 집계
    # agg = BashOperator(
    #     task_id="spark_agg", #spark-submit으로 Spark 잡(spark_agg.py) 실행
    #     bash_command=(
    #         "spark-submit --conf spark.run.date={{ ds }} " #날짜는 {{ ds }} (Airflow가 DAG 실행일자 자동 전달)
    #         "/opt/airflow/jobs/spark_agg.py"
    #     ),
    # )
    agg = BashOperator(
        task_id="spark_agg",
        bash_command=(
            "spark-submit --conf spark.run.date={{ ds }} "
            f"{PROJECT_ROOT}/jobs/spark_agg.py"
        ),
    )
    
    # 실행 순서 지정
    gen_raw >> clean >> dq >> agg
