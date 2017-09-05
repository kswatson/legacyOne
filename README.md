# legacyOne
Project for Legacy One vaporizer website and resources

## Deployment
The cloudformation template cft.yaml deploys the api and it's resources, assuming the code can be found in S3.
After the cloudformation stack is created the Api Gateway must be deployed to the environment in use.
If no code changes are made the sdk used by the website should not need to be altered.