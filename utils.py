# utils.py
import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
import json
from datetime import datetime
import psycopg2
import psycopg2.extras


# --- UNIT DEFINITIONS ---
UNITS = {
    "Rupees": 1,
    "Thousands": 1000,
    "Lakhs": 100000,
    "Crores": 10000000
}
UNIT_OPTIONS = ["","Rupees","Thousands", "Lakhs", "Crores"]
# Default persistent file
LEADS_FILE = Path("data/leads.xlsx")
LEADS_SHEET = "leads"

def to_excel(df):
    """Converts a DataFrame to an Excel file in memory for download."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=LEADS_SHEET)
    processed_data = output.getvalue()
    return processed_data

def ensure_data_dir():
    data_dir = LEADS_FILE.parent
    data_dir.mkdir(parents=True, exist_ok=True)

def _read_all_leads():
    """Return a DataFrame of all leads; empty df if file missing."""
    ensure_data_dir()
    if not LEADS_FILE.exists():
        return pd.DataFrame()
    try:
        df = pd.read_excel(LEADS_FILE, sheet_name=LEADS_SHEET, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Could not read leads file: {e}")
        return pd.DataFrame()

# def save_lead_to_excel(lead_dict, status="draft"):
#     """
#     Append or upsert a lead into data/leads.xlsx using mobile_number as key.
#     lead_dict is a Python dict with the lead fields (will store full lead_json too).
#     Returns True/False for success.
#     """
#     ensure_data_dir()
#     try:
#         df_all = _read_all_leads()
#         # Normalize a few columns we want to keep separate (if present)
#         mobile = lead_dict.get('mobile_number')
#         vintage = lead_dict.get('vintage_years')
#         pincode = lead_dict.get('pincode')
#         yearly_turnover = lead_dict.get('yearly_turnover')
#         foir = lead_dict.get('foir')
#         requested_loan_type = lead_dict.get('requested_loan_type')
#         is_ntc = lead_dict.get('is_ntc')

#         # store a JSON string snapshot of the full lead
#         lead_json = json.dumps(lead_dict, default=str)

#         row = {
#             "mobile_number": mobile,
#             "vintage_years": vintage,
#             "pincode": pincode,
#             "yearly_turnover": yearly_turnover,
#             "foir": foir,
#             "requested_loan_type": requested_loan_type,
#             "is_ntc": is_ntc,
#             "lead_json": lead_json,
#             "status": status,
#             "updated_at": datetime.utcnow()
#         }

#         # If df empty -> create new
#         if df_all.empty:
#             df_new = pd.DataFrame([row])
#         else:
#             # Upsert by mobile_number
#             # if mobile exists, replace its row; else append
#             if mobile and (df_all['mobile_number'].astype(str) == str(mobile)).any():
#                 df_all.loc[df_all['mobile_number'].astype(str) == str(mobile), :] = df_all.loc[df_all['mobile_number'].astype(str) == str(mobile), :].copy()
#                 # Replace the first matching row
#                 idx = df_all.index[df_all['mobile_number'].astype(str) == str(mobile)][0]
#                 for k, v in row.items():
#                     df_all.at[idx, k] = v
#                 df_new = df_all
#             else:
#                 df_new = pd.concat([df_all, pd.DataFrame([row])], ignore_index=True)

#         # Save to Excel
#         with pd.ExcelWriter(LEADS_FILE, engine='openpyxl', mode='w') as writer:
#             df_new.to_excel(writer, index=False, sheet_name=LEADS_SHEET)

#         return True
#     except Exception as e:
#         st.error(f"Failed to save lead to Excel: {e}")
#         return False

# def load_draft_from_excel(mobile):
#     """
#     Load a draft by mobile number from data/leads.xlsx.
#     Returns dict: {lead_data: dict, status: str, updated_at: datetime} or None
#     """
#     if not mobile:
#         return None
#     df_all = _read_all_leads()
#     if df_all.empty:
#         return None
#     try:
#         match = df_all[df_all['mobile_number'].astype(str) == str(mobile)]
#         if match.empty:
#             return None
#         # take the most recently updated if multiple
#         match = match.sort_values('updated_at', ascending=False).iloc[0]
#         lead_json = match.get('lead_json')
#         if isinstance(lead_json, str):
#             lead_dict = json.loads(lead_json)
#         else:
#             # If it's already a dict-like or pd.NA
#             lead_dict = lead_json or {}
#         return {"lead_data": lead_dict, "status": match.get('status'), "updated_at": match.get('updated_at')}
#     except Exception as e:
#         st.error(f"Failed to load draft from Excel: {e}")
#         return None

@st.cache_resource
def load_pincode_sets():
    """
    Loads serviceable pincodes from CSV files into a dictionary of sets.
    """
    pincode_sets = {}
    # IMPORTANT: Update these file paths to be correct for your system
    lender_files = {
        "Indifi (Term Loan)": "data/indifi_pincode.csv",
        "Kotak (Term Loan)": "data/kotak_pincode.csv",
        "Bajaj (Term Loan)":"data/bajaj_pincode.csv",
        "Bajaj (STBL Lite T/O < 50L)":"data/bajaj_pincode.csv",
        "Bajaj (STBL T/O > 50L)":"data/bajaj_pincode.csv",
        "Flexi (Term Loan)":"data/flexi_pincode.csv",
        "Kotak (CA Program)": "data/kotak_pincode.csv",
        "L&T (Term Loan)":"data/ltfs_pincode.csv",
        "L&T (CA Program)":"data/ltfs_pincode.csv",
        "Hero (Term Loan)":"data/hero_pincode.csv",
        "Credit Saison (SBA Program)":"data/credit_saison_pincode.csv",
        "Credit Saison (UBL Program)":"data/credit_saison_pincode.csv"
    }

    for lender, filename in lender_files.items():
        try:
            # Read the CSV file
            df = pd.read_csv(filename)
            
            # Convert the 'pincode' column to a set of integers for fast lookup
            pincode_sets[lender] = set(df['pincode'].astype(int))
            print(f"Loaded {len(pincode_sets[lender])} pincodes for {lender}")
            
        except FileNotFoundError:
            st.error(f"Pincode file not found: {filename}. {lender} will have no pincode rules.")
            pincode_sets[lender] = set() # Create an empty set
        except Exception as e:
            st.error(f"Error loading {filename}: {e}")
            pincode_sets[lender] = set()

    return pincode_sets


@st.cache_resource
def load_negative_industry_sets():
    negative_industry_sets = {}
    lender_files = {
        "Indifi (Term Loan)": "data/bajaj_negative_industry.csv",
        "Kotak (Term Loan)": "data/bajaj_negative_industry.csv",
        "Bajaj (Term Loan)":"data/bajaj_negative_industry.csv",
        "Bajaj (STBL Lite T/O < 50L)":"data/bajaj_negative_industry.csv",
        "Bajaj (STBL T/O > 50L)":"data/bajaj_negative_industry.csv",
        "Flexi (Term Loan)":"data/flexi_negative_industry.csv",
        "Kotak (CA Program)": "data/bajaj_negative_industry.csv",
        "L&T (Term Loan)":"data/ltfs_negative_industries.csv",
        "L&T (CA Program)":"data/ltfs_negative_industries.csv",
        "Hero (Term Loan)":"data/ltfs_negative_industries.csv",
        "Credit Saison (SBA Program)":"data/ltfs_negative_industries.csv",
        "Credit Saison (UBL Program)":"data/ltfs_negative_industries.csv"
    }
    for lender,filename in lender_files.items():
        try:
            df = pd.read_csv(filename)
            
            # --- START FIX ---
            # Clean and normalize the data: drop NAs, convert to string, strip whitespace, and convert to lowercase
            df_cleaned = df['negative_industries'].dropna().astype(str)
            negative_industry_sets[lender] = set(s.strip().lower() for s in df_cleaned)
            # --- END FIX ---

            print(f"Loaded {len(negative_industry_sets[lender])} Negative Industries for {lender}")
        except FileNotFoundError:
            st.error(f"Negative Industry file not found: {filename}. {lender} will have no rules.")
            negative_industry_sets[lender] = set()
        except Exception as e:
            st.error(f"Error loading {filename}: {e}")
            negative_industry_sets[lender] = set()
        
    return negative_industry_sets

@st.cache_resource
def init_db_connection():
    """
    Initialize and return a psycopg2 connection using Streamlit secrets.
    Expects the secret at st.secrets["supabase"]["DATABASE_URL"].
    """
    db_url = None
    try:
        db_url = st.secrets["supabase"]["DATABASE_URL"]
    except Exception:
        st.error("Database URL not found in Streamlit secrets under ['supabase']['DATABASE_URL'].")
        raise

    # Use sslmode=require to be safe for cloud connections
    conn = psycopg2.connect(db_url, sslmode='require', cursor_factory=psycopg2.extras.RealDictCursor)
    return conn

def save_lead_to_db(lead_dict, status="draft"):
    """
    Upsert lead into public.bdo_leads using mobile_number as the key.
    lead_dict: dict containing lead data. Returns True/False.
    """
    try:
        conn = init_db_connection()
        mobile = lead_dict.get('mobile_number')
        if not mobile:
            st.error("Mobile number required to save.")
            return False

        # Prepare values
        vintage = lead_dict.get('vintage_years')
        pincode = lead_dict.get('pincode')
        yearly_turnover = lead_dict.get('yearly_turnover')
        foir = lead_dict.get('foir')
        requested_loan_type = lead_dict.get('requested_loan_type')
        is_ntc = bool(lead_dict.get('is_ntc'))
        # Save full snapshot as JSON
        lead_json = json.dumps(lead_dict, default=str)
        eligibility = lead_dict.get('eligibility_results', None)

        query = """
        INSERT INTO public.bdo_leads (
            mobile_number, vintage_years,firm_name,bdo_name, business_segment, nature_of_business,
            constitution_type, gender, age, co_applicant_details, monthly_turnover,
            yearly_turnover, total_obligations, foir, pincode, ownership_status,
            profit_last_year, eligibility_results, is_ntc, requested_loan_type,
            lead_json, draft_step, status, updated_at, remarks
        )
        VALUES (
            %(mobile)s, %(vintage)s,%(firm_name)s,%(bdo_name)s, %(business_segment)s, %(nature_of_business)s,
            %(constitution_type)s, %(gender)s, %(age)s, %(co_applicant_details)s, %(monthly_turnover)s,
            %(yearly_turnover)s, %(total_obligations)s, %(foir)s, %(pincode)s, %(ownership_status)s,
            %(profit_last_year)s, %(eligibility_results)s, %(is_ntc)s, %(requested_loan_type)s,
            %(lead_json)s, %(draft_step)s, %(status)s, now(), %(remarks)s
        )
        ON CONFLICT (mobile_number) DO UPDATE SET
            firm_name = EXCLUDED.firm_name,
            bdo_name = EXCLUDED.bdo_name,
            vintage_years = EXCLUDED.vintage_years,
            business_segment = EXCLUDED.business_segment,
            nature_of_business = EXCLUDED.nature_of_business,
            constitution_type = EXCLUDED.constitution_type,
            gender = EXCLUDED.gender,
            age = EXCLUDED.age,
            co_applicant_details = EXCLUDED.co_applicant_details,
            monthly_turnover = EXCLUDED.monthly_turnover,
            yearly_turnover = EXCLUDED.yearly_turnover,
            total_obligations = EXCLUDED.total_obligations,
            foir = EXCLUDED.foir,
            pincode = EXCLUDED.pincode,
            ownership_status = EXCLUDED.ownership_status,
            profit_last_year = EXCLUDED.profit_last_year,
            eligibility_results = EXCLUDED.eligibility_results,
            is_ntc = EXCLUDED.is_ntc,
            requested_loan_type = EXCLUDED.requested_loan_type,
            lead_json = EXCLUDED.lead_json,
            draft_step = EXCLUDED.draft_step,
            status = EXCLUDED.status,
            updated_at = now(),
            remarks = EXCLUDED.remarks;
        """

        params = {
            "mobile": mobile,
            "vintage": vintage,
            "firm_name": lead_dict.get('firm_name'),
            "bdo_name": lead_dict.get('bdo_name'),
            "business_segment": lead_dict.get('business_segment'),
            "nature_of_business": lead_dict.get('nature_of_business'),
            "constitution_type": lead_dict.get('constitution_type'),
            "gender": lead_dict.get('gender'),
            "age": lead_dict.get('age'),
            "co_applicant_details": json.dumps(lead_dict.get('co_applicant_details')) if lead_dict.get('co_applicant_details') else None,
            "monthly_turnover": lead_dict.get('monthly_turnover'),
            "yearly_turnover": yearly_turnover,
            "total_obligations": lead_dict.get('total_obligations'),
            "foir": foir,
            "pincode": pincode,
            "ownership_status": lead_dict.get('ownership_status'),
            "profit_last_year": lead_dict.get('profit_last_year'),
            "eligibility_results": json.dumps(eligibility) if eligibility is not None else None,
            "is_ntc": is_ntc,
            "requested_loan_type": requested_loan_type,
            "lead_json": lead_json,
            "draft_step": lead_dict.get('draft_step'),
            "status": status,
            "remarks": lead_dict.get('remarks')
        }

        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Failed to save lead to DB: {e}")
        return False

def load_draft_from_db(mobile):
    """
    Load lead row by mobile number. Returns dict {'lead_data': {...}, 'draft_step':..., 'status':..., 'updated_at':...} or None.
    Robustly handles lead_json stored as jsonb/dict or as string.
    """
    try:
        conn = init_db_connection()
        query = "SELECT lead_json, draft_step, status, updated_at FROM public.bdo_leads WHERE mobile_number = %s LIMIT 1;"
        with conn.cursor() as cur:
            cur.execute(query, (str(mobile),))
            row = cur.fetchone()
            if not row:
                return None

            # If using RealDictCursor, row may be a dict-like
            if isinstance(row, dict):
                lead_json = row.get('lead_json')
                draft_step = row.get('draft_step')
                status = row.get('status')
                updated_at = row.get('updated_at')
            else:
                # tuple-like: (lead_json, draft_step, status, updated_at)
                lead_json, draft_step, status, updated_at = row

            # Parse lead_json into a python dict regardless of stored type
            lead_data = {}
            if lead_json is None:
                lead_data = {}
            elif isinstance(lead_json, dict):
                lead_data = lead_json
            else:
                # lead_json likely a string
                try:
                    lead_data = json.loads(lead_json)
                except Exception:
                    # fallback: leave as empty dict if unparseable
                    lead_data = {}

            # ensure draft_step is also present inside lead_data (useful when restoring)
            if 'draft_step' not in lead_data and draft_step is not None:
                try:
                    lead_data['draft_step'] = int(draft_step)
                except Exception:
                    lead_data['draft_step'] = draft_step

            return {"lead_data": lead_data, "draft_step": draft_step, "status": status, "updated_at": updated_at}
    except Exception as e:
        st.error(f"Failed to load draft from DB: {e}")
        return None