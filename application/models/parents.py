from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class Parent(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(350), nullable=True)
    last_name = db.Column(db.String(350), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    user = db.relationship("User", back_populates='parents')
    address = db.Column(db.String(350), nullable=True)
    _gender = db.Column(db.String(250), nullable=True)
    country = db.Column(db.String(350), nullable=True)
    state = db.Column(db.String(350), nullable=True)
    work_email = db.Column(db.String(350), nullable=True)
    work_address = db.Column(db.String(350), nullable=True)
    work_msisdn = db.Column(db.String(350), nullable=True)

    # work_msisdn = db.Column(db.String(350), nullable=True)

    students = db.relationship("Student", back_populates='parents')
    schools = db.relationship("School", secondary='school_parent', back_populates='parents', passive_deletes=True)

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        # Ensure that the value is capitalized before assigning it
        self._gender = value.capitalize() if value else None

    @classmethod
    def GetParent(cls, user_id):
        parent = Parent.query.filter_by(id=user_id).first()
        if not parent:
            raise CustomException(message="Parent does not exist", status_code=404)
        return parent
