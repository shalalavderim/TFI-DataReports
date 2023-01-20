# In this script is implemented a single transformation
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, count

# This method calculates the number of cases where given Rule applies for each Manufacturer
def t_count_rule(input_data: DataFrame, rule_name: str):
    step1_df = input_data.filter(f"{rule_name} = 'True'")
    step2_df = step1_df.groupBy("Manufacturer").agg(count(rule_name).alias("Count"))
    step3_df = step2_df.withColumn("Rule", lit(f"{rule_name}"))

    return step3_df
