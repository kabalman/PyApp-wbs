# WBS REST Api

This is built with Flask, Flask-RESTful, Flask-SQLAlchemy, psycopg2

###Create:

curl -X POST @parameters.json http://URL/wbs/create

Description:

Creates a wbs and stores it in a Postgres DB

Parameters:
⋅⋅* **company**: The company the WBS belongs to
⋅⋅* **businessunit**: The business unit the WBS belongs to
⋅⋅* **project**: The project unit the WBS belongs to


###Delete:

curl -X DELETE http://URL/wbs/delete/**<wbs>**

Deletes the specified wbs passed in the url
Parameters:
⋅⋅* **wbs**: the wbs code you want to delete


###List all:

curl -X GET http://URL/wbs/list/**<company>**/**<businessunit>**/**<project>**

Returns a list of all wbs codes belonging to the specified parameters

Parameters:
⋅⋅* **company**: The company the WBS belongs to
⋅⋅* **businessunit**: The business unit the WBS belongs to
⋅⋅* **project**: The project unit the WBS belongs to