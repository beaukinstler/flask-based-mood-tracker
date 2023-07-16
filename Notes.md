# NOTES



# Road map

1. simple mood logging, per user account, time tracked, limited time between new moods logs
	1. Notes allowed as well, but as attribute on the logged mood record
2. Support for adding API keys and endpoints to other media, to show info about time when mood changes
4. Encrypted notes, with front end javascript encryption keys
	5. Also, notes become their own table, but linked to the most recent allowed note
5. Visualization: Data graphs for trends in both media and user moods
6. Make sure the log entryies are indexed by user and created_at for quick search for last mood entry



# User authentication
1. https://www.freecodecamp.org/news/how-to-authenticate-users-in-flask/
2. https://pypi.org/project/Flask-Login/

### Steps

- `pip install Flask-Login`

GUESS: I think I'll add the below to the `src/__init__.py`

```
import flask_login

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
```

### API token
For API access, I will probably want to to implment a jwt soluition, like I did in another project.
[my item catalog approach](https://github.com/beaukinstler/fswd-item-catalog/blob/master/db_setup.py#L19)

1. Create secret key
	https://github.com/beaukinstler/fswd-item-catalog/blob/a96eb4767903ad5a8282d215555c33127cdb6640/db_setup.py#L25

2. In the User class, implement the secret_key global variable and the user functions:
	- [Global secret_key](https://github.com/beaukinstler/fswd-item-catalog/blob/a96eb4767903ad5a8282d215555c33127cdb6640/db_setup.py#L25)
	- [User.generate_auth_token](https://github.com/beaukinstler/fswd-item-catalog/blob/a96eb4767903ad5a8282d215555c33127cdb6640/db_setup.py#L43C9-L43C24)
		```
		"""
		Use jwt.encode
		to encrypt a token, and the secret key created global
		in the class.

		Parameters:
			self

			[optional]
			expiraexpiration: integer, seconds until expires

		Returns: encrypted token, containing id of the user
		"""
		```
	- [@staticmethod verify_auth_token(token)](https://github.com/beaukinstler/fswd-item-catalog/blob/a96eb4767903ad5a8282d215555c33127cdb6640/db_setup.py#L79C14-L79C14)


		```
		Purpose: Decrypt a token and check for the user id.
				Exceptions are thrown for expired tokens,
				and for BadSignatures. If these exceptions
				are found, "None" is returned

		Params: A token created with jwt.encode

		Returns: a user_id if successfully decrypted
				from the token
		```




## Many to many log table

Based on the SQLAlchemy docs, I've decided to use [Association Object](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object) as my model for linking the two tables.



### azure
```
az group create --name moody-flask --location eastus
az aks create --resource-group moody-flask --name flaskcluster --node-count 1 --generate-ssh-keys
az aks get-credentials --resource-group moody-flask --name flaskcluster
kubectl get nodes

$ kubectl.exe get nodes
NAME                                STATUS   ROLES   AGE     VERSION
aks-nodepool1-11853184-vmss000000   Ready    agent   7m19s   v1.25.6


az acr create --resource-group moody-flask --name bkinmoodyflask --sku Basic

$ az acr show-endpoints --name bkinmoodyflask
←[93mTo configure client firewall w/o using wildcard storage blob urls, use "az acr update --name bkinmoodyflask --data-endpoint-enabled" to enable dedicated data endpoints.←[0m
{
  "dataEndpoints": [
    {
      "endpoint": "*.blob.core.windows.net",
      "region": "eastus"
    }
  ],
  "loginServer": "bkinmoodyflask.azurecr.io"
}

loginServer": "bkinmoodyflask.azurecr.io


az aks update -n flaskcluster -g moody-flask --attach-acr bkinmoodyflask


kubectl create deployment primary --image=bkinmoodyflask.azurecr.io/moodyflask:v0.2

```