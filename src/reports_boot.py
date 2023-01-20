# This script is the job definition code
import sys
import json
from notebookutils import mssparkutils
from reports.job import extract,transform,load
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

# This method initializes spark context,
# reads the configuration and
# executes the extract, transform, load
# methods of the job.
if __name__ == "__main__":
    # Intialize Context & Config
    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc)
    config_file_path = sys.argv[1]
    config = json.loads(mssparkutils.fs.head(config_file_path))

    # Read the Inputs
    print("Reading Inputs...")
    input_analytics_df = extract(spark, config)
    # Process the Data
    print("Transforming Data...")
    result_df = transform(input_analytics_df)
    # Write the Output
    print("Writing Result...")
    load(result_df, config)