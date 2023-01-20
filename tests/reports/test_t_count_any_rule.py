# This script implements the integration test for a transformation

from pyspark import SparkContext
from pyspark.sql import SparkSession

from src.reports.t_count_any_rule import t_count_any_rule


# This method implements the integration test for transformation t_count_any_rule
def test_t_count_any_rule():
    spark_context = SparkContext()
    spark = SparkSession.builder.getOrCreate()
    spark_context.setLogLevel("ERROR")

    print("\n---- Start Test t_count_any_rule ----")
    print("Reading input data ...")
    input_df = spark.read.parquet("tests/testdata/input_data.parquet")
    input_df.show(5)

    excpeted_df = spark.read.parquet("tests/testdata/expected_data_t2.parquet")
    excpeted_df.show(5)

    print("Applying Transformations ...")
    result_df = t_count_any_rule(input_df)
    #result_df.repartition(1).write.parquet("./tests/testdata/create_expected_table.parquett")
    result_df.show(5)

    print("Comparing Expected and Actual Result ...")
    excpeted_df.show(5)

    assert result_df.subtract(excpeted_df).rdd.isEmpty()
    assert excpeted_df.subtract(result_df).rdd.isEmpty()
    spark_context.stop()
    print("---- End Test t_count_any_rule ----")
