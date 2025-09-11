# from sqlalchemy import create_engine, Column, Integer, String, Text
# from sqlalchemy.ext.declarative import declarative_base
# from core.config import settings
# from time import Datetime
# from datetime import datetime

# # Create database engine
# engine = create_engine(
#     settings.DATABASE_URL,
#     connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
# )
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # Create a base class for ORM
# Base = declarative_base()

# class ChatHistory(Base):
#     __tablename__ = "chat_history"
#     id = Column(Integer, primary_key=True, index=True)
#     session_id = Column(String, index=True)
#     user_message = Column(Text, nullable=False)
#     bot_response = Column(Text, nullable=False)
#     timestamp = Column(datetime, default=datetime.utcnow)

#     def __repr__(self):
#         return {
#             "id": self.id,
#             "session_id": self.session_id,
#             "user_message": self.user_message,
#             "bot_response": self.bot_response,
#             "timestamp": self.timestamp.isoformat(),
#             "response_time": self.response_time,
#             "model_used": self.model_used
#         }


# # Create tables
# def create_tables():
#     Base.metadata.create_all(bind=engine)


# # Database dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
