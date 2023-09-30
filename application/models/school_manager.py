from application import db
from application.Mixins.GenericMixins import GenericMixin


class SchoolManager(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='managers')
    name = db.Column(db.String(250), nullable=True)
    residence = db.Column(db.String(250), nullable=True)
    _gender = db.Column(db.String(250), nullable=True)
    designation = db.Column(db.String(250), nullable=True)
    schools = db.relationship("School", back_populates='managers')

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


