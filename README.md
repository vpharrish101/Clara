# Clara

What it is: An automated pipeline that ingests client voice transcripts, and converts into structured AI agent configurations and tracks configuration updates from onboarding conversations.

**Architecture: -**
<img width="1225" height="278" alt="image" src="https://github.com/user-attachments/assets/77dcfba3-dc50-4dd7-bb8e-d498f91ea3c5" />


**How it works: -**

1. Client demo call transcripts are fed into an LLM, which extracts structured information and populates the predefined account memo schema.
2. The extracted data is stored as a **v1 configuration** (`account_memo.json`) representing the preliminary agent setup based only on demo information.
3. When onboarding call transcripts are provided, the system compares them with the existing v1 configuration and extracts **only the fields that require updates**.
4. These updates are stored as a patch (`updates.json`) and merged with the v1 configuration to produce a **v2 configuration**, preserving version history.
5. A **change log** is generated that highlights which fields were modified between v1 and v2.
6. Finally, the updated configuration is used to generate a **Retell Agent Specification**, which defines the voice agent’s prompt, routing rules, and operational behavior.


## Project Structure
```text
clara/

├── data/
│   ├── demo_calls/
│   │   └── account_001.txt
│   │
│   └── onboarding_calls/
│       └── account_001.txt
│
├── outputs/
│   └── accounts/
│       └── account_001/
│           ├── v1/
│           └── v2/

├── schema/
│   └── account_schema.json
│
├── scripts/
│   ├── v1.py                # Extracts initial configuration from demo transcript
│   ├── v2.py                # Processes onboarding transcript and generate updates
│   ├── update.py            # Merges updates into existing configuration
│   ├── changelogger.py      # Generates changelog between v1 and v2 configs
│   ├── Retell.py            # Generates Retell voice agent specification
│   ├── utils.py             # Shared helper utilities
│   │
│   └── n8n/                 # Optional workflow automation integrations
│
├── mlruns/                  # Experiment logs (if using MLflow)
│
├── requirements.txt
└── README.md
```


### Directory Overview
- **data/** – Raw demo and onboarding call transcripts.
- **outputs/** – Generated configurations, version history, and agent specifications.
- **schema/** – JSON schema defining the structure of the account memo.
- **scripts/** – Core pipeline logic for extraction, updating, merging, and agent generation.
- **mlruns/** – Optional experiment tracking logs.
- **.env** – Environment variables such as API keys or model configs.

## Installation

Clone the repository and install dependencies.

```bash
git clone https://github.com/<your-username>/clara-agent-pipeline
cd clara-agent-pipeline
pip install -r requirements.txt
```

Pull and run the local LLM used for extraction:

```bash
ollama pull qwen2.5:7b-instruct
ollama serve
```

---

## Dataset

Place transcripts in:

```
data/demo_calls/
data/onboarding_calls/
```

Example:

```
data/demo_calls/account_001.txt
data/onboarding_calls/account_001.txt
```

---

## Running the Pipeline

Import the workflow:

```
workflows/n8n_workflow.json
```

Run the demo pipeline to generate **v1 agent configuration**, then run the onboarding pipeline to generate **v2 updates and changelog**.

Outputs are stored in:

```
outputs/accounts/<account_id>/
```


## Design Decisions

- **Chunked transcript parsing** : Demo transcripts can be long, so v1 extraction processes them in chunks and merges the results into a single account memo. This avoids unstable outputs from sending large transcripts to the model.

- **Schema-guided extraction** : Extraction follows a predefined `account_memo_schema.json` so only required operational fields are captured (business hours, routing rules, services, etc.).

- **No hallucinated values** : If a detail is not mentioned in the transcript, it is left blank or added to `questions_or_unknowns`.

- **Demo vs Onboarding separation** : Demo calls generate **v1 agent configurations**, while onboarding calls update them to **v2**, reflecting confirmed operational rules. :contentReference[oaicite:0]{index=0}

- **Patch-based updates** : Onboarding processing extracts only changed fields and merges them into the existing memo instead of regenerating the entire configuration.

- **Versioned outputs** : Each account stores `v1`, `v2`, and a `changelog.json` to track configuration changes.

- **Local LLM usage** : The system uses a local Ollama model (`qwen2.5:7b-instruct`) to keep the pipeline zero-cost and reproducible. I ran it in my RTX 4060 8GB.

- **n8n orchestration** : n8n coordinates transcript ingestion, extraction, update merging, and agent spec generation across accounts.
