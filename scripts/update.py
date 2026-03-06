import mlflow
import json

from pathlib import Path
from utils import run_llm, extract_json




def main():
    onboard_dir=Path("data/onboarding_calls")
    mlflow.set_experiment("clara_pipeline")
    with mlflow.start_run(run_name="update_extraction"):
        
        for transcript_file in onboard_dir.glob("*.txt"):

            account=transcript_file.stem
            v1_path=Path(f"outputs/accounts/{account}/v1/account_memo.json")

            if not v1_path.exists(): continue

            v1=v1_path.read_text()
            transcript=transcript_file.read_text()

            prompt=f"""
    Given an existing configuration and onboarding transcript,
    return ONLY fields that must change.

    Existing config:
    {v1}

    Transcript:
    {transcript}

    Return JSON only.
    """

            response=run_llm(prompt)
            updates=extract_json(response)

            out=Path(f"outputs/accounts/{account}/v2/updates.json")
            out.parent.mkdir(parents=True,exist_ok=True)
            out.write_text(json.dumps(updates,indent=2))

            mlflow.log_param("update_account",account)
            mlflow.log_dict(updates,f"updates_{account}.json")

if __name__=="__main__":
    main()