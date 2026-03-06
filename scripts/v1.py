import mlflow
import json

from pathlib import Path
from utils import run_llm,extract_json,demo_transcripts

SCHEMA_PATH="schema/account_schema.json"

demo_dir=Path("data/demo_calls")
schema=Path(SCHEMA_PATH).read_text()

mlflow.set_experiment("clara_pipeline_v1")

def detect_integrations(text):
    integrations=[]
    lower=text.lower()
    if "jobber" in lower:
        integrations.append("Uses Jobber CRM")
    return integrations


def main():

    with mlflow.start_run(run_name="v1_generation"):

        for transcript_file in demo_transcripts():
            account=transcript_file.stem
            transcript=transcript_file.read_text()

            prompt = f"""
    Populate the schema using the transcript.

    Rules:
    - Do not hallucinate
    - Fill only explicit facts
    - Leave unknown fields empty
    - Add missing info to questions_or_unknowns

    Schema:
    {schema}

    Transcript:
    {transcript}

    Return JSON only.
    """

            result=run_llm(prompt)
            data=extract_json(result)
            integrations=detect_integrations(transcript)

            if integrations:
                data["integration_constraints"]=integrations

            output=Path(f"outputs/accounts/{account}/v1/account_memo.json")
            output.parent.mkdir(parents=True,exist_ok=True)
            output.write_text(json.dumps(data,indent=2))

            mlflow.log_param("account",account)
            mlflow.log_dict(data,f"v1_config_{account}.json")

            print("v1 created:",account)

if __name__=="__main__":
    main()