import os
import mlflow
from mlflow.tracking import MlflowClient

# Example pyfunc wrapper for Hugging Face Seq2Seq models
class TransformersHFWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        import transformers
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        # 'hf_model' is the local path where mlflow saved the HF files as an artifact
        artifact_path = context.artifacts.get("hf_model")
        self.tokenizer = AutoTokenizer.from_pretrained(artifact_path, use_fast=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(artifact_path, device_map="auto")

    def predict(self, context, model_input):
        # model_input: a pandas.DataFrame or a list of strings
        import pandas as pd
        texts = None
        if isinstance(model_input, pd.DataFrame):
            # expect a column 'text' with input strings
            if "text" in model_input.columns:
                texts = model_input["text"].astype(str).tolist()
            else:
                texts = model_input.iloc[:,0].astype(str).tolist()
        elif isinstance(model_input, (list, tuple)):
            texts = list(model_input)
        else:
            texts = [str(model_input)]
        # Tokenize and generate
        inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        gen = self.model.generate(**inputs, max_new_tokens=128)
        outs = [self.tokenizer.decode(g, skip_special_tokens=True) for g in gen]
        return pd.DataFrame({"prediction": outs})

def log_and_register_pyfunc(model_dir: str, model_name: str, conda_env: dict=None, run_name: str="hf-log-run") -> str:
    # \"\"\"Log local HF model_dir (a folder from save_pretrained) as an MLflow pyfunc and register it.
    # Returns the registered model version uri (models:/...)
    # \"\"\"
    mlflow.set_experiment("hf-mlflow-experiments")
    with mlflow.start_run(run_name=run_name) as run:
        # Log the HF model directory as an artifact under the run (artifact_path 'hf_model')
        mlflow.log_artifacts(model_dir, artifact_path="hf_model")
        # Log pyfunc model that uses the saved artifact
        mlflow.pyfunc.log_model(
            artifact_path="pyfunc_model",
            python_model=TransformersHFWrapper(),
            artifacts={"hf_model": model_dir},
            conda_env=conda_env,
            registered_model_name=model_name
        )
        model_uri = f"models:/{model_name}/latest"
        return model_uri

def register_s3_model_version(s3_uri: str, model_name: str) -> str:
    # \"\"\"Register an already-uploaded S3 URI as a new version in MLflow Model Registry.
    # s3_uri must be of the form s3://bucket/path/to/model_dir
    # \"\"\"
    client = MlflowClient()
    try:
        client.create_registered_model(model_name)
    except Exception as e:
        # model may already exist
        pass
    result = client.create_model_version(name=model_name, source=s3_uri, run_id=None)
    # Optionally transition to a stage:
    client.transition_model_version_stage(name=model_name, version=result.version, stage="Staging")
    return f"models:/{model_name}/{result.version}"
