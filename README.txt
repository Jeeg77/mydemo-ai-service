Alcune note sul modulo Python-AI

- prima di avviarlo occorre creare l'ambiente virtuale (venv)
- nella cartella del modulo eseguire -> Get-ChildItem -Force
- se esiste venv allora l'ambiente virtuale esiste (basta anche vedere se nel progetto è presente la cartella .venv)
- se non esiste crearlo con il comando -> py -3.13 -m venv .venv
- dopo che è stato creato attivarlo con il comando -> .\.venv\Scripts\Activate.ps1
- quando compare (venv) nel prompt è possibile installare dipendenze e quant'altro: ad esempio
  python -m pip install --upgrade pip
  python -m pip install fastapi uvicorn pydantic 
  ...

- sempre con (venv) attivo eseguire -> python -c "from fastapi import FastAPI; print('FastAPI OK')"
- verificare che FastAPI è ok

- Infine avviare l'app in locale con il comando: uvicorn app.main:app --reload --port 8000
- Chiamare l'app con le api di prova, e verificare dal browser:
  http://localhost:8000/health (se abbiamo già definito l'endpoint).
  http://localhost:8000/docs (documentazione Swagger generata automaticamente da FastAPI).