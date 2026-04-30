<div align="center">
  <h1>🔗 VeriVision</h1>
  <p><strong>A Blockchain-Based Perceptual Hashing Registry for Media Provenance</strong></p>
</div>

<br />

VeriVision is a research-grade, decentralized media provenance system designed to mathematically guarantee the authenticity and origin of digital media. It combines **Deep Learning (ResNet-50)**, **Asymmetric Cryptography (RSA)**, and **High-Performance Vector Search (FAISS)** into a fully encapsulated Web3-style web application.

---

## ✨ Core Features

* 🧠 **Robust Perceptual Hashing:** Uses a fine-tuned ResNet-50 CNN to extract 2048-bit binary perceptual hashes that are resistant to benign image manipulation (resizing, compression).
* ⚡ **Instant Verification (FAISS):** Replaces traditional linear blockchain querying with Facebook AI Similarity Search (`IndexBinaryFlat`), enabling sub-millisecond $O(\log n)$ Hamming distance lookups.
* 🔐 **Hardware Enclave Security:** Simulates a hardware-locked camera node by generating and permanently binding an RSA-512 cryptographic identity (`node_private_key.pem`) to the local machine.
* 📦 **Off-Chain IPFS Simulation:** Solves blockchain data bloat by storing actual metadata off-chain while keeping the cryptographic state-of-truth securely on the ledger.
* 🚨 **Anti-Plagiarism Protocol:** Actively rejects registrations of media that are identical or highly similar to assets already registered on the network by other authors.

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/VeriVision.git
cd VeriVision
```

### 2. Install Dependencies
This project requires Python 3.8+ and uses PyTorch.
```bash
pip install -r requirements.txt
```

### 3. Add Model Weights
Because deep learning weights exceed GitHub's standard file limits, the `VeriVision.pth` file is not included in this repository. 
* Place your pre-trained `VeriVision.pth` file directly into the root `VeriVision` directory before running the app.

### 4. Launch the Decentralized App (DApp)
```bash
streamlit run verivision_app.py
```

---

## 📖 How to Use the System

1. **Initialize your Node:** Navigate to the **"🔐 Identity & Security"** tab. Provide an Author Name and click "Initialize". This simulates a secure camera node generating its private hardware key and registering itself on the network.
2. **Register Media:** Go to the **"📝 Register Media"** tab. Upload a photograph. The AI will extract its perceptual hash, sign the payload with your node's RSA Private Key, and mine it into the local blockchain.
3. **Verify Authenticity:** Go to the **"🔍 Verify Media"** tab. Upload any image (even one that has been slightly compressed). The FAISS engine will locate the closest match. If the signature is mathematically valid and the Hamming distance is below the tolerance threshold, the media is confirmed as **Authentic**.

---

## 🌍 Deployment Options

To deploy this application publicly for your research presentation, **Hugging Face Spaces** is highly recommended:
1. Create a free account at [Hugging Face](https://huggingface.co/).
2. Create a new **Space** and select **Streamlit** as the SDK.
3. Upload the 5 core files: `verivision_app.py`, `verivision_ai.py`, `verivision_blockchain.py`, `requirements.txt`, and your `VeriVision.pth`.
4. Hugging Face will automatically build the environment, install PyTorch, and host your Web3 dashboard live on the internet!

---
*Developed as part of a Blockchain and AI academic research initiative.*
