from flask import request
from flask_restful import Resource
import psycopg2
from models.wbs import WBS


class CreateWBS(Resource):
    def post(self):
        data = request.get_json()
        wbstoadd = WBS(data['company'], data['businessunit'], data['project'], data['wbs'], data['owner'])
        try:
            WBS.save_to_db(wbstoadd)
            return {"message": "WBS code added"}, 201
        except:
            return {'message': 'WBS Code already exists'}, 400


class DeleteWBS(Resource):
    def delete(self, wbs):
        wbs = WBS.find_by_wbs(wbs)
        if wbs:
            WBS.delete_from_db(wbs)
        return {'message': 'WBS {} deleted'.format(wbs.wbs)}


class ListWBS(Resource):
    def get(self, company, businessunit, project):
        try:
            return {'WBS Codes': list(map(lambda x: x.json(), WBS.find_all(company, businessunit, project)))}, 200
        except Exception:
            return {'message': 'No WBS Codes found'}, 404
