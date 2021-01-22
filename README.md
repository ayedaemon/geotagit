# Geo-Tag-it

> Upload any image and it'll plot the image in the location it is clicked. This project uses metadata from the image and if the metadata (for location) is not present then it can't be displayed on map.

---

#### Test locally

1. Clone the repo locally

2. Use `Dockerfile` to create the local docker image. And then run a container.
(refer - https://fastapi.tiangolo.com/deployment/docker/?h=+docker#create-a-dockerfile)

```
## Create image from Dockerfile (make sure to add . at the end of the command)

docker build -t geo_tag_it .

## Run a container

docker run -d --name geo_tag_it_container -p 80:80 geo_tag_it

```

3. Check it on `localhost`.

4. Remove (If you want)

```
docker rm -f geo_tag_it_container
docker rmi -f geo_tag_it
```


#### Deploy on heroku

1. Login to heroku.
2. Create an application
3. Follow the instructions provided.



```
## For me this works.

#### pushing container to heroku container repo
heroku container:push web -a geotagit

#### Release the container to deploy
heroku container:release web -a geotagit
```
