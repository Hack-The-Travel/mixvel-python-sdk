# mixvel-python-sdk

The `mixvel-python-sdk` is a python client for interacting with the MixVel API.
It is designed to simplify the integration of MixVel functionality into
python-based applications.

## Development

To run tests in a Docker container, use:

```sh
docker build -t mixvel-sdk .
docker run -t \
  -e MIXVEL_LOGIN="testUser.auth@mixvel.com" \
  -e MIXVEL_PASSWORD="passWord1!" \
  -e MIXVEL_STRUCTURE_ID="12036_ALPHA" \
  mixvel-sdk
```
