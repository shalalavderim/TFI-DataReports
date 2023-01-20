# This script implements the integration test for the entire job

from pyspark import SparkContext
from pyspark.sql import SparkSession

from src.reports.job import transform



# This method implements the integration test for the transform function of the job
# extract and load functions are not tested since they are of category I/O
def test_transform():
    spark_context = SparkContext()
    spark = SparkSession.builder.getOrCreate()
    spark_context.setLogLevel("ERROR")

    print("\n---- Start Integration Test DataReports ----")
    print("Reading input data ...")
    input_df = spark.read.parquet("tests/testdata/input_data.parquet")
    input_df.show(5)

    excpeted_df = spark.read.parquet("tests/testdata/expected_data_job.parquet")
    excpeted_df.show(5)

    print("Applying Transformations ...")
    result_df = transform(input_df)
    #result_df.repartition(1).write.parquet("./tests/testdata/create_expected_table.parquett")
    result_df.show(5)

    print("Comparing Expected and Actual Result ...")
    excpeted_df.show(5)

    assert result_df.subtract(excpeted_df).rdd.isEmpty()
    assert excpeted_df.subtract(result_df).rdd.isEmpty()
    spark_context.stop()
    print("---- End Integration Test DataReports ----")