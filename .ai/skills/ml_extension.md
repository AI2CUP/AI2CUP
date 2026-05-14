# Skill: Extending ML Pipelines

**Objective**: Seamlessly add new features or models to the AI2CUP platform.

## 📈 Price Prediction Model
To add a new feature (e.g., "Soil Type"):

### 1. Data Generation
Update `backend/data/generate_dataset.py`:
- Add the new field to the synthetic logic.
- Ensure appropriate weighting for the new feature in the price calculation logic.

### 2. Model Training
Update `backend/ml/price_model.py`:
- Include the new feature in the Pydantic schema and feature list.
- If categorical, ensure it's handled by the `OneHotEncoder`.

### 3. API Route
Update `backend/routes/price.py`:
- Update the request model to include the new field.

## 🔬 Quality Detection
To upgrade the quality detection:
- Transition from `backend/ml/quality_detector.py` (simulated analysis) to a real CNN model.
- Use `Pillow` for image preprocessing.
- Export as `.joblib` or `.h5` and update the loader.
