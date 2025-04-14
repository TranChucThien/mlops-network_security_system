import sys, os
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_atifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_atifact
            self.data_transformation_config = data_transformation_config
            
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def get_data_transformer_object(cls) -> Pipeline:
        logging.info("Entering get_data_transformer_object method")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("KNNImputer object created")
            
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def initiate_data_tranformation(self, ) -> DataTransformationArtifact:
        
        try:
            logging.info("Data Transformation started")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ## training data fram
            input_features_train = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train = train_df[TARGET_COLUMN]
            target_feature_train = target_feature_train.replace(-1, 0)
            
            ## testing data fram
            input_features_test = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test = test_df[TARGET_COLUMN]
            target_feature_test = target_feature_test.replace(-1, 0)
            
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_features_train)
            transfromed_input_train = preprocessor_object.transform(input_features_train)
            transfromed_input_test = preprocessor_object.transform(input_features_test) 
            
            train_arr = np.c_[np.array(transfromed_input_train), np.array(target_feature_train)] 
            test_arr = np.c_[np.array(transfromed_input_test), np.array(target_feature_test)]
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)
            
            #preparing artifact
            
            data_tranformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            return data_tranformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e