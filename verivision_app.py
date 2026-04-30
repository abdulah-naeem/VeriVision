import streamlit as st
from PIL import Image
import time
import rsa

from verivision_blockchain import VeriVisionBlockchain
from verivision_ai import VeriVisionAI

# ==========================================
# Streamlit UI Configuration
# ==========================================
st.set_page_config(page_title="VeriVision", page_icon="🔗", layout="wide")

# Hide Streamlit UI elements and inject premium minimalist styling
premium_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Minimalist Deep Slate Background */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }

    /* Clean Headers */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    /* Tabs (Fixed Overflow) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        padding: 4px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 10px !important;
        padding-bottom: 10px !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
        white-space: nowrap;
    }
    .stTabs [aria-selected="true"] {
        color: #10B981 !important; /* Professional Emerald Accent */
        background-color: rgba(16, 185, 129, 0.05) !important;
        border-radius: 6px;
    }
    .stTabs [aria-selected="true"] [data-testid="stMarkdownContainer"] p {
        color: #10B981 !important;
        font-weight: 600;
    }

    /* Professional Buttons */
    .stButton > button, .stFormSubmitButton > button {
        background-color: #10B981 !important;
        color: #022C22 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: background-color 0.2s ease !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background-color: #059669 !important;
        color: white !important;
    }

    /* Sleek Alerts */
    .stAlert {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border-radius: 8px !important;
        border-left: 4px solid #10B981 !important;
        color: #F1F5F9 !important;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        color: white !important;
        border-radius: 6px;
    }
    .stTextInput > div > div > input:focus {
        border: 1px solid #10B981 !important;
        box-shadow: none !important;
    }

    /* Code Blocks */
    .stCodeBlock {
        border-radius: 6px !important;
        border: 1px solid #334155 !important;
        background-color: #0F172A !important;
    }

    /* Hide defaults and disable selection */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    body {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    </style>
"""
st.markdown(premium_css, unsafe_allow_html=True)

# Inject Javascript to disable context menu and DevTools shortcuts
st.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('contextmenu', event => event.preventDefault());
    doc.onkeydown = function(e) {
        if(e.keyCode == 123) { return false; } // Disable F12
        if(e.ctrlKey && e.shiftKey && e.keyCode == 73) { return false; } // Disable Ctrl+Shift+I
        if(e.ctrlKey && e.shiftKey && e.keyCode == 74) { return false; } // Disable Ctrl+Shift+J
        if(e.ctrlKey && e.keyCode == 85) { return false; } // Disable Ctrl+U
    }
    </script>
    """
)

st.title("🔗 VeriVision")
st.subheader("Blockchain-Based Perceptual Hashing Registry for Media Provenance")

@st.cache_resource
def init_system():
    return VeriVisionAI(), VeriVisionBlockchain(data_dir="data")

with st.spinner("Initializing AI and Blockchain Engines..."):
    ai_engine, registry = init_system()

# Hardware Enclave Auto-Login
node_priv = registry.load_node_key()
if node_priv:
    node_pub = rsa.PublicKey(node_priv.n, node_priv.e)
    st.session_state.public_key = node_pub
    st.session_state.private_key = node_priv
else:
    st.session_state.public_key = None
    st.session_state.private_key = None

tabs = st.tabs(["🔐 Identity & Security", "📝 Register Media", "📂 My Media", "🔍 Verify Media", "📦 View Blockchain"])

# --- TAB 1: Security & Identity ---
with tabs[0]:
    st.header("Hardware Node Enclave (Security)")
    st.write("VeriVision nodes (like a journalist's secure camera) do not use passwords. They use an internal **Hardware Enclave** that generates and stores a single cryptographic Private Key bounded to the device.")
    
    bound_author = registry.get_bound_author()
    
    if st.session_state.public_key and bound_author:
        st.success(f"✅ Hardware Node Authenticated! Operating as: **{bound_author}**")
        st.write("**Node Public Key (Your Decentralized ID - Visible on Blockchain):**")
        st.code(st.session_state.public_key.save_pkcs1().hex(), language="text")
        st.info("Your Private Key is securely locked in the hardware enclave (`data/node_private_key.pem`) and cannot be manually exported or logged out. This guarantees 100% node integrity.")
    else:
        st.warning("⚠️ UNINITIALIZED HARDWARE NODE")
        st.write("This device has not been initialized on the VeriVision network.")
        
        with st.form("init_node"):
            author_input = st.text_input("Set Author/Node Identity (Permanent)")
            init_submit = st.form_submit_button("Initialize Node & Generate Keys")
            
            if init_submit:
                if not author_input.strip():
                    st.error("Please provide an identity for this node.")
                else:
                    with st.spinner("Initializing Hardware Enclave..."):
                        registry.bind_author(author_input.strip())
                        pub, priv = rsa.newkeys(512)
                        registry.save_node_key(priv)
                        registry.authorize_node(pub.save_pkcs1().hex())
                        st.success("Node Initialized!")
                        st.rerun()

# --- TAB 2: Register Media ---
with tabs[1]:
    st.header("Register New Media")
    
    if not st.session_state.public_key:
        st.error("You must initialize this Hardware Node in the 'Identity & Security' tab first!")
    else:
        uploaded_file = st.file_uploader("Upload Image to Register", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Media", width=400)
            
            with st.form("register_form"):
                author = st.text_input("Author Name (Hardware Locked)", value=bound_author, disabled=True)
                device_type = st.text_input("Device Model", value="VeriVision Node v1.0")
                location = st.text_input("Location", value="New York, USA")
                
                submitted = st.form_submit_button("Sign & Register to Blockchain")
                if submitted:
                    with st.spinner("Extracting Perceptual Hash..."):
                        phash = ai_engine.extract_perceptual_hash(image)
                    
                    # Anti-Plagiarism / Duplicate Check
                    best_match, min_dist, _ = registry.verify_media_faiss(phash)
                    DUPLICATE_THRESHOLD = 75 # Matches the default Verification tolerance
                    
                    if min_dist <= DUPLICATE_THRESHOLD and best_match:
                        st.error(f"🚨 **PLAGIARISM REJECTED:** This exact media (or a highly manipulated version of it) is ALREADY registered on the blockchain! (Hamming Distance: {min_dist} bits). You cannot claim provenance over an existing asset.")
                    else:
                        metadata = {"filename": uploaded_file.name, "author": author, "device": device_type, "location": location}
                        ipfs_cid = registry.mock_ipfs_upload(metadata)
                        
                        payload = f"{phash}{ipfs_cid}".encode()
                        signature = rsa.sign(payload, st.session_state.private_key, 'SHA-256')
                        sig_hex = signature.hex()
                        pub_hex = st.session_state.public_key.save_pkcs1().hex()
                        
                        with st.spinner("Verifying Signature & Broadcasting to Blockchain..."):
                            try:
                                media_id = registry.register_media(phash, ipfs_cid, pub_hex, sig_hex)
                                block_idx = registry.mine()
                                st.success(f"Media Successfully Signed & Registered! Transaction ID: {media_id}")
                                st.info(f"Metadata securely stored off-chain at IPFS CID: ipfs://{ipfs_cid}")
                                st.info(f"Immutable Hash Log added to Block #{block_idx}")
                            except Exception as e:
                                st.error(str(e))

# --- TAB 3: My Media ---
with tabs[2]:
    st.header("My Registered Media")
    if not st.session_state.public_key:
        st.warning("⚠️ Please initialize your node to view registered media.")
    else:
        pub_hex = st.session_state.public_key.save_pkcs1().hex()
        user_txs = []
        for block in registry.chain:
            for tx in block.transactions:
                if tx.get("public_key") == pub_hex:
                    user_txs.append((block.index, tx))
                    
        if not user_txs:
            st.info("You have not registered any media yet on this node.")
        else:
            st.write(f"You have securely registered **{len(user_txs)}** media assets on the blockchain.")
            for block_idx, tx in reversed(user_txs):
                metadata = registry.mock_ipfs_retrieve(tx["ipfs_cid"])
                filename = metadata.get("filename", "Unknown File") if isinstance(metadata, dict) else "Unknown File"
                
                with st.expander(f"🖼️ {filename} (Mined in Block #{block_idx})"):
                    st.write(f"**Registration Date:** {time.ctime(tx['timestamp'])}")
                    st.write(f"**Transaction ID:** `{tx['media_id']}`")
                    st.write(f"**IPFS CID:** `ipfs://{tx['ipfs_cid']}`")
                    st.write("**Decrypted Metadata:**")
                    st.json(metadata)

# --- TAB 4: Verify Media ---
with tabs[3]:
    st.header("Verify Media Authenticity")
    verify_file = st.file_uploader("Upload Image to Verify", type=["png", "jpg", "jpeg"], key="verify")
    THRESHOLD = st.slider("Hamming Distance Threshold (Robustness to edits)", 0, 500, 75)
    
    if verify_file is not None:
        image = Image.open(verify_file)
        st.image(image, caption="Media for Verification", width=400)
        
        if st.button("Verify Now"):
            with st.spinner("Computing Perceptual Hash..."):
                query_hash = ai_engine.extract_perceptual_hash(image)
            
            best_match, min_dist, best_block = registry.verify_media_faiss(query_hash)
                        
            if min_dist <= THRESHOLD and best_match:
                st.success("✅ **Media is AUTHENTIC.** Found matching record in immutable registry using FAISS.")
                st.write(f"**Hamming Distance:** {min_dist} bits (Threshold: {THRESHOLD})")
                
                payload = f"{best_match['perceptual_hash']}{best_match['ipfs_cid']}".encode()
                pub_key = rsa.PublicKey.load_pkcs1(bytes.fromhex(best_match["public_key"]))
                
                try:
                    rsa.verify(payload, bytes.fromhex(best_match["signature"]), pub_key)
                    st.info("🔐 **Cryptographic Signature VERIFIED.** The author's identity is mathematically proven and untampered.")
                except rsa.VerificationError:
                    st.error("🚨 **SECURITY ALERT:** The cryptographic signature on this block is invalid! Data may have been tampered with.")
                
                metadata = registry.mock_ipfs_retrieve(best_match["ipfs_cid"])
                st.subheader("Provenance History (From IPFS & Blockchain)")
                st.json({
                    "Block Index": best_block,
                    "Media ID": best_match["media_id"],
                    "Author Public Key": f"{best_match['public_key'][:30]}...",
                    "Timestamp": time.ctime(best_match["timestamp"]),
                    "IPFS CID": f"ipfs://{best_match['ipfs_cid']}",
                    "Decrypted Metadata": metadata
                })
            else:
                st.error("❌ **Media NOT FOUND or MANIPULATED.**")
                if best_match:
                    st.warning(f"Closest match had a Hamming distance of {min_dist} bits, which exceeds the threshold.")

# --- TAB 5: Blockchain Explorer ---
with tabs[4]:
    st.header("Blockchain Ledger Explorer")
    if st.button("Refresh Ledger"):
        registry.load_chain()
        
    for block in reversed(registry.chain):
        with st.expander(f"Block #{block.index} | Hash: {block.hash}"):
            st.write(f"**Timestamp:** {time.ctime(block.timestamp)}")
            st.write(f"**Previous Hash:** {block.previous_hash}")
            st.write(f"**Nonce:** {block.nonce}")
            st.write("**Transactions (Notice metadata is hidden off-chain):**")
            st.json(block.transactions)
