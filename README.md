# ADV XAI FULFILMENT

## Requisiti Ambiente

`python 3.11.5`

## Preparazione ambiente

Linguaggio di programmazione richiesto:

```bash
python 3.11.5
```

Script di installazione:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Avvio del server in modalità debug

```bash
.\venv\Scripts\activate
python .\startServer.py -LEVEL DEBUG
```

il server di debug sarà consultabile con swagger sull'end point `http://localhost:8505/api/doc`

## Test

Per eseguire i test:

```bash
python -m unittest -v
```

Per avere un report di _coverage_:

```bash
python -m coverage run -m unittest | python -m coverage report
```

## DEPLOY

push on agridatavalue gitlab
create the tag
