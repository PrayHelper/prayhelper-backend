from sqlalchemy.dialects.postgresql import UUID
import uuid
from app import db

class Request(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		uid = db.Column(UUID(as_uuid=True), nullable=False)
		target = db.Column(db.String(50), nullable=False)
		title = db.Column(db.Text(), nullable=False)
		createdAt = db.Column(db.DateTime(), nullabe=False)
		isShared = db.Column(db.Integer, nullable=False)