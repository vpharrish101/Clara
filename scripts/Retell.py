import mlflow
import json

from pathlib import Path


def main():
    mlflow.set_experiment("clara_pipeline")
    with mlflow.start_run(run_name="retell_agent_generation"):

        accounts_dir=Path("outputs/accounts")
        for account_dir in accounts_dir.iterdir():
            memo=json.loads((account_dir / "v2/account_memo.json").read_text())

            prompt=f"""
    You are Clara, AI receptionist for {memo['company_name']}.

    Location:
    {memo['office_address']}

    Services:
    {", ".join(x["description"] if isinstance(x,dict) else x for x in memo["services_supported"])}

    Emergency situations:
    {", ".join(x["description"] if isinstance(x,dict) else x for x in memo["emergency_definition"])}
    """

            spec={
                "agent_name": f"{account_dir.name}_agent",
                "voice_style": "professional",
                "version": "v2",
                "system_prompt": prompt,
                "variables": memo,
                "tools": [
                    "create_service_request",
                    "log_call_summary",
                    "attempt_call_transfer"
                ],
                "call_transfer_protocol": memo["call_transfer_rules"]
            }

            out=account_dir/"v2/agent_spec.json"
            out.write_text(json.dumps(spec,indent=2))

            mlflow.log_param("agent_account",account_dir.name)
            mlflow.log_dict(spec,f"agent_{account_dir.name}.json")

            print("agent spec generated:",account_dir.name)

if __name__=="__main__":
    main()