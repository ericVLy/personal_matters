# personal patters

- a django project based on wagtail cms

## extend requirements

- nodejs `auto install in container`
- npm `auto install in container`
- postgresql `product default`

## install

### by container

- **postgresql** are required by backend

``` sh
podman build -t personal_matters:latest .

podman run -d --name personal_matters --network host localhost/personal_matters:latest

```