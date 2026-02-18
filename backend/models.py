import torch
import torch.nn as nn
import xgboost as xgb
import numpy as np
import logging

logger = logging.getLogger(__name__)

class LSTMModel(nn.Module):
    """LSTM-based model for price prediction."""
    
    def __init__(self, input_dim: int, hidden_dim: int = 64, num_layers: int = 2, output_dim: int = 1):
        super(LSTMModel, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

class XGBoostModel:
    """XGBoost-based model for signal classification."""
    
    def __init__(self, params=None):
        self.params = params or {
            'objective': 'binary:logistic',
            'max_depth': 6,
            'eta': 0.1,
            'eval_metric': 'logloss'
        }
        self.model = None

    def train(self, X_train, y_train):
        dtrain = xgb.DMatrix(X_train, label=y_train)
        self.model = xgb.train(self.params, dtrain, num_boost_round=100)

    def predict(self, X):
        dtest = xgb.DMatrix(X)
        return self.model.predict(dtest)

class ModelFactory:
    """Factory for creating models."""
    
    @staticmethod
    def get_model(model_type: str, **kwargs):
        if model_type == 'lstm':
            return LSTMModel(**kwargs)
        elif model_type == 'xgboost':
            return XGBoostModel(**kwargs)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
