# project_crypto

Applied Cryptography project : secure storage of passwords

## Method :

Docker containers :

- **app** container containing the frontend and csv/json file for the database
- **hsm** container containing the hsm providing the encryption of the passwords

### HSM

Our secure module is a flask app build on a docker container.
We used Tink to encrypt the hashed password.

There are 2 path in this server :

- **encrypt** : takes a JSON containing the ID and HASH and use Tink and a key template AES256 to encrypt the HASH. Once it is done, it return a JSON conaining the encrypted hash

- **decrypt** : this method reads the keys from the JSON file containing them and retreives the one corresponding to the correct ID. It then decrypts the hash and returns the clear hash.

### Client

The client side contains the frontend and the hashing of the passwords.

#### Frontend

The frontend is constituted of 3 HTML pages : Home, Login and Register.
The Home page leads to the other pages.
All html include code directly used, so we did not use a JS file.

#### Hashing

The app.py contains all methods to log and register.

- **login** : in this method, we get the JSON file containing all IDs and passwords, load it in a dictionnary and use it to verify if the user id already in the database, and then we check ther password.

To verify the password, we send a request to the server to decrypt the hash stored and compare it to the password entered.

- **register** we load the DbFile and verify if the username is already used. If not, we send a JSON with the ID and password to the server requesting for the /encrypt method, and then retreive the encrypted password from it.
  After this, we add the id to the JSON body and append the whole to the DbFile. The user is registered.

  PS : The redirection does not work but the register and login do.
