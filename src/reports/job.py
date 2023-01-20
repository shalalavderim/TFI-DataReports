# This script implements an ETL job with three methods
# extract, transform, load

import json
from pyspark.sql import SparkSession, DataFrame
from .t_count_rule import t_count_rule
from .t_count_any_rule import t_count_any_rule

# This method reads the input data from data lake
# The input paths are taken from config file
def extract(spark: SparkSession, config: json):
    analytics_data_path = config["reports_input_path"]
    analytics_data = spark.read.parquet(analytics_data_path)
    return analytics_data


# This method transforms the extracted data according
# to the requirements.
def transform(analytics_data: DataFrame):
    stage1_df = t_count_rule(analytics_data, "R1")
    stage2_df = t_count_rule(analytics_data, "R2")
    stage3_df = t_count_rule(analytics_data, "R3")
    stage4_df = t_count_rule(analytics_data, "R4")
    stage5_df = t_count_rule(analytics_data, "R5")
    stage6_df = t_count_any_rule(analytics_data)
    stage7_df = stage1_df.unionByName(stage2_df).unionByName(stage3_df).unionByName(stage4_df).unionByName(stage5_df).unionByName(stage6_df)
    stage8_df = stage7_df.groupBy("Manufacturer").pivot("Rule").sum("Count")
    return stage8_df


# This method writes the result back to the target folder
# in data lake. The output folder is taken from config file.
def load(result_df: DataFrame, config: json):
    output_path = config["reports_output_path"]
    result_df.write.mode("overwrite").parquet(output_path)
