from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class Admin(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=True)
    last_name = db.Column(db.String(250), nullable=True)
    profile_image = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(250), nullable=True)
    state = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    user = db.relationship("User", back_populates='admins')
    residence = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(150), nullable=True)
    checklist = db.relationship("ChecklistQuestion", back_populates="admins")

    @classmethod
    def GetAdmin(cls, user):
        if not user.admins:
            raise CustomException(message="Admin does not exist", status_code=404)
        return user.admins
