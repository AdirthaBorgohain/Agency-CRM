@echo off
cd %~dp0
docker-compose build
docker-compose up -d
