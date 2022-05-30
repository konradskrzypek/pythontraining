from uuid import UUID

import pickle
import pandas as pd
from fastapi import Depends
from sklearn.tree import DecisionTreeRegressor

from mlserver.datasets import DatasetService
from mlserver.persistence.repository import ModelRepository, Model


class DecisionTreeModel:
    regressor: DecisionTreeRegressor

    def __init__(self, pickle_data: bytes = None):
        if pickle_data:
            self.regressor = pickle.loads(__data=pickle_data)
        else:
            self.regressor = DecisionTreeRegressor(max_depth=2)
        pass

    def fit_decision_tree(self, df: pd.DataFrame) -> DecisionTreeRegressor:
        """
        Fit a DecissionTreeRegressor model using supplied dataframe.
        'y' column is used as target vaules for fitting
        :param df:
        :return: regressor - DecissionTreeRegressor object
        """

        X = df.drop("y", axis=1)
        y = df["y"]

        # Fit regression model
        self.regressor.fit(X, y)

    def predict(self, X):
        return self.regressor.predict(X)

    def serialize(self) -> bytes:
        return pickle.dumps(self.regressor)


class MlService:

    def __init__(self, dataset_service: DatasetService = Depends(), model_repository: ModelRepository = Depends()):
        self.model_repository = model_repository
        self.dataset_service = dataset_service

    def train_new(self, dataset_id: UUID, version_id: int) -> UUID:
        dataset = self.dataset_service.get_by_id_and_version(dataset_id, version_id)
        decision_tree = DecisionTreeModel()
        decision_tree.fit_decision_tree(dataset)
        model = self.model_repository.persist(Model(model_data=decision_tree.serialize()))
        return model.model_id

    def predict(self, model_id: UUID, version_id: int, x) -> float:
        model = self.model_repository.get_by_id_and_version(model_id, version_id)
        decision_tree = DecisionTreeModel(pickle_data=model.model_data)
        return decision_tree.predict(x)
