"""Strumenti per il caricamento documenti e il tracciamento del processo."""

import os
import json
from pathlib import Path

from google.adk.tools import ToolContext


# ---------------------------------------------------------------------------
# Document loader (used at startup, not as an agent tool)
# ---------------------------------------------------------------------------

def load_document(file_path: str) -> str:
    """Carica un documento .docx o .pdf e restituisce il testo.

    Args:
        file_path: Percorso del file da caricare.

    Returns:
        Il contenuto testuale del documento.
    """
    path = Path(file_path)
    if not path.exists():
        return f"[ERRORE] File non trovato: {file_path}"

    suffix = path.suffix.lower()

    if suffix == ".docx":
        return _load_docx(path)
    elif suffix == ".pdf":
        return _load_pdf(path)
    else:
        return f"[ERRORE] Formato non supportato: {suffix}. Usa .docx o .pdf."


def _load_docx(path: Path) -> str:
    """Estrai testo da un file .docx."""
    from docx import Document

    doc = Document(str(path))
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            # Preserve heading hierarchy
            if para.style and para.style.name.startswith("Heading"):
                level = para.style.name.replace("Heading ", "").strip()
                try:
                    level = int(level)
                except ValueError:
                    level = 1
                paragraphs.append(f"{'#' * level} {text}")
            else:
                paragraphs.append(text)
    return "\n\n".join(paragraphs)


def _load_pdf(path: Path) -> str:
    """Estrai testo da un file .pdf."""
    import pdfplumber

    pages = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
    return "\n\n".join(pages)


# ---------------------------------------------------------------------------
# Agent tools (called by the LLM during conversation)
# ---------------------------------------------------------------------------

def salva_informazione(
    campo: str,
    valore: str,
    tool_context: ToolContext,
) -> dict:
    """Salva un'informazione raccolta dall'utente durante il processo.

    Usa questo strumento ogni volta che l'utente fornisce un dato richiesto
    da uno dei passi del processo.

    Args:
        campo: Il nome del campo o dell'informazione raccolta (es. "nome_dipendente", "data_spesa").
        valore: Il valore fornito dall'utente per quel campo.

    Returns:
        Conferma del salvataggio con lo stato attuale.
    """
    collected = tool_context.state.get("collected_info", {})
    collected[campo] = valore
    tool_context.state["collected_info"] = collected

    return {
        "status": "salvato",
        "campo": campo,
        "valore": valore,
        "totale_campi_raccolti": len(collected),
    }


def mostra_progresso(tool_context: ToolContext) -> dict:
    """Mostra un riepilogo delle informazioni raccolte finora.

    Usa questo strumento quando l'utente chiede a che punto è del processo,
    oppure alla fine per fornire un riepilogo completo.

    Returns:
        Riepilogo delle informazioni raccolte e dello stato del processo.
    """
    collected = tool_context.state.get("collected_info", {})

    if not collected:
        return {
            "status": "nessuna_informazione",
            "messaggio": "Non è stata ancora raccolta nessuna informazione.",
        }

    return {
        "status": "in_corso",
        "informazioni_raccolte": collected,
        "totale_campi": len(collected),
    }
