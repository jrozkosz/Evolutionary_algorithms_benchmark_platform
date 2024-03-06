#!/bin/bash

docker build -t algorithm -f Dockerfile .

docker run -d --name ranking_evolutionary algorithm
