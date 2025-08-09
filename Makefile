.PHONY: install run docker-build up down logs

install:
`tpython -m pip install -r requirements.txt

run:
`tpython main.py

docker-build:
`tdocker build -t support-bot .

up:
`tdocker compose up -d --build

down:
`tdocker compose down

logs:
`tdocker compose logs -f
