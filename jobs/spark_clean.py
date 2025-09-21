from pyspark.sql import SparkSession, functions as F
from airflow.models import Variable
PROJECT_ROOT = Variable.get("PROJECT_ROOT")  # 절대경로 저장해둔 변수


# SparkSession: Spark 작업의 시작점
spark = (SparkSession.builder
         .appName("clean_logs") #Spark UI에서 job이름으로 보일 이름
         .getOrCreate())

# Aifrflow에서 --conf spark.run.date=2025-09-12 로 전달 한다고 가정 / 실행 시, 전달한 날짜 파라미터를 가져오는 코드
date = spark.sparkContext.getConf().get("spark.run.date", "2025-09-12")
project_root = spark.sparkContext.getConf().get("project.root", ".")  # << 추가/확인

# 입력 경로(raw), 출력 경로(clean)
# raw_path = f"s3a://data-pipeline-ott/raw/watch_logs_{date}.json"
# clean_path = f"s3a://data-pipeline-ott/clean/watch_logs_{date}.parquet"
# raw_path = f"data/raw/watch_logs_{date}.json"
# clean_path = f"data/clean/watch_logs_{date}.parquet"
raw_path = f"{project_root}/data/raw/watch_logs_{date}.json"
clean_path = f"{project_root}/data/clean/date={date}"

# 1) Raw JSON 읽기
df = spark.read.json(raw_path)

# 2) 데이터 정제
df_clean = (df
    # 시청 시간: 음수나 NULL → 0 처리
    .withColumn("watch_time_sec",
                F.when((F.col("watch_time_sec").isNull()) | (F.col("watch_time_sec") < 0), F.lit(0))
                 .otherwise(F.col("watch_time_sec")))
    # 국가 허용값 체크 (허용 외 값은 "UNKNOWN")
    .withColumn("country",
                F.when(F.col("country").isin(["KR","US","JP","TW","TH"]), F.col("country"))
                 .otherwise(F.lit("UNKNOWN")))
    # 기기 허용값 체크
    .withColumn("device",
                F.when(F.col("device").isin(["ios","android","web","tv"]), F.col("device"))
                 .otherwise(F.lit("other")))
    # event_date 컬럼 추가 (날짜만 추출)
    .withColumn("event_date", F.to_date("ts"))
)

# 3) 결과 저장(Parquet, 날짜별 파티션)
(df_clean
    .repartition(1)
    .write.mode("overwrite")
    .parquet(clean_path)
)

# 4) 결과 확인
print(f"✅ 정제된 로그 저장 완료 -> {clean_path}")
