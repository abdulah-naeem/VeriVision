import json
import hashlib
import time
import os
import uuid
from uuid import uuid4
import faiss
import rsa
import numpy as np

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class VeriVisionBlockchain:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.storage_file = os.path.join(self.data_dir, "blockchain_state.json")
        self.whitelist_file = os.path.join(self.data_dir, "authorized_nodes.json")
        self.accounts_file = os.path.join(self.data_dir, "user_accounts.json")
        self.node_key_file = os.path.join(self.data_dir, "node_private_key.pem")
        self.ipfs_dir = os.path.join(self.data_dir, "mock_ipfs")
        os.makedirs(self.ipfs_dir, exist_ok=True)
        
        self.unconfirmed_transactions = []
        self.chain = []
        
        # FAISS Engine
        self.faiss_index = faiss.IndexBinaryFlat(2048)
        self.tx_mapping = []
        self.tx_block_mapping = []
        
        self.load_chain()

    # --- Blockchain Core Logic ---
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        self.save_chain()

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        if self.last_block.hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        
        block.hash = proof
        self.chain.append(block)
        
        # Update FAISS index securely
        for tx in block.transactions:
            bin_arr = np.frombuffer(bytes.fromhex(tx["perceptual_hash"]), dtype=np.uint8)
            self.faiss_index.add(np.expand_dims(bin_arr, 0))
            self.tx_mapping.append(tx)
            self.tx_block_mapping.append(block.index)
            
        self.save_chain()
        return True

    def is_valid_proof(self, block, block_hash):
        return block_hash.startswith('00') and block_hash == block.compute_hash()

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('00'):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def save_chain(self):
        data = [{"index": b.index, "transactions": b.transactions, "timestamp": b.timestamp, 
                 "previous_hash": b.previous_hash, "nonce": b.nonce, "hash": b.hash} for b in self.chain]
        with open(self.storage_file, "w") as f:
            json.dump(data, f)

    def load_chain(self):
        self.faiss_index = faiss.IndexBinaryFlat(2048)
        self.tx_mapping = []
        self.tx_block_mapping = []
        
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                try:
                    data = json.load(f)
                    self.chain = []
                    for b_data in data:
                        b = Block(b_data["index"], b_data["transactions"], b_data["timestamp"], b_data["previous_hash"])
                        b.nonce = b_data["nonce"]
                        b.hash = b_data["hash"]
                        self.chain.append(b)
                        
                        for tx in b.transactions:
                            bin_arr = np.frombuffer(bytes.fromhex(tx["perceptual_hash"]), dtype=np.uint8)
                            self.faiss_index.add(np.expand_dims(bin_arr, 0))
                            self.tx_mapping.append(tx)
                            self.tx_block_mapping.append(b.index)
                except Exception:
                    self.create_genesis_block()
        else:
            self.create_genesis_block()

    # --- Node Identity & Security Logic ---
    def load_node_key(self):
        if os.path.exists(self.node_key_file):
            with open(self.node_key_file, "rb") as f:
                return rsa.PrivateKey.load_pkcs1(f.read())
        return None

    def save_node_key(self, priv):
        with open(self.node_key_file, "wb") as f:
            f.write(priv.save_pkcs1())
        # Secure file permissions (Read/Write only for owner)
        if os.name != 'nt': # Unix systems
            os.chmod(self.node_key_file, 0o600)

    def get_bound_author(self):
        mac_str = str(uuid.getnode())
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, "r") as f:
                accounts = json.load(f)
                return accounts.get(mac_str)
        return None

    def bind_author(self, author_name):
        mac_str = str(uuid.getnode())
        accounts = {}
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, "r") as f:
                accounts = json.load(f)
        accounts[mac_str] = author_name
        with open(self.accounts_file, "w") as f:
            json.dump(accounts, f)

    def authorize_node(self, public_key_hex):
        authorized = []
        if os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, "r") as f:
                authorized = json.load(f)
        if public_key_hex not in authorized:
            authorized.append(public_key_hex)
            with open(self.whitelist_file, "w") as f:
                json.dump(authorized, f)

    def is_node_authorized(self, public_key_hex):
        if os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, "r") as f:
                return public_key_hex in json.load(f)
        return False

    # --- Decentralized Storage (IPFS Mock) ---
    def mock_ipfs_upload(self, metadata):
        metadata_json = json.dumps(metadata, sort_keys=True)
        hash_obj = hashlib.sha256(metadata_json.encode())
        cid = f"Qm{hash_obj.hexdigest()[:44]}"
        with open(os.path.join(self.ipfs_dir, f"{cid}.json"), "w") as f:
            f.write(metadata_json)
        return cid

    def mock_ipfs_retrieve(self, cid):
        path = os.path.join(self.ipfs_dir, f"{cid}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {"error": "Metadata not found on IPFS."}

    # --- Transaction & Verification ---
    def register_media(self, perceptual_hash, ipfs_cid, public_key_hex, signature_hex):
        if not self.is_node_authorized(public_key_hex):
            raise PermissionError("Node is not authorized on the network whitelist.")
            
        payload = f"{perceptual_hash}{ipfs_cid}".encode()
        try:
            pub_key = rsa.PublicKey.load_pkcs1(bytes.fromhex(public_key_hex))
            rsa.verify(payload, bytes.fromhex(signature_hex), pub_key)
        except Exception:
            raise ValueError("Cryptographic Signature Verification Failed!")

        transaction = {
            "media_id": str(uuid4()),
            "perceptual_hash": perceptual_hash,
            "ipfs_cid": ipfs_cid,
            "public_key": public_key_hex,
            "signature": signature_hex,
            "timestamp": time.time()
        }
        self.unconfirmed_transactions.append(transaction)
        return transaction["media_id"]

    def verify_media_faiss(self, query_hash_hex):
        if self.faiss_index.ntotal == 0:
            return None, float('inf'), None
            
        bin_arr = np.frombuffer(bytes.fromhex(query_hash_hex), dtype=np.uint8)
        D, I = self.faiss_index.search(np.expand_dims(bin_arr, 0), k=1)
        
        dist = int(D[0][0])
        idx = int(I[0][0])
        
        if idx != -1 and idx < len(self.tx_mapping):
            return self.tx_mapping[idx], dist, self.tx_block_mapping[idx]
        return None, float('inf'), None
