from application import db
from application.Mixins.GenericMixins import GenericMixin


class Audit(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    data = db.Column(db.JSON(none_as_null=True), nullable=True)
    admins = db.relationship("Admin", back_populates='audits')
