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

- **encrypt**
