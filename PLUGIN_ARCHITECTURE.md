## Plugin architecture constraint
- plugin itself shouldn't care how auth is happening.
- plugin functions should not have any access to authentication mechanism.

## Architecture
- For a platform, a class is created for the platform that has methods specific to the actions that the agent can take.
