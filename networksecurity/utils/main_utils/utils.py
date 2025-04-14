import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
import pickle
 

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    
    :param file_path: Path to the YAML file.
    :return: Dictionary containing the contents of the YAML file.
    """
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.ndarray):
    """
    Saves a NumPy array to a specified file path.
    
    :param file_path: Path to save the NumPy array.
    :param array: NumPy array to save.
    """
    try:
        dir_path= os.path.dirname(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file: 
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def save_object(file_path: str, obj: object) -> None:
    """
    Saves an object to a specified file path using pickle.
    
    :param file_path: Path to save the object.
    :param obj: Object to save.
    """
    try:
        logging.info(f"Saving object at: {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logging.info(f"Object saved at: {file_path}")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e