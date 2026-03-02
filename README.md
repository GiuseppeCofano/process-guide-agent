# Process Guide Agent 🇮🇹

Agente ADK che guida i dipendenti passo dopo passo attraverso un processo aziendale descritto in un documento (.docx o .pdf).

## Setup

### 1. Crea un virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Installa le dipendenze

```bash
pip install -e .
```

### 3. Configura le variabili d'ambiente

Modifica il file `.env`:

```env
GOOGLE_API_KEY=la-tua-api-key
PROCESS_DOCUMENT_PATH=sample_process.docx
```

- **`GOOGLE_API_KEY`** — La tua Google API key per Gemini. Ottienila da [Google AI Studio](https://aistudio.google.com/apikey).
- **`PROCESS_DOCUMENT_PATH`** — Percorso al documento del processo (`.docx` o `.pdf`). Può essere relativo alla root del progetto.

### 4. Genera il documento di esempio (opzionale)

```bash
python create_sample_doc.py
```

Questo crea `sample_process.docx` — una procedura di "Richiesta Rimborso Spese" con 6 passi.

### 5. Avvia l'agente

```bash
adk web .
```

Apri [http://localhost:8000](http://localhost:8000) nel browser, seleziona **process_guide_agent** e inizia a chattare!

## Come usare il tuo documento

Sostituisci `sample_process.docx` con il tuo documento di processo:

1. Copia il tuo file `.docx` o `.pdf` nella cartella del progetto
2. Aggiorna `PROCESS_DOCUMENT_PATH` nel file `.env`
3. Riavvia l'agente con `adk web .`

## Struttura del progetto

```
├── process_guide_agent/
│   ├── __init__.py     # Entry point ADK
│   ├── agent.py        # Definizione root_agent
│   ├── prompts.py      # Prompt di sistema in italiano
│   └── tools.py        # Parser documenti + strumenti di tracking
├── create_sample_doc.py  # Genera il documento di esempio
├── pyproject.toml      # Dipendenze del progetto
├── .env                # Variabili d'ambiente
└── README.md
```

## Formati supportati

| Formato | Libreria     |
|---------|-------------|
| `.docx` | python-docx |
| `.pdf`  | pdfplumber  |
