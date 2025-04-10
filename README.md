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

**Note**: For integration tests to work, provide valid `MIXVEL_LOGIN`, `MIXVEL_PASSWORD`,
and `MIXVEL_STRUCTURE_ID` as env vars.
To get these values, contact MixVel support at [support@mixvel.com](mailto:support@mixvel.com).
