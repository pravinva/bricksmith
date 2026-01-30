"""MLflow tracking integration for Nano Banana Pro."""

import json
from pathlib import Path
from typing import Any, Optional

import mlflow
from mlflow.entities import ViewType

from .config import MLflowConfig
from .models import DiagramSpec, EvaluationScores


class MLflowTracker:
    """MLflow tracking manager for experiments and runs."""

    def __init__(self, config: MLflowConfig):
        """Initialize MLflow tracker.

        Args:
            config: MLflow configuration
        """
        self.config = config
        self._experiment_id: Optional[str] = None
        self._current_run_id: Optional[str] = None

    def initialize(self, experiment_name: Optional[str] = None) -> None:
        """Initialize MLflow tracking.

        Sets tracking URI and creates/gets experiment.

        Args:
            experiment_name: Optional experiment name override. If provided,
                           uses this instead of config.experiment_name.
                           Useful for grouping runs by prompt file.
        """
        # Set tracking URI
        mlflow.set_tracking_uri(self.config.tracking_uri)

        # Use provided experiment name or fall back to config
        exp_name = experiment_name or self.config.experiment_name

        # Create or get experiment
        try:
            experiment = mlflow.get_experiment_by_name(exp_name)
            if experiment is None:
                self._experiment_id = mlflow.create_experiment(
                    exp_name,
                    artifact_location=self.config.artifact_location,
                )
            else:
                self._experiment_id = experiment.experiment_id
        except Exception as e:
            raise Exception(f"Failed to initialize MLflow experiment: {e}")

        # Set active experiment
        mlflow.set_experiment(exp_name)

    def start_run(
        self,
        run_name: Optional[str] = None,
        tags: Optional[dict[str, str]] = None,
    ) -> str:
        """Start a new MLflow run.

        Args:
            run_name: Optional run name
            tags: Optional tags dictionary

        Returns:
            Run ID

        Raises:
            Exception: If experiment not initialized
        """
        if self._experiment_id is None:
            raise Exception("Experiment not initialized. Call initialize() first.")

        run = mlflow.start_run(run_name=run_name, tags=tags)
        self._current_run_id = run.info.run_id
        return self._current_run_id

    def log_parameters(self, params: dict[str, Any]) -> None:
        """Log parameters to current run.

        Args:
            params: Dictionary of parameters to log
        """
        for key, value in params.items():
            # Convert complex types to strings
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            mlflow.log_param(key, value)

    def log_metrics(self, metrics: dict[str, float]) -> None:
        """Log metrics to current run.

        Args:
            metrics: Dictionary of metrics to log
        """
        mlflow.log_metrics(metrics)

    def log_prompt(self, prompt_text: str, filename: str = "prompt.txt") -> None:
        """Log prompt as text artifact.

        Args:
            prompt_text: Complete prompt text
            filename: Artifact filename
        """
        # Save to temp file and log
        temp_file = Path(f"/tmp/{self._current_run_id}_{filename}")
        temp_file.write_text(prompt_text)
        mlflow.log_artifact(str(temp_file), artifact_path="prompts")
        temp_file.unlink()  # Clean up

    def log_diagram_spec(self, spec: DiagramSpec, filename: str = "diagram_spec.yaml") -> None:
        """Log diagram spec as YAML artifact.

        Args:
            spec: Diagram specification
            filename: Artifact filename
        """
        temp_file = Path(f"/tmp/{self._current_run_id}_{filename}")
        spec.to_yaml(temp_file)
        mlflow.log_artifact(str(temp_file), artifact_path="specs")
        temp_file.unlink()

    def log_generation_config(
        self, config: dict[str, Any], filename: str = "generation_config.json"
    ) -> None:
        """Log generation config as JSON artifact.

        Args:
            config: Generation configuration
            filename: Artifact filename
        """
        temp_file = Path(f"/tmp/{self._current_run_id}_{filename}")
        temp_file.write_text(json.dumps(config, indent=2))
        mlflow.log_artifact(str(temp_file), artifact_path="configs")
        temp_file.unlink()

    def log_output_image(self, image_path: Path) -> None:
        """Log generated image for inline preview in MLflow UI.

        Uses mlflow.log_image() for better visualization in the MLflow UI,
        allowing side-by-side comparison of diagram outputs across runs.

        Args:
            image_path: Path to image file
        """
        from PIL import Image

        # Load image and log with log_image for inline preview
        img = Image.open(image_path)
        # Use artifact_path to organize under outputs folder
        mlflow.log_image(img, artifact_file=f"outputs/{image_path.name}")

    def log_evaluation(self, scores: EvaluationScores) -> None:
        """Log evaluation scores as metrics and artifact.

        Args:
            scores: Evaluation scores
        """
        # Log individual scores as metrics
        metrics = {
            "logo_fidelity_score": float(scores.logo_fidelity_score),
            "layout_clarity_score": float(scores.layout_clarity_score),
            "text_legibility_score": float(scores.text_legibility_score),
            "constraint_compliance_score": float(scores.constraint_compliance_score),
            "overall_score": scores.overall_score,
        }
        mlflow.log_metrics(metrics)

        # Log full evaluation as JSON artifact
        temp_file = Path(f"/tmp/{self._current_run_id}_evaluation.json")
        temp_file.write_text(json.dumps(scores.to_dict(), indent=2))
        mlflow.log_artifact(str(temp_file), artifact_path="evaluations")
        temp_file.unlink()

        # Log notes as tag if present
        if scores.notes:
            mlflow.set_tag("evaluation_notes", scores.notes[:250])  # Truncate if too long

    def end_run(self, status: str = "FINISHED") -> None:
        """End the current run.

        Args:
            status: Run status (FINISHED, FAILED, KILLED)
        """
        mlflow.end_run(status=status)
        self._current_run_id = None

    def get_run_info(self, run_id: str) -> dict[str, Any]:
        """Get information about a specific run.

        Args:
            run_id: MLflow run ID

        Returns:
            Dictionary with run information
        """
        run = mlflow.get_run(run_id)

        return {
            "run_id": run.info.run_id,
            "run_name": run.info.run_name,
            "status": run.info.status,
            "start_time": run.info.start_time,
            "end_time": run.info.end_time,
            "parameters": run.data.params,
            "metrics": run.data.metrics,
            "tags": run.data.tags,
            "artifact_uri": run.info.artifact_uri,
        }

    def list_runs(
        self,
        filter_string: Optional[str] = None,
        max_results: int = 100,
        order_by: list[str] = None,
    ) -> list[dict[str, Any]]:
        """List runs in the experiment.

        Args:
            filter_string: Optional MLflow filter string
            max_results: Maximum number of runs to return
            order_by: Optional list of order by clauses

        Returns:
            List of run dictionaries
        """
        if self._experiment_id is None:
            raise Exception("Experiment not initialized. Call initialize() first.")

        if order_by is None:
            order_by = ["start_time DESC"]

        runs = mlflow.search_runs(
            experiment_ids=[self._experiment_id],
            filter_string=filter_string,
            max_results=max_results,
            order_by=order_by,
            run_view_type=ViewType.ACTIVE_ONLY,
        )

        # Convert DataFrame to list of dicts
        return runs.to_dict("records") if not runs.empty else []

    def get_artifact_path(self, run_id: str, artifact_path: str) -> str:
        """Get local path to a specific artifact.

        Args:
            run_id: MLflow run ID
            artifact_path: Relative artifact path

        Returns:
            Local file path to artifact
        """
        client = mlflow.tracking.MlflowClient()
        artifact_uri = client.get_run(run_id).info.artifact_uri
        return f"{artifact_uri}/{artifact_path}"

    @property
    def current_run_id(self) -> Optional[str]:
        """Get current run ID."""
        return self._current_run_id

    @property
    def experiment_id(self) -> Optional[str]:
        """Get experiment ID."""
        return self._experiment_id
