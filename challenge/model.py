import pandas as pd
import pickle
import numpy as np
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from typing import Tuple, Union, List


MODEL_LOGIC_R = "delay_model.pkl"

class DelayModel:

    
    def __init__(self):
        self._model = None 
        self.FEATURES_COLS = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]
        
        
    def __load_model(self, file_name):
        with open(file_name, 'rb') as fp:
            return pickle.load(fp)
        

    def __save_model(self, filename):
        with open(filename, 'wb') as fp:
            pickle.dump(self._model, fp)
            
    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """

        
        def get_min_diff(data):
            fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
            fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
            return ((fecha_o - fecha_i).total_seconds()) / 60

  
        data['min_diff'] = data.apply(get_min_diff, axis=1)
        data['delay'] = np.where(data['min_diff'] > 15, 1, 0)
        
 
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)


        features = features.reindex(columns=self.FEATURES_COLS, fill_value=0)
        
        target = data[['delay']]  

        if target_column:
            return features, target
        return features


    def fit(
        self,
        features: pd.DataFrame,
        target: pd.Series
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.Series): target.
        """
        self._model = LogisticRegression(class_weight='balanced')
        self._model.fit(features, target)

        self.__save_model(MODEL_LOGIC_R)
        
    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            List[int]: predicted targets.
        """
        
        if self._model is None:
            self._model = self.__load_model(MODEL_LOGIC_R)
        
        return self._model.predict(features).tolist()

