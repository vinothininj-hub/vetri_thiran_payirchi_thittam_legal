import os
import requests
import streamlit as st
from dotenv import load_dotenv
from core.exporters import format_docx, format_html_preview, format_pdf
load_dotenv(); BACKEND_URL=os.getenv("BACKEND_URL","http://127.0.0.1:8000").rstrip("/")
st.set_page_config(page_title="LegalEase",page_icon="⚖️",layout="wide")
st.title("⚖️ LegalEase"); st.caption("AI-assisted legal document drafting and export")
if "document" not in st.session_state: st.session_state.document=""
if "editing" not in st.session_state: st.session_state.editing=False
with st.sidebar:
    st.header("Document Details")
    document_type=st.selectbox("Document type",["Employment Contract","NDA","Lease Agreement","Employment Offer Letter","Freelance Work Contract","Service Agreement","General Agreement","Custom"])
    if document_type=="Custom": document_type=st.text_input("Custom document type")
    effective_date=st.text_input("Effective date",placeholder="e.g. 1 October 2026")
    parties=st.text_area("Parties",height=120,placeholder="Party A: ABC Pvt Ltd\nParty B: John Doe")
    terms=st.text_area("Terms / requirements",height=220,placeholder="1. Scope of work\n2. Payment terms\n3. Confidentiality")
    logo=st.file_uploader("Optional company logo",type=["png","jpg","jpeg"])
    generate=st.button("Generate Document",type="primary",use_container_width=True)
if generate:
    if not all([document_type.strip(),effective_date.strip(),parties.strip(),terms.strip()]): st.error("Please complete all required fields.")
    else:
        try:
            with st.spinner("Generating document..."):
                r=requests.post(f"{BACKEND_URL}/generate",json={"document_type":document_type,"parties":parties,"terms":terms,"effective_date":effective_date},timeout=120)
            if r.ok: st.session_state.document=r.json()["content"]; st.session_state.editing=False; st.success("Document generated successfully.")
            else: st.error(f"Backend error: {r.json().get('detail',r.text)}")
        except requests.RequestException as e: st.error(f"Could not connect to FastAPI at {BACKEND_URL}: {e}")
if st.session_state.document:
    st.subheader("Document")
    if st.button("Stop Editing" if st.session_state.editing else "Edit Document"): st.session_state.editing=not st.session_state.editing; st.rerun()
    if st.session_state.editing: st.session_state.document=st.text_area("Edit document",value=st.session_state.document,height=650)
    st.markdown(f"<div style='background:white;color:#111827;padding:2rem;border-radius:12px'>{format_html_preview(st.session_state.document)}</div>",unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a: st.download_button("Download TXT",st.session_state.document.encode(),"legalease_document.txt","text/plain",use_container_width=True)
    with b: st.download_button("Download DOCX",format_docx(st.session_state.document,document_type,logo.getvalue() if logo else None),"legalease_document.docx","application/vnd.openxmlformats-officedocument.wordprocessingml.document",use_container_width=True)
    with c: st.download_button("Download PDF",format_pdf(st.session_state.document,document_type,logo.getvalue() if logo else None),"legalease_document.pdf","application/pdf",use_container_width=True)
st.divider(); st.caption("Disclaimer: LegalEase provides AI-assisted drafting support. Generated documents should be reviewed by a qualified legal professional.")
