from typing import Tuple
from uuid import UUID

from fastapi import File, Depends, HTTPException
import pandas as pd

from mlserver.persistence.repository import DatasetRepository, Dataset, InvalidDatasetIdException

DATASET_ENCODING = 'utf8'
DATASET_COLUMNS = {'age;sex;bmi;bp;s1;s2;s3;s4;s5;s6;y'}


class InvalidDatasetException(Exception):
    pass


class DatasetValidator:
    def validate_and_read_csv(self, dataset_file: File) -> pd.DataFrame:
        df = pd.read_csv(dataset_file.file)
        if set(df.columns) != DATASET_COLUMNS:
            raise InvalidDatasetException()
        return df


class DatasetService:
    def __init__(self,
                 repository: DatasetRepository = Depends(),
                 validator: DatasetValidator = Depends()):
        self.repository = repository
        self.validator = validator

    def persist_new(self, dataset_file: File) -> Tuple[UUID, int]:
        """
        Persist a new dataset, return new dataset id and version number

        :param dataset_file: csv file containing the data to be persisted
        """
        df = self.validator.validate_and_read_csv(dataset_file)

        dataset = Dataset(dataset_data=df.to_csv().encode(encoding=DATASET_ENCODING))
        dataset = self.repository.persist_new(dataset)
        return dataset.dataset_id, dataset.version_id

    def persist(self, dataset_id: UUID, dataset_file: File) -> int:
        """
        Persist a new version of a dataset, return the new version number

        :param dataset_id: id of persisted dataset
        :param dataset_file: csv file containing the data to be persisted
        """
        try:
            df = self.validator.validate_and_read_csv(dataset_file)

            dataset = Dataset(dataset_id=dataset_id, dataset_data=df.to_csv().encode(encoding=DATASET_ENCODING))
            dataset = self.repository.persist(dataset)
            return dataset.version_id
        except InvalidDatasetIdException as exc:
            raise HTTPException(status_code=404, detail="Invalid dataset id")

    def get_by_id_and_version(self, dataset_id: UUID, version_id: int) -> pd.DataFrame:
        dataset = self.repository.get_by_id_and_version(dataset_id, version_id)
        csv = dataset.dataset_data.decode(encoding=DATASET_ENCODING)
        return pd.read_csv(csv)
