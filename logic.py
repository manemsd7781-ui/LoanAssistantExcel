import utils

# Load the pincode sets ONCE
SERVICEABLE_PINCODES = utils.load_pincode_sets()
NEGATIVE_INDUSTRIES = utils.load_negative_industry_sets()

# --- LENDER POLICY RULES (JSON stored as Python Dictionary) ---
POLICY_RULES = {
    "Indifi (Term Loan)": {
        "min_vintage_years": 1,
        "allowed_constitutions": ["Sole Proprietor", "Partnership", "LLP", "Private Ltd","Public Ltd"],
        "min_yearly_turnover": 4000000,
        "max_foir": 0.30,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Indifi (Term Loan)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned", "Office Owned", "Both Rented","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Indifi (Term Loan)", set()),
        "ntc_allowed": False,
        "allowed_loan_types": ["Term Loan"]
    },
    "Bajaj (Term Loan)": {
        "min_vintage_years": 3,
        "allowed_constitutions" : ["Sole Proprietor", "Partnership", "LLP", "Private Ltd", "Public Ltd"],
        "min_yearly_turnover": 2000000,
        "max_foir": 0.17,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Bajaj (Term Loan)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned","Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Bajaj (Term Loan)",set()),
        "ntc_allowed": True,
        "allowed_loan_types": ["Term Loan", "DLOD", "LAP"]
    },
    "Bajaj (STBL Lite T/O < 50L)": {
        "min_vintage_years": 1,
        "allowed_constitutions" : ["Sole Proprietor"],
        "min_yearly_turnover": 1000000,
        "max_foir": 0.17,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Bajaj (STBL Lite T/O < 50L)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned","Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Bajaj (STBL Lite T/O < 50L)",set()),
        "ntc_allowed": True,
        "allowed_loan_types": ["Term Loan"]
    },
    "Bajaj (STBL T/O > 50L)": {
        "min_vintage_years": 1,
        "allowed_constitutions" : ["Sole Proprietor"],
        "min_yearly_turnover": 5000000,
        "max_foir": 0.17,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Bajaj (STBL T/O > 50L)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned","Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Bajaj (STBL T/O > 50L)",set()),
        "ntc_allowed": True,
        "allowed_loan_types": ["Term Loan"]
    },
    "Flexi (Term Loan)": {
        "min_vintage_years": 2,
        "allowed_constitutions": ["Sole Proprietor", "Partnership", "LLP", "Private Ltd", "Public Ltd"],
        "min_yearly_turnover": 2400000,
        "max_foir": 0.30,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Flexi (Term Loan)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned", "Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Flexi (Term Loan)",set()),
        "ntc_allowed": True,
        "allowed_loan_types": ["Term Loan"]
    },
    "Kotak (Term Loan)":{
        "min_vintage_years": 3,
        "allowed_constitutions": ["Sole Proprietor", "Partnership", "LLP", "Private Ltd", "Public Ltd"],
        "min_yearly_turnover": 5000000,
        "max_foir": 0.30,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Kotak (Term Loan)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned", "Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Kotak (Term Loan)",set()),
        "ntc_allowed": True,
        "allowed_loan_types": ["Term Loan", "LAP", "OD"]
    },
    "Kotak (CA Program)":{
        "min_vintage_years": 1,
        "allowed_constitutions": ["Sole Proprietor", "CA"],
        "min_yearly_turnover": 5000000,
        "max_foir": 0.30,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Kotak (CA Program)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned", "Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Kotak (CA Program)",set()),
        "ntc_allowed": False,
        "allowed_loan_types": ["Term Loan"]
    },
    "L&T (Term Loan)":{
        "min_vintage_years": 3,
        "allowed_constitutions": ["Sole Proprietor", "Partnership", "LLP", "Private Ltd", "Public Ltd"],
        "min_yearly_turnover": 10000000,
        "max_foir": 0.30,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("L&T (Term Loan)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned", "Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("L&T (Term Loan)",set()),
        "ntc_allowed": False,
        "allowed_loan_types": ["Term Loan","DLOD"]
    },
    "L&T (CA Program)":{
        "min_vintage_years": 3,
        "allowed_constitutions": ["Sole Proprietor", "CA"],
        "min_yearly_turnover": 5000000,
        "max_foir": 0.30,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("L&T (CA Program)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned", "Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("L&T (CA Program)",set()),
        "ntc_allowed": False,
        "allowed_loan_types": ["Term Loan"]
    },
    "Hero (Term Loan)":{
        "min_vintage_years": 3,
        "allowed_constitutions": ["Sole Proprietor", "Partnership", "LLP", "Private Ltd", "Public Ltd"],
        "min_yearly_turnover": 5000000,
        "max_foir": 0.30,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Hero (Term Loan)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned", "Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Hero (Term Loan)",set()),
        "ntc_allowed": False,
        "allowed_loan_types": ["Term Loan"]
    },
    "Credit Saison (SBA Program)":{
        "min_vintage_years": 3,
        "allowed_constitutions": ["Sole Proprietor", "Partnership", "LLP", "Private Ltd", "Public Ltd"],
        "min_yearly_turnover": 1000000,
        "max_foir": 0.50,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Credit Saison (SBA Program)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned", "Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Credit Saison (SBA Program)",set()),
        "ntc_allowed": False,
        "allowed_loan_types": ["Term Loan"]
    },
    "Credit Saison (UBL Program)":{
        "min_vintage_years": 3,
        "allowed_constitutions": ["Sole Proprietor", "Partnership", "LLP", "Private Ltd", "Public Ltd"],
        "min_yearly_turnover": 10000000,
        "max_foir": 0.50,
        "allowed_pincodes": SERVICEABLE_PINCODES.get("Credit Saison (UBL Program)", set()),
        "allowed_ownership": ["Both Owned", "Residence Owned", "Office Owned","Residence Owned in Other City"],
        "negative_industry": NEGATIVE_INDUSTRIES.get("Credit Saison (UBL Program)",set()),
        "ntc_allowed": False,
        "allowed_loan_types": ["Term Loan"]
    }
}


# --- ELIGIBILITY CHECKING LOGIC ---
def check_eligibility(lead_data):
    """
    Checks the lead data against all lender policies.
    Returns a dictionary with eligibility status, failure reasons and tips for each lender.
    """
    results = {}
    for lender, rules in POLICY_RULES.items():
        is_eligible = True
        reasons = []
        tips = []

        # 1. Vintage Check
        if 'vintage_years' in lead_data and lead_data['vintage_years'] is not None:
            try:
                vintage = float(lead_data['vintage_years'])
            except Exception:
                vintage = None

            if vintage is not None:
                min_vintage = rules.get('min_vintage_years', 0)
                if vintage < min_vintage:
                    is_eligible = False
                    reasons.append(f"Business vintage is {vintage:.2f} years (requires {min_vintage}+ years).")

                # Tip logic: if vintage is within last 3 months (0.25 years) below the min requirement
                # e.g., for min_vintage 3 -> tip if vintage between 2.75 and 3.0
                tolerance_years = 0.25  # 3 months
                lower_bound = max(0.0, min_vintage - tolerance_years)
                if lower_bound <= vintage < min_vintage:
                    # Add a tip only (do not mark as failed)
                    tips.append(
                        f"Tip: Vintage is {vintage:.2f} years — close to the {min_vintage}-year requirement. "
                        "If additional evidence (e.g., earlier business documents) is available or if the underwriter "
                        "considers associated/previous business history, a deviation may be considered."
                    )

        # 2. Constitution Check
        if 'constitution_type' in lead_data and lead_data['constitution_type'] not in rules.get('allowed_constitutions', []):
            is_eligible = False
            reasons.append(f"Constitution type '{lead_data['constitution_type']}' is not supported.")

        # 3. Turnover Check
        if 'yearly_turnover' in lead_data and lead_data['yearly_turnover'] is not None:
            try:
                yearly_turnover = float(lead_data['yearly_turnover'])
            except Exception:
                yearly_turnover = None
            if yearly_turnover is not None and yearly_turnover < rules.get('min_yearly_turnover', 0):
                is_eligible = False
                reasons.append(f"Yearly turnover is ₹{int(yearly_turnover):,} (requires ₹{rules['min_yearly_turnover']:,}+).")

        # 4. FOIR Check
        if 'foir' in lead_data and lead_data['foir'] is not None:
            try:
                foir_val = float(lead_data['foir'])
            except Exception:
                foir_val = None
            if foir_val is not None and foir_val > rules.get('max_foir', 1.0):
                is_eligible = False
                reasons.append(f"FOIR is {foir_val:.0%} (max allowed is {rules['max_foir']:.0%}).")

        # 5. Pincode Check
        if 'allowed_pincodes' in rules:
            user_pincode_str = lead_data.get('pincode')
            if not user_pincode_str:
                is_eligible = False
                reasons.append("Pincode is missing.")
            else:
                try:
                    user_pincode_int = int(user_pincode_str)
                    if user_pincode_int not in rules['allowed_pincodes']:
                        is_eligible = False
                        reasons.append(f"Pincode {user_pincode_str} is not in a serviceable area.")
                except ValueError:
                    is_eligible = False
                    reasons.append(f"Pincode '{user_pincode_str}' is invalid.")

        # 6. Negative industry check (containment match)
        if 'negative_industry' in rules:
            user_industry = lead_data.get('business_segment')
            if user_industry:
                normalized_industry = user_industry.strip().lower()
                for negative_term in rules['negative_industry']:
                    if negative_term in normalized_industry:
                        is_eligible = False
                        reasons.append(f"Industry '{user_industry}' is negative (contains '{negative_term}').")
                        break

        # 7. Ownership Status Check
        if 'ownership_status' in lead_data and lead_data['ownership_status'] not in rules.get('allowed_ownership', []):
            is_eligible = False
            reasons.append(f"Ownership status '{lead_data['ownership_status']}' is not supported.")

        # 8. NTC check
        if 'is_ntc' in lead_data and lead_data['is_ntc'] is True:
            if not rules.get('ntc_allowed', False):
                is_eligible = False
                reasons.append("New to Credit (NTC) customers are not supported.")

        # 9. Requested Loan Type Check
        requested_loan_type = lead_data.get('requested_loan_type')
        if requested_loan_type:
            allowed = rules.get('allowed_loan_types', ["Term Loan"])
            if requested_loan_type not in allowed:
                is_eligible = False
                pretty_requested = "Loan Against Property (LAP)" if requested_loan_type == "LAP" else requested_loan_type
                reasons.append(f"Requested loan type '{pretty_requested}' is not offered by {lender}.")

        # Finalize
        results[lender] = {
            "eligible": is_eligible,
            "reasons": reasons if not is_eligible else ["All criteria passed."],
            "tips": tips  # empty list if none
        }

    return results