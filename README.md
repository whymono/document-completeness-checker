DCC — Document Completeness Checker

DCC (Document Completeness Checker) is a tool that analyzes documents to surface structural gaps — places where something is referenced but never actually explained.

Instead of summarizing content or answering questions, DCC scans a document for implicit expectations. These are cases where the document assumes that a process, rule, or definition exists, without ever defining it.

For example, a policy might say that users can request a refund — but never describe how that request is made. A specification might mention termination conditions without defining what happens next. DCC attempts to automatically identify these kinds of gaps and report them in a structured way.

Problem Scope

Many documents fail not because the information they contain is incorrect, but because important details are missing.

It is common to see documents reference processes, conditions, or responsibilities without ever defining them clearly. These gaps may not be obvious at first glance, but they can create ambiguity during implementation, enforcement, or review.

This project focuses specifically on detecting those missing structural components. It does not attempt to evaluate correctness, legality, or intent — only whether required definitions appear to be absent given what the document itself references.

What This Tool Does

Given a document (PDF for now), DCC:

Detects phrases that imply required structure (such as processes, conditions, or constraints)

Groups related references across the document

Checks whether the implied components are ever fully defined

Outputs a list of missing components, each with:

what is missing

why it is expected

which parts of the document imply it

a confidence score

All results are returned as structured JSON, not free-form text.

Example Output
{
  "missing_components": [
    {
      "expected": "Refund request procedure",
      "category": "process",
      "reason": "Refunds are referenced without any description of how a request is initiated or submitted.",
      "derived_from": ["Section 3.2", "Section 5.1"],
      "confidence": 0.91
    }
  ]
}


Each item is traceable back to specific sections of the document.

How It Works (High Level)
PDF Upload
   ↓
Text Extraction & Sectioning
   ↓
Expectation Signal Detection
   ↓
Semantic Reference Grouping
   ↓
Definition Presence Check
   ↓
Missing Component Inference
   ↓
Structured JSON Output


The system combines:

deterministic parsing and pattern-based detection

semantic search using embeddings

constrained language model inference for naming and explaining gaps

AI is used selectively and late in the pipeline, with strict output validation.

What This Project Does NOT Do

This project is intentionally scoped.

❌ Does not judge legal correctness

❌ Does not guarantee document completeness

❌ Does not suggest how to fix missing items

❌ Does not replace professional review

❌ Does not train on uploaded documents

The goal is to surface structural signals, not make decisions.

Use Cases

Potential applications include:

Reviewing policies and terms of service

Checking internal documentation quality

Validating technical or product specifications

Pre-review for contracts or compliance documents

Catching structural gaps before manual review

Tech Stack

Backend: Python, FastAPI

PDF Parsing: pdfplumber / pypdf

Embeddings: Local models via Ollama

Vector Search: FAISS (local)

LLM: ChatGPT API (used only for constrained inference)

Frontend: React 19 (minimal UI)

Project Status

DCC is currently in active development.

The focus for v1 is:

correctness of the reasoning pipeline

explainable and traceable output

minimal but complete end-to-end functionality

License

This project is released under the MIT License.

Disclaimer

This project is for educational and experimental purposes only.
It should not be used as a substitute for legal, professional, or compliance advice.

Design Note

“Half knowledge is worse than no knowledge.”

A document that appears complete but leaves critical gaps can be more harmful than having no document at all.
This project exists to surface those gaps early, before assumptions turn into problems.
