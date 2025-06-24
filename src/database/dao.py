from sqlalchemy import select, insert, update, create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, Client, Messages
from src.settings import APP_SETTINGS

engine = create_engine(APP_SETTINGS.DB_URL, echo=False)

Session = sessionmaker(autoflush=False, bind=engine)


class BaseDAO:
    model: Base | None = None

    @classmethod
    def find_by_id(cls, model_id: int):
        with Session() as session:
            q = select(cls.model).filter_by(id=model_id)
            result = session.execute(q)
            return result.scalar_one_or_none()

    @classmethod
    def find_one_or_none(cls, **kwargs):
        with Session() as session:
            q = select(cls.model).filter_by(**kwargs)
            result = session.execute(q)
            return result.scalar_one_or_none()

    @classmethod
    def find_all(cls, **kwargs):
        with Session() as session:
            q = select(cls.model).filter_by(**kwargs)
            result = session.execute(q)
            return result.scalars().all()

    @classmethod
    def create(cls, **data):
        with Session() as session:
            q = insert(cls.model).values(**data)
            session.execute(q)
            session.commit()

    @classmethod
    def update(cls, id: int, **data):
        with Session() as session:
            q = (
                update(cls.model)
                .filter_by(id=id)
                .values(**data)
            )
            session.execute(q)
            session.commit()


class ClientDao(BaseDAO):
    model = Client


class MessagesDao(BaseDAO):
    model = Messages

    @classmethod
    def get_history(cls, from_user_id: int, to_user_id: int):
        with Session() as session:
            q = (
                select(cls.model)
                .filter(
                    or_(
                        and_(cls.model.from_user == from_user_id, cls.model.to_user == to_user_id),
                        and_(cls.model.from_user == to_user_id, cls.model.to_user == from_user_id),
                    )
                ).order_by(cls.model.date_create.asc())
            )
            result = session.execute(q)
            return result.scalars().all()
