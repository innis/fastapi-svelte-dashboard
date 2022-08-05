# fastapi-svelte-dashboard
templates of fastapi with svelte admin dashboard - ([Norus](https://github.com/creativetimofficial/notus-svelte) by Creative Tim)

## Using
- fastapi
- pydantic
- sqlalchemy
- uvicorn
- pyjwt
- pymysql
- svelte
- rollup
- tailwind css
- fortawesome
- chartjs

## Quick Start
### build svelte dashboard
build files are in admin-app/public/build
```bash
cd admin-app
yarn install
yarn build
yarn build:tailwind
yarn build:fontawesome
cd ..
```

run backend api with docker
```bash
docker build -f Dockerfile.local -t fastapi-svelte .
docker run -t --rm --name fastapi-svelte -p 8080:80 -v `pwd`:/code --link mysql:fastapidb -e env="local" fastapi-svelte
INFO:     Will watch for changes in these directories: ['/code']
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
INFO:     Started reloader process [1] using StatReload
INFO:     Started server process [8]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     172.17.0.1:47318 - "GET /docs HTTP/1.1" 200 OK
INFO:     172.17.0.1:47318 - "GET /openapi.json HTTP/1.1" 200 OK
```

## test
- api swagger : http://localhost:8080/docs
- admin dashboard : http://localhost:8080/admin/
