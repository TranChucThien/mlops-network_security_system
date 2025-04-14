
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
import os, sys
from scipy.stats import ks_2samp
import pandas as pd

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f"Number of columns in the schema: {number_of_columns}")
            logging.info(f"Number of columns in the dataframe: {len(dataframe.columns)}")
            if len(dataframe.columns) != number_of_columns:
                return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_sample_dist = ks_2samp(d1,d2)
                if threshold <= is_sample_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column: {"pvalue": float(is_sample_dist.pvalue), "drift_staus": is_found}})
                
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            ## Creating directory for the drift report file
            
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(drift_report_file_path, report, replace=True)
            return status
           
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            # Read the data from train and test files
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            ## Validate the number of columns in the train and test dataframes
            is_train_valid = self.validate_number_of_columns(train_dataframe)
            is_test_valid = self.validate_number_of_columns(test_dataframe)
            
            if not is_train_valid:
                error_message = "Train dataframe has invalid number of columns\n."
            if not is_test_valid:
                error_message = "Test dataframe has invalid number of columns\n."
            
            
            #check data drift
            status = self.detect_dataset_drift(train_dataframe, test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_data_dir)
            os.makedirs(dir_path, exist_ok=True) 
            print(dir_path)
            # Ensure the directory for valid train file exists
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)
            # Ensure the directory for valid test file exists
            os.makedirs(os.path.dirname(self.data_validation_config.valid_test_file_path), exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True

            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)