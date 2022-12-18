# Note

The selenium connection is slow. It takes at least a minute.

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

  - Culprit found: when `app.py` import `scraputil`, the webdriver gets called. So, it open the browser 2 times.