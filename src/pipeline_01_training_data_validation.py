import os
import argparse
import yaml
import logging
from src.training_Validation_Insertion import train_validation

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def main(config_path, datasource):
    config = read_params(config_path)
    # print(config)
    path = config["data_source"]["batch_files"]
    # print(path)
    train_valObj = train_validation(path) #object initialization

    train_valObj.train_validation()#calling the training_validation function

   

if __name__=="__main__":
    args = argparse.ArgumentParser()
    default_config_path = os.path.join("config", "params.yaml")
    args.add_argument("--config", default=default_config_path)
    args.add_argument("--datasource", default=None)

    parsed_args = args.parse_args()
    # print(parsed_args)
    print(parsed_args.config, parsed_args.datasource)
    main(config_path=parsed_args.config, datasource=parsed_args.datasource)