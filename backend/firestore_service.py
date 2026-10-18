"""
Cloud Firestore Integration Service
Provides real-time persistence for telemetry events, incident alerts, work orders, and QA audits.
Supports live Google Cloud Firestore with zero-configuration local persistence fallback.
"""

import os
import json
import datetime
from typing import Dict, Any, List, Optional

FIRESTORE_AVAILABLE = False
db_client = None

# Attempt to load Google Cloud Firestore client
try:
    from google.cloud import firestore
    # Check if GCP project or credentials exist
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if project_id:
        db_client = firestore.Client(project=project_id)
        FIRESTORE_AVAILABLE = True
    else:
        # Try default credentials
        db_client = firestore.Client()
        FIRESTORE_AVAILABLE = True
except Exception:
    FIRESTORE_AVAILABLE = False
    db_client = None

# Local Fallback In-Memory / File-based Store
LOCAL_STORE_PATH = os.path.join(os.path.dirname(__file__), "local_firestore_cache.json")

def _load_local_store() -> Dict[str, Any]:
    if os.path.exists(LOCAL_STORE_PATH):
        try:
            with open(LOCAL_STORE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "telemetry_stream": [],
        "incidents": [],
        "work_orders": [],
        "qa_inspections": []
    }

def _save_local_store(data: Dict[str, Any]):
    try:
        with open(LOCAL_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

class FirestoreService:
    @staticmethod
    def is_connected_to_gcp() -> bool:
        """Returns True if connected to live Google Cloud Firestore."""
        return FIRESTORE_AVAILABLE and db_client is not None

    @staticmethod
    def get_connection_info() -> Dict[str, str]:
        if FIRESTORE_AVAILABLE and db_client is not None:
            return {
                "status": "Connected to Google Cloud Firestore",
                "backend": "Google Cloud Firestore (Live)",
                "project": getattr(db_client, "project", "Auto-Detected")
            }
        else:
            return {
                "status": "Local Real-Time Emulation",
                "backend": "Firestore Emulated Ledger (Memory + Sync)",
                "project": "mfg-intelligent-ops-dev"
            }

    @classmethod
    def record_incident(cls, incident: Dict[str, Any]) -> str:
        """Saves a machine anomaly alert into Firestore 'incidents' collection."""
        doc_id = f"INC-{int(datetime.datetime.now().timestamp())}"
        incident["id"] = doc_id
        incident["created_at"] = datetime.datetime.now().isoformat()
        
        if cls.is_connected_to_gcp():
            try:
                db_client.collection("incidents").document(doc_id).set(incident)
                return doc_id
            except Exception as e:
                print(f"[Firestore Warning] Fallback to local store: {e}")

        # Local store
        store = _load_local_store()
        store["incidents"].insert(0, incident)
        # Keep last 50
        store["incidents"] = store["incidents"][:50]
        _save_local_store(store)
        return doc_id

    @classmethod
    def get_incidents(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves recent machine anomaly alerts."""
        if cls.is_connected_to_gcp():
            try:
                docs = db_client.collection("incidents").order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit).stream()
                return [doc.to_dict() for doc in docs]
            except Exception:
                pass
        
        store = _load_local_store()
        return store["incidents"][:limit]

    @classmethod
    def save_work_order(cls, work_order: Dict[str, Any]) -> str:
        """Stores a Gemini-generated Standard Operating Procedure / Maintenance Work Order."""
        doc_id = f"WO-{int(datetime.datetime.now().timestamp())}"
        work_order["id"] = doc_id
        work_order["created_at"] = datetime.datetime.now().isoformat()

        if cls.is_connected_to_gcp():
            try:
                db_client.collection("work_orders").document(doc_id).set(work_order)
                return doc_id
            except Exception as e:
                print(f"[Firestore Warning] Fallback to local store: {e}")

        store = _load_local_store()
        store["work_orders"].insert(0, work_order)
        store["work_orders"] = store["work_orders"][:50]
        _save_local_store(store)
        return doc_id

    @classmethod
    def get_work_orders(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves maintenance work orders."""
        if cls.is_connected_to_gcp():
            try:
                docs = db_client.collection("work_orders").order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit).stream()
                return [doc.to_dict() for doc in docs]
            except Exception:
                pass

        store = _load_local_store()
        return store["work_orders"][:limit]

    @classmethod
    def save_qa_inspection(cls, inspection: Dict[str, Any]) -> str:
        """Stores a visual inspection result from Gemini multimodal analysis."""
        doc_id = f"QA-{int(datetime.datetime.now().timestamp())}"
        inspection["id"] = doc_id
        inspection["timestamp"] = datetime.datetime.now().isoformat()

        if cls.is_connected_to_gcp():
            try:
                db_client.collection("qa_inspections").document(doc_id).set(inspection)
                return doc_id
            except Exception as e:
                print(f"[Firestore Warning] Fallback to local store: {e}")

        store = _load_local_store()
        store["qa_inspections"].insert(0, inspection)
        store["qa_inspections"] = store["qa_inspections"][:50]
        _save_local_store(store)
        return doc_id

    @classmethod
    def get_qa_inspections(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves visual inspection records."""
        if cls.is_connected_to_gcp():
            try:
                docs = db_client.collection("qa_inspections").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit).stream()
                return [doc.to_dict() for doc in docs]
            except Exception:
                pass

        store = _load_local_store()
        return store["qa_inspections"][:limit]

    @classmethod
    def get_all_collections_summary(cls) -> Dict[str, Any]:
        """Provides a live diagnostic view of collections and total documents."""
        incidents = cls.get_incidents(10)
        work_orders = cls.get_work_orders(10)
        inspections = cls.get_qa_inspections(10)
        
        return {
            "incidents": {
                "count": len(incidents),
                "recent": incidents[:3]
            },
            "work_orders": {
                "count": len(work_orders),
                "recent": work_orders[:3]
            },
            "qa_inspections": {
                "count": len(inspections),
                "recent": inspections[:3]
            }
        }
