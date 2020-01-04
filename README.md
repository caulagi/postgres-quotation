# postgres-quotation

This repo contains one sql file that can be used to
populate a postgres database with quotations.

The dataset for quotations is from https://www.kaggle.com/akmittal/quotes-dataset

You need **git lfs** for working with this repo.

## Example use

```shell
$ docker run -e POSTGRES_PASSWORD=1234 -p 5432:5432 -v $(pwd)/data/data.sql:/docker-entrypoint-initdb.d/01-data.sql postgres:12
```
