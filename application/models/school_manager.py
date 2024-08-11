from application import db
from application.Mixins.GenericMixins import GenericMixin
from exceptions.custom_exception import CustomException


class SchoolManager(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    school_role_id = db.Column(db.Integer, db.ForeignKey('school_role.id', ondelete="SET NULL"))
    user = db.relationship("User", back_populates='managers')
    name = db.Column(db.String(250), nullable=True)
    residence = db.Column(db.String(250), nullable=True)
    _gender = db.Column(db.String(250), nullable=True)
    designation = db.Column(db.String(250), nullable=True)
    schools = db.relationship("School", back_populates='managers')
    school_roles = db.relationship("SchoolRole", back_populates='managers', cascade="all, delete")

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        # Ensure that the value is capitalized before assigning it
        self._gender = value.capitalize() if value else None

    @gender.getter
    def gender(self):
        # Ensure that the value is capitalized before assigning it
        return self._gender

    @classmethod
    def GetSchoolAdmin(cls, user_id, school_id):
        admin = SchoolManager.query.filter_by(id=user_id, school_id=school_id).first()
        if not admin:
            raise CustomException(message="School Admin does not exist", status_code=404)
        return admin
