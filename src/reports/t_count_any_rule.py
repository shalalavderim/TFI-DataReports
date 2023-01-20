# In this script is implemented a single transformation
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, count

# This method calculates the number of cases where any Rule applies for each Manufacturer
def t_count_any_rule(input_data: DataFrame):
    step1_df = input_data.filter("R1 = 'True' OR R2 = 'True' OR R3 = 'True' OR R4 = 'True' OR R5 = 'True'")
    step2_df = step1_df.groupBy("Manufacturer").count().alias("Count")
    step3_df = step2_df.withColumn("Rule", lit("R"))

    return step3_df
