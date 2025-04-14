import os
import sys
import numpy as np
import pandas as pd


TARGET_COLUMN = "Result"
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR = "Atifacts"
FILE_NAME = "phishingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"


DATA_INSGESTION_COLLECTION_NAME = "NetworkData"
DATA_INSGESTION_DATABASE_NAME = "NetworkSecurity"
DATA_INSGESTION_DIR_NAME = "data_ingestion"
DATA_INSGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INSGESTION_INGESTED_DIR = "ingested"
DATA_INSGESTION_TRAIN_TEST_SPLIT_RATION = 0.2