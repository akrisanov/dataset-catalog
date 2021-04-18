# Building Docker Image

In the project root directory execute the command:

```shell
export DOCKER_BUILDKIT=1

docker build -t akrisanov/dataset-catalog:<VERSION> . --no-cache
```

## Pushing Release Image to Private Docker Registry

_I'm using Artifactory here._

First, authenticate your account with credentials:

```shell
docker login https://[repository-name].[organization].com
```

Then, find a tag of your release image, tag it with a proper name of the private Docker registry,
and push it to the repository:

```shell
docker images | head
docker tag <IMAGE_ID> [repository-name].[organization].com/dataset-catalog:<VERSION>
docker push [repository-name].[organization].com/dataset-catalog:<VERSION>
```
