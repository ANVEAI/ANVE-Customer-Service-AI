from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import os

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, default=lambda: str(uuid.uuid4()))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    context = Column(JSON)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "context": self.context
        }

class Metric(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True)
    metric_type = Column(String(50))
    value = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "metric_type": self.metric_type,
            "value": self.value,
            "timestamp": self.timestamp.isoformat()
        }

def get_database_url():
    # Use SQLite for development
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data.db')
    return f"sqlite:///{db_path}"

def init_db():
    engine = create_engine(get_database_url())
    Base.metadata.create_all(engine)
    return engine 