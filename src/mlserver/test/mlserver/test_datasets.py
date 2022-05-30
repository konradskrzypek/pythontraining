import os
import uuid
import unittest
from unittest.mock import MagicMock, create_autospec

import pandas as pd
from fastapi import HTTPException

from ...datasets import DatasetService, DatasetValidator
from ...persistence.repository import DatasetRepository, Dataset, InvalidDatasetIdException


class TestDatasetService(unittest.TestCase):

    def test_should_save_proper_csv(self):
        repository = create_autospec(DatasetRepository)
        validator = create_autospec(DatasetValidator)
        dataset_id = uuid.uuid4()
        service = DatasetService(repository=repository, validator=validator)
        dataframe = pd.DataFrame()
        expected_version = 1

        validator.validate_and_read_csv.return_value = dataframe
        repository.persist.return_value = Dataset(dataset_id=dataset_id, version_id=expected_version)

        with open('mlserver/test/mlserver/ok.csv', 'r') as dataset_file:
            actual_version = service.persist(dataset_id, dataset_file)
            validator.validate_and_read_csv.assert_called()
            self.assertEquals(actual_version, expected_version)

    def test_should_throw_when_dataset_not_found(self):
        repository = create_autospec(DatasetRepository)
        validator = create_autospec(DatasetValidator)
        dataset_id = uuid.uuid4()
        service = DatasetService(repository=repository, validator=validator)
        dataframe = pd.DataFrame()
        expected_version = 1

        validator.validate_and_read_csv.return_value = dataframe

        def raise_invalid_dataset_id_exception():
            raise InvalidDatasetIdException()

        repository.persist.side_effect = InvalidDatasetIdException()

        with open('mlserver/test/mlserver/ok.csv', 'r') as dataset_file:
            with self.assertRaises(HTTPException) as cm :
                actual_version = service.persist(dataset_id, dataset_file)
                self.assertFalse("Exception expected")
            actual_exception = cm.exception
            self.assertEquals(actual_exception.detail, "Invalid dataset id")
