import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
import numpy as np

class VeriVisionAI:
    def __init__(self, model_path='best_model.pth'):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.feature_extractor = self._load_model(model_path)
        self.val_tf = self._get_transforms()

    def _load_model(self, model_path):
        model = models.resnet50(weights=None)
        model.fc = nn.Sequential(nn.Dropout(0.3), nn.Linear(model.fc.in_features, 2))
        try:
            model.load_state_dict(torch.load(model_path, map_location=self.device))
        except Exception as e:
            raise RuntimeError(f"Failed to load ResNet model weights from {model_path}. Error: {e}")
        
        feature_extractor = nn.Sequential(*list(model.children())[:-1]).to(self.device).eval()
        return feature_extractor

    def _get_transforms(self):
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def extract_perceptual_hash(self, image):
        """
        Extracts a robust 2048-bit perceptual hash from an image using the loaded CNN.
        Returns the hash as a hex string.
        """
        img = image.convert("RGB")
        img_t = self.val_tf(img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            if torch.cuda.is_available():
                with torch.amp.autocast('cuda'):
                    feat = self.feature_extractor(img_t)
            else:
                feat = self.feature_extractor(img_t)
                
            feat = feat.float().view(feat.size(0), -1).cpu().numpy()[0]
        
        # L2 Normalize
        norm = np.linalg.norm(feat) + 1e-10
        feat = feat / norm
        
        # Binarize and pack to hex
        bin_arr = (feat > 0).astype(np.uint8)
        byte_arr = np.packbits(bin_arr)
        return byte_arr.tobytes().hex()
