<div align="center">
  <h1>🔗 VeriVision</h1>
  <p><strong>A Blockchain-Based Perceptual Hashing Registry for Media Provenance</strong></p>
</div>

<br />

VeriVision is a research-grade, decentralized media provenance system designed to mathematically guarantee the authenticity and origin of digital media. It combines **Deep Learning (ResNet-50)**, **Asymmetric Cryptography (RSA)**, and **High-Performance Vector Search (FAISS)** into a fully encapsulated Web3-style web application.

---

## ✨ Core Features

* 🧠 **Robust Perceptual Hashing:** Uses a fine-tuned ResNet-50 CNN to extract 2048-bit binary perceptual hashes resistant to image manipulation (resizing, compression).
* ⚡ **Instant Verification (FAISS):** Employs Facebook AI Similarity Search (`IndexBinaryFlat`) for sub-millisecond $O(\log n)$ Hamming distance lookups.
* 🔐 **Cloud Identity Persistence:** Integrates with **MongoDB Atlas** to ensure your RSA cryptographic identity and blockchain ledger survive server reboots (crucial for Hugging Face Spaces).
* 🛡️ **Smart Truncation Security:** An "Auto-Healing" protocol that detects database tampering. If a block is hacked, the system automatically truncates the chain to the last known valid state and purges the corruption.
* 📦 **Off-Chain IPFS Simulation:** Stores heavy metadata off-chain while keeping the cryptographic "state-of-truth" securely on the ledger.
* 🚨 **Anti-Plagiarism Protocol:** Actively rejects registrations of media that are identical or highly similar to assets already registered by other authors.

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/VeriVision.git
cd VeriVision
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Model Weights
Place your pre-trained `VeriVision.pth` file directly into the root directory before running the app.

### 4. Setup Cloud Persistence (Optional but Recommended)
1. Create a free **M0 Cluster** at [MongoDB Atlas](https://www.mongodb.com/).
2. Copy `.env.example` to `.env` and fill in your `MONGO_URI`.
3. If you have existing local data, run: `python migrate_to_mongodb.py`

### 5. Launch the DApp
```bash
streamlit run verivision_app.py
```

---

## 🔐 Security & Testing

### Smart Truncation Protocol
VeriVision verifies the entire blockchain integrity on every launch. If any block's hash, index, or linkage is tampered with in the database, the system will:
1. Identify the exact point of the breach.
2. Truncate the chain to the last valid block.
3. Overwrite the corrupted database state with the clean, recovered ledger.

### Simulating an Attack
To test the security system, run the included simulation script:
```bash
python simulate_attack.py
```
Then restart the app to see the "Auto-Healing" protocol in action.

---

## 🌍 Production Deployment (Hugging Face)

To host VeriVision as a live public demo on **Hugging Face Spaces**:
1. Create a **Streamlit Space** and upload your code.
2. **Add Model Weights**: Ensure `VeriVision.pth` is in the root.
3. **Set Secrets**: Go to **Settings > Variables and secrets** and add:
   * **Name**: `MONGO_URI`
   * **Value**: Your full MongoDB connection string (URL-encoded).

---
*Developed as part of a Blockchain and AI academic research initiative.*
