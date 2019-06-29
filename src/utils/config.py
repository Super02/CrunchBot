import json
import firebase_admin
import discord
import os
from firebase_admin import credentials, firestore

class PathNotFound(BaseException): pass

class Config:

	def __init__(self, arg_creds = os.environ['FIREBASE']):
		if isinstance(arg_creds, str):
			creds = credentials.Certificate(json.loads(arg_creds))
		elif isinstance(arg_creds, dict):
			creds = credentials.Certificate(credentials)
		else:
			raise ValueError("credentials needs to be either json string or dict")

		app = firebase_admin.initialize_app(creds, name="crunchbot")
		self.db = firestore.client(app=app)

	# Getters
	def getRaw(self, path: str, key: str = None):
		doc_ref = self.db.document(str(path)).get()
		if doc_ref.exists:
			doc_ref = doc_ref.to_dict()
			if key is None:
				return doc_ref
			else:
				return doc_ref[str(key)]
		else:
			raise PathNotFound(f"The path '{path}' doesn't exist")

	def getServerConfig(self, id, key: str = None):
		if isinstance(id, discord.Guild):
			id = str(id.id)
		else:
			id = str(id)

		default_server_config = self.db.document("config/default_server_config").get()
		server_config = self.db.document(f"server_configs/{id}").get()
		if not server_config.exists:
			server_config = default_server_config

		server_config = {**default_server_config.to_dict(), **server_config.to_dict()}

		if key is None:
			return server_config

		return server_config[key]

	# Setters
	def setRaw(self, path: str, key: str, value: str):
		return self.db.document(str(path)).update({str(key): value})


if __name__ == "__main__":
	import os
	x = Config(os.environ['FIREBASE'])

	x.setRaw("config/config/", 1, "test")