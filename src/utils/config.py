import json
import firebase_admin
import discord
from firebase_admin import credentials, firestore

class PathNotFound(BaseException): pass

class Config:

	def __init__(self, arg_creds):
		if isinstance(arg_creds, str):
			creds = credentials.Certificate(json.loads(arg_creds))
		elif isinstance(arg_creds, dict):
			creds = credentials.Certificate(credentials)
		else:
			raise ValueError("credentials needs to be either json string or dict")

		app = firebase_admin.initialize_app(creds, name="crunchbot")
		self.db = firestore.client(app=app)

	# Getters
	def _get(self, path: str, key: str = None):
		document = self.db.document(str(path)).get()
		if document.exists:
			document = document.to_dict()
			if key is None:
				return document
			else:
				return document[str(key)]
		else:
			raise PathNotFound(f"The path '{path}' doesn't exist")

	# Setters
	def _set(self, path: str, key: str, value: str):
		return self.db.document(str(path)).update({str(key): value})
	
	def getServerConfig(self, id):
		if isinstance(id, discord.Guild):
			id = str(id.id)
		elif isinstance(id, int):
			id = str(id)
		elif not isinstance(id, str):
			raise ValueError(f"The id '{id}' is not valid")
		


if __name__ == "__main__":
	import os
	x = Config(os.environ['FIREBASE'])

	x._set("config/config/", 1, "test")