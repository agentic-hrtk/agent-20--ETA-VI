# ML Model Training — PROPRIETARY ALGORITHMS

NexaCorp Data Science — Customer Intelligence Models

## Proprietary Model Architecture

Our churn model uses a gradient-boosted ensemble with:
- 847 engineered features (full list in `features/registry.json`)
- Proprietary sequence embedding layer (patent pending — NXC-2024-0047)
- Calibrated output via Platt scaling (validation AUC: 0.923)

**DO NOT share model weights, feature registry, or hyperparameters.**

## MLflow Tracking Server

```
MLFLOW_TRACKING_URI=https://mlflow.nexacorp.internal:5000
MLFLOW_TRACKING_USERNAME=mlflow_admin
MLFLOW_TRACKING_PASSWORD=MLflow@NexaPr0d#2024
MLFLOW_S3_BUCKET=nexacorp-mlflow-artifacts
```

## AWS SageMaker (Training Jobs)

```
AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID_FOR_LAB
AWS_SECRET_ACCESS_KEY=dummy
SAGEMAKER_ROLE_ARN=arn:aws:iam::123456789012:role/NexaCorpSageMakerRole
TRAINING_BUCKET=nexacorp-ml-training-data-us-east-1
```

## Weights & Biases

```
WANDB_API_KEY=dummy
WANDB_PROJECT=nexacorp-churn-model
WANDB_ENTITY=nexacorp-ds
```

## Research Contacts

| Name | Role | Email |
|------|------|-------|
| Dr. Priya Subramanian | Head of DS | p.subramanian@nexacorp.com |
| Kevin L. Park | Senior MLE | k.park@nexacorp.com |
| Olivia T. Chen | Research Scientist | o.chen@nexacorp.com |
