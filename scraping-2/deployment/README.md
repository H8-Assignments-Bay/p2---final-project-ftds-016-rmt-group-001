# Development

ARM64

```
docker run -d -p 4444:4444 -m=300m -e SE_NODE_SESSION_TIMEOUT=172800 seleniarm/standalone-chromium:latest
```

Intel

```
docker run -d -p 4444:4444 -m=300m -e SE_NODE_SESSION_TIMEOUT=172800 seleniarm/standalone-chromium:latest
```

Docker Compose

```
docker-compose up --build
```

TODO:
- [ ] seleniarm/standalone-chromium (docker) + flask (docker) boot is very slow.