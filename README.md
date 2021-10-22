[![codecov](https://codecov.io/gh/dhdtech/dojo-dojo/branch/main/graph/badge.svg?token=DXMWQL1375)](https://codecov.io/gh/dhdtech/dojo-dojo)
# ${{ secrets. DHD_ECR_REPO_NAME }}
API to get contents from oficial SKF databases.

## To run the project on develop environment
### First Time:
  Requires: Unix based system, docker, docker compose, make and at least python3.8.
```shell
make configure_devel
make build
make up
```

## To run the project on develop environment
### Second time an on...:
  Requires: Unix based system, docker, docker compose, make and at least python3.8.
```shell
make up
```


## To run unit tests:
```shell
source venv/bin/activate
make init_test
```
## Do you wanna dev here? Follow this.
![image](https://user-images.githubusercontent.com/49169467/135934002-10881b9d-3841-46ad-a809-085f2732d818.png)
