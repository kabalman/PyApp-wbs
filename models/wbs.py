from db import db


class WBS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String)
    businessunit = db.Column(db.String)
    project = db.Column(db.String)
    wbs = db.Column(db.String)
    owner = db.Column(db.String)

    def __init__(self, company, businessunit, project, wbs, owner):
        self.company = company
        self.businessunit = businessunit
        self.project = project
        self.wbs = wbs
        self.owner = owner

    def json(self):
        return {'WBS': self.wbs}

    @classmethod
    def find_by_wbs(cls, wbs):
        return WBS.query.filter_by(wbs=wbs).first()

    @classmethod
    def find_by_owner(cls, owner):
        return WBS.query.filter_by(owner=owner).all()

    @classmethod
    def find_by_company(cls, company):
        return WBS.query.filter_by(company=company).all()

    @classmethod
    def find_all(cls, company, businessunit, project):
        return WBS.query.filter_by(company=company, businessunit=businessunit, project=project)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
