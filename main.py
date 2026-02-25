from sensor.exception import SensorException
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainPipeline
import sys
# def test_exception():
#     try:
#         logging.info(" yaahn ek error ayega")
#         a=1/0
#     except Exception as e:
#         raise SensorException(e,sys)    



# if __name__=="__main__":
#     file_path=r"C:\myprojects\sensorlive\aps_failure_training_set1.csv"
#     database_name="isatya"
#     collection_name="sensor"
#     dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)

if __name__ == "__main__":
    try:
        logging.info("Starting Training Pipeline")

        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()

        logging.info("Training Pipeline completed successfully")

    except Exception as e:
        logging.exception(e)
        raise SensorException(e, sys)