# mixvel-python-sdk

The **mixvel-python-sdk** is a Python client for the MixVel API. It simplifies the process of
integrating MixVel functionality into Python-based applications.

## Development

To run tests inside a Docker container, follow these steps.

Build the Docker image

```sh
docker build -t mixvel-sdk .
```

Run the container, supplying your MixVel credentials as environment variables

```sh
docker run -t \
  -e MIXVEL_LOGIN="testUser.auth@mixvel.com" \
  -e MIXVEL_PASSWORD="passWord1!" \
  -e MIXVEL_STRUCTURE_ID="12036_ALPHA" \
  mixvel-sdk
```

Note:

- The integration tests require valid values for `MIXVEL_LOGIN`, `MIXVEL_PASSWORD`,
  and `MIXVEL_STRUCTURE_ID`.
- To obtain these credentials, please contact MixVel support at [support@mixvel.com](mailto:support@mixvel.com).
