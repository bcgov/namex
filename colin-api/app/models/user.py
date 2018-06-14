from app import db


class User(db.Model):

    APPROVER='names_approver'
    EDITOR='names_editor'
    VIEWONLY='names_viewer'

