# jobs/spark_agg.py

from pyspark.sql import SparkSession, functions as F

# 1) Spark 세션 생성: 모든 Spark 잡의 시작점
spark = (
    SparkSession.builder
    .appName("agg_logs")              # Spark UI에서 잡 이름으로 보임
    .getOrCreate()
)

# 2) 날짜 파라미터: Airflow나 터미널에서 --conf spark.run.date=YYYY-MM-DD 로 넘길 예정
date = spark.sparkContext.getConf().get("spark.run.date", "2025-09-12")
project_root = spark.sparkContext.getConf().get("project.root", ".")

# 3) 입력/출력 경로 (로컬 데모 버전)
# clean_path = f"data/clean/watch_logs_{date}.parquet"    # 이전 단계에서 만든 정제 데이터
# agg_path   = f"data/agg/date={date}"       # 집계 결과를 저장할 경로
clean_path = f"{project_root}/data/clean/date={date}"
agg_path   = f"{project_root}/data/agg/date={date}"

# 4) 정제 데이터 읽기 (Parquet)
df = spark.read.parquet(clean_path)

# 5) 핵심 집계: 일자/국가/디바이스별 DAU/총시청시간/이벤트 수
agg_daily = (
    df.groupBy("event_date", "country", "device")
      .agg(
          F.countDistinct("user_id").alias("dau"),          # Daily Active Users
          F.sum("watch_time_sec").alias("total_watch_sec"), # 총 시청 시간(초)
          F.count("*").alias("events")                      # 이벤트(로그) 수
      )
)

# 6) 저장: 파케이(Parquet)로 출력
# - 데모라서 한 파일로 저장(repartition(1)); 실제에선 파티션/파일 크기 조절
(agg_daily
    .repartition(1)
    .write.mode("overwrite")
    .parquet(agg_path)
)

print(f"✅ Aggregated metrics written to {agg_path}")
