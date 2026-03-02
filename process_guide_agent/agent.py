"""Agente guida al processo aziendale — entry point ADK."""

import os
from pathlib import Path

from google.adk.agents import Agent
from google.genai import types

from .prompts import ROOT_AGENT_INSTRUCTION
from .tools import load_document, salva_informazione, mostra_progresso


# ---------------------------------------------------------------------------
# Load the process document at import time
# ---------------------------------------------------------------------------

def _get_document_text() -> str:
    """Read the process document specified in the environment."""
    doc_path = os.environ.get("PROCESS_DOCUMENT_PATH", "sample_process.docx")

    # Resolve relative paths from the project root
    if not os.path.isabs(doc_path):
        project_root = Path(__file__).resolve().parent.parent
        doc_path = str(project_root / doc_path)

    return load_document(doc_path)


# Build the instruction with the document embedded
_document_text = _get_document_text()
_instruction = ROOT_AGENT_INSTRUCTION.format(process_document=_document_text)


# ---------------------------------------------------------------------------
# Root agent
# ---------------------------------------------------------------------------

root_agent = Agent(
    name="process_guide_agent",
    model="gemini-2.5-flash",
    description=(
        "Agente che guida i dipendenti passo dopo passo attraverso un "
        "processo aziendale descritto in un documento."
    ),
    instruction=_instruction,
    tools=[salva_informazione, mostra_progresso],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Low temperature for precise, consistent guidance
    ),
)
