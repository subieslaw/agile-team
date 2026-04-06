#!/bin/bash
docker run -it -d \
  --name ai-code-dev \
  -v $(pwd):/workspace:Z \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ai-code-home:/home/developer \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY \
  subieslaw/ai-code:latest \
  sleep infinity
  