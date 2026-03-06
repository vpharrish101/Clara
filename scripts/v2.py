import mlflow
import json

from pathlib import Path

mlflow.set_experiment("clara_pipeline_v2")

def merge(base,patch):
    for k,v in patch.items():
        if isinstance(v, dict) and k in base: merge(base[k],v)
        else: base[k]=v
    return base


def main():

    with mlflow.start_run(run_name="v2_merge"):
        accounts_dir=Path("outputs/accounts")
        for account_dir in accounts_dir.iterdir():

            v1_path=account_dir/"v1/account_memo.json"
            update_path=account_dir/"v2/updates.json"

            if not v1_path.exists() or not update_path.exists(): continue

            v1=json.loads(v1_path.read_text())
            updates=json.loads(update_path.read_text())

            v2=merge(v1,updates)

            v2["questions_or_unknowns"]=[]
            out=account_dir/"v2/account_memo.json"
            out.write_text(json.dumps(v2,indent=2))

            mlflow.log_param("account",account_dir.name)
            mlflow.log_dict(v2,f"v2_config_{account_dir.name}.json")

if __name__=="__main__":
    main()