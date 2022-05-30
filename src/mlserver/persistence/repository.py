import uuid

from sqlalchemy import Column, Integer, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from src.mlserver.persistence.engine import Base, engine


class InvalidDatasetIdException(Exception):
    pass

class Model(Base):
    __tablename__ = 'model'
    model_id = Column(UUID(as_uuid=True), primary_key=True)
    version_id = Column(Integer, primary_key=True, autoincrement=True)
    model_data = Column(LargeBinary)


class Dataset(Base):
    __tablename__ = 'dataset'
    dataset_id = Column(UUID(as_uuid=True), primary_key=True)
    version_id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_data = Column(LargeBinary)
    # __mapper_args__ = {
    #     "version_id_col": version_id
    # }


class DatasetRepository:
    def __init__(self, ):
        pass;

    def persist_new(self, dataset: Dataset) -> Dataset:
        with Session(engine) as session:
            dataset_id = uuid.uuid4()
            while self.dataset_exists(session, dataset_id):
                dataset_id = uuid.uuid4()

            dataset.dataset_id = dataset_id
            session.add(dataset)
            session.commit()
            session.refresh(dataset)
        return dataset

    def persist(self, dataset: Dataset) -> Dataset:
        with Session(engine) as session:
            if not self.dataset_exists(session, dataset.dataset_id):
                raise InvalidDatasetIdException()

            session.add(dataset)
            session.commit()
            session.refresh(dataset)
        return dataset

    def get_by_id_and_version(self, dataset_id: UUID, version_id: int) -> Dataset:
        with Session(engine) as session:
            dataset = session.get(
                Dataset,
                {"id": dataset_id, "version_id": version_id}
            )
            return dataset

    def dataset_exists(selfself, session : Session, dataset_id : UUID) -> bool:
        q = session.query(Dataset).filter(Dataset.dataset_id == dataset_id)
        return session.query(q.exists()).scalar()


class ModelRepository:
    def __init__(self):
        # db models
        # user modelsuser
        # pwd models
        #TODO: db access config
        pass

    def persist(self, model: Model) -> Model:
        with Session(engine) as session:
            return session.add(model)

    def get_by_id_and_version(self, model_id: UUID, version_id: int) -> Model:
        with Session(engine) as session:
            model = session.get(
                Model,
                {"id": model_id, "version_id": version_id}
            )
            return model


# uncomment to reinitialize DB schema
#
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)