
import joblib
import pandas as pd

class CostOfLivingForecaster:
    def __init__(self):
        """
        Load the trained model
        """
        self.model = joblib.load("models/cost_of_living_forecaster.pkl")
        
    def _get_required_feature_columns(self):
        return [str(col) for col in self.model.feature_names_in_]
    
    def _prepare_features(self, year, month, area, encoder_columns):
        """
        Prepare input data for prediction
        
        Args:
            year (int): _description_
            month (int): _description_
            area (str): _description_
            encoder_columns (list): A list of all one-hot-encoded area columns (from training)
        """
        
        # Create a base dataframe with the required columns
        data = pd.DataFrame([[year, month]], columns=["Year", "Month"])
        
        # One-hot encode the Area column
        for col in encoder_columns:
            data[col] = 0 # Initialize all area columns with 0
            
        area_col = f"Area_{area}"
        
        if area_col in encoder_columns:
            data[area_col] = 1 # Set the correct area to 1
        else:
            raise ValueError(f"Unknown area: {area}. Expected one of {encoder_columns}")
        
        return data
    
    def predict(self, year, area):
        """
        Make predictions given the input values
        Args:
            year (int): _description_
            area (int): _description_
        """
        try:
            features = self._prepare_features(year, 6, area, self._get_required_feature_columns())
            
            predictions = self.model.predict(features)[0].tolist()
           
            return {
                "predicted_total_cost": round(sum(predictions), 2),
                "breakdown": {
                    "rent": round(predictions[0], 2),
                    "food": round(predictions[1], 2),
                    "transportation": round(predictions[2], 2),
                    "utilities": round(predictions[3], 2),
                    "misc": round(predictions[4], 2),
                }
            }
        except Exception as e:
            return {"error": str(e)}