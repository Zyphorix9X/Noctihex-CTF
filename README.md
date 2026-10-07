# NoctiHex CTF

## Requirements

Windows 11
Docker Desktop
WSL2
8 GB RAM minimum
Git

## Start

docker compose build
docker compose up -d

## Platform

https://noctihex.local

## Linux challenge

ssh analyst@127.0.0.1 -p 2225

## Check services

docker compose ps

## Reset NHX-03

.\scripts\reset.ps1 nhx03

## Reset NHX-05

.\scripts\reset.ps1 nhx05

## Reset all live stages

.\scripts\reset.ps1 all

## Stop

docker compose down

## Full clean reset

docker compose down -v

docker compose build --no-cache

docker compose up -d