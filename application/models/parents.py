from application import db
from application.Mixins.GenericMixins import GenericMixin


class Parent(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(350), nullable=True)
    last_name = db.Column(db.String(350), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='parents')
    address = db.Column(db.String(350), nullable=True)
    _gender = db.Column(db.String(250), nullable=True)
    country = db.Column(db.String(350), nullable=True)
    state = db.Column(db.String(350), nullable=True)
    work_email = db.Column(db.String(350), nullable=True)
    work_address = db.Column(db.String(350), nullable=True)
    work_msisdn = db.Column(db.String(350), nullable=True)
    projects = db.relationship("Project", back_populates='parents')
    students = db.relationship("Student", back_populates='parents')
    schools = db.relationship("School", secondary='school_parent', back_populates='parents')

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        # Ensure that the value is capitalized before assigning it
        self._gender = value.capitalize() if value else None
