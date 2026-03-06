import mlflow
import json

from pathlib import Path


def main():
    mlflow.set_experiment("clara_pipeline")
    with mlflow.start_run(run_name="changelogger"):
        accounts_dir=Path("outputs/accounts")
        for account_dir in accounts_dir.iterdir():

            v1=json.loads((account_dir/"v1/account_memo.json").read_text())
            v2=json.loads((account_dir/"v2/account_memo.json").read_text())

            changes=[]

            for key in v2:
                if v1.get(key)!=v2.get(key): changes.append(key)
            result={"updated_fields":changes}
            (account_dir/"v2/changes.json").write_text(json.dumps(result, indent=2))

            mlflow.log_param("account",account_dir.name)
            mlflow.log_dict(result,f"changes_{account_dir.name}.json")

            print("changes generated:",account_dir.name)

if __name__=="__main__":
    main()