# ui_capture.py
import streamlit as st
import json
import logic
import utils
from datetime import datetime

def display_lead_capture():
    """
    Renders the Lead Capture view and the Eligibility Board.
    """
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.lead_data = {}
        st.session_state.eligibility_results = {}

    def save_lead_to_storage(is_draft=True):
        # uses utils.save_lead_to_excel
        try:
            status = 'draft' if is_draft else 'active'
            ok = utils.save_lead_to_excel(st.session_state.lead_data, status=status)
            return ok
        except Exception as e:
            st.error(f"Failed to save lead: {e}")
            return False

    def load_draft_from_storage(mobile):
        try:
            return utils.load_draft_from_excel(mobile)
        except Exception as e:
            st.error(f"Failed to load draft: {e}")
            return None

    # Reset button
    if st.sidebar.button("Start New Lead"):
        st.session_state.clear()
        st.rerun()

    # --- UI LAYOUT ---
    chat_col, board_col = st.columns([1, 1])

    with chat_col:
        st.header("Lead Details")

        # STEP 0: Mobile Number
        if st.session_state.step >= 0:
            col_mobile, col_load = st.columns([3,1])
            with col_mobile:
                mobile = st.text_input("1. What is the client's Mobile Number?", key="mobile_number_input", max_chars=10)
            with col_load:
                if st.button("Load Draft", key="load_draft_btn"):
                    if mobile and mobile.isdigit() and len(mobile) == 10:
                        result = load_draft_from_storage(mobile)
                        if result:
                            st.session_state.lead_data = result['lead_data'] or {}
                            # step: if draft had no step info, try to resume safely
                            st.session_state.step = result['lead_data'].get('draft_step', st.session_state.step)
                            st.session_state.eligibility_results = logic.check_eligibility(st.session_state.lead_data)
                            st.success(f"Draft loaded for {mobile}. Resuming.")
                            st.rerun()
                        else:
                            st.warning("No draft found for this mobile.")
                    else:
                        st.error("Enter a valid 10-digit mobile number before loading a draft.")

        if mobile:
            if mobile.isdigit() and len(mobile) == 10:
                st.session_state.lead_data['mobile_number'] = mobile
                if st.session_state.step == 0: st.session_state.step = 1
            else:
                st.error("Please enter a valid 10-digit mobile number.")

        # (the rest of your steps remain the same, unchanged)
        # I'll include them exactly as you had, but with Save/Save Draft using save_lead_to_storage

        # STEP 1: Pincode (moved up)
        if st.session_state.step >= 1:
            pincode = st.text_input("2. What is the Pincode?", max_chars=6, key="pincode_input")
            if pincode:
                if pincode.isdigit() and len(pincode) == 6:
                    st.session_state.lead_data['pincode'] = pincode
                    if st.session_state.step == 1: st.session_state.step = 2
                else:
                    st.error("Please enter a valid 6-digit pincode.")

        # STEP 2: Business Vintage
        if st.session_state.step >= 2:
            vintage = st.number_input(
                "3. What is the Vintage of Business (in years)?",min_value=0.0,step=0.01,format="%.2f", key="vintage_input")
            if vintage is not None and vintage > 0.0:
                st.session_state.lead_data['vintage_years'] = float(vintage)
                if st.session_state.step == 2:
                    st.session_state.step = 3

        # STEP 3: Ownership (moved up)
        if st.session_state.step >= 3:
            ownership = st.selectbox("4. What is the Ownership Status?", ["", "Both Owned", "Both Rented", "Residence Owned", "Office Owned", "Residence Owned in Other City"], key="ownership_input")
            if ownership:
                st.session_state.lead_data['ownership_status'] = ownership
                if st.session_state.step == 3: st.session_state.step = 4

        # STEP 4: Business Segment
        if st.session_state.step >= 4:
            segment = st.text_input("5. What is the Business Industry?", key="segment_input")
            if segment:
                st.session_state.lead_data['business_segment'] = segment
                if st.session_state.step == 4: st.session_state.step = 5

        # STEP 5: Nature of Business
        if st.session_state.step >= 5:
            nature = st.selectbox("6. What is the Nature of Business?", ["", "Retailer", "Manufacturer", "Service Provider", "Wholesaler"], key="nature_input")
            if nature:
                st.session_state.lead_data['nature_of_business'] = nature
                if st.session_state.step == 5: st.session_state.step = 6

        # STEP 6: Constitution Type
        if st.session_state.step >= 6:
            constitution = st.selectbox("7. What is the Constitution Type?", ["", "Sole Proprietor", "Partnership", "LLP", "Private Ltd", "Public Ltd", "CA","Others"], key="constitution_input")
            if constitution:
                st.session_state.lead_data['constitution_type'] = constitution
                if st.session_state.step == 6: st.session_state.step = 7

        # STEP 7: Age
        if st.session_state.step >= 7:
            age = st.number_input("8. What is the Age of the Business Owner?", min_value=0, max_value=100, step=1, key="age_input")
            if age > 0:
                st.session_state.lead_data['age'] = age
                if age < 18:
                     st.error("Applicant must be at least 18 years old.")
                elif age < 21 or age > 65:
                    st.warning("Co-applicant will be required due to age being outside the 21-65 range.")
                
                if age >= 18 and st.session_state.step == 7: 
                    st.session_state.step = 8

        # STEP 8: Gender
        if st.session_state.step >= 8:
            gender = st.selectbox("9. What is the Gender of the Business Owner?", ["", "Male", "Female", "Other"], key="gender_input")
            if gender:
                st.session_state.lead_data['gender'] = gender
                if st.session_state.step == 8: st.session_state.step = 9

        if st.session_state.step >= 9:
            ntc_status = st.selectbox("10. Is the customer New to Credit (NTC)?", ["", "Yes", "No"], key="ntc_input")
            if ntc_status:
                st.session_state.lead_data['is_ntc'] = (ntc_status == "Yes") 
                if st.session_state.step == 9: st.session_state.step = 10

        # STEP 9: Co-Applicant
        if st.session_state.step >= 10:
            is_female = st.session_state.lead_data.get('gender') == 'Female'
            age = st.session_state.lead_data.get('age', 30)
            is_age_out_of_range = age < 21 or age > 65
            needs_co_applicant = is_female or is_age_out_of_range

            if needs_co_applicant:
                st.subheader("Co-Applicant Details (Required)")
                if is_female:
                    st.info("Co-applicant required for female business owners.")
                if is_age_out_of_range:
                    st.info(f"Co-applicant required because age ({age}) is outside the 21-65 range.")
                
                co_name = st.text_input("Name", key="co_name_input")
                co_relation = st.text_input("Relationship", key="co_relation_input")
                
                if co_name and co_relation:
                    st.session_state.lead_data['co_applicant_details'] = {"name": co_name, "relationship": co_relation}
                    if st.session_state.step == 10: st.session_state.step = 11
                else:
                    st.warning("Please enter co-applicant name and relationship to proceed.") 
            
            elif st.session_state.step == 10: 
                st.session_state.lead_data['co_applicant_details'] = None
                st.session_state.step = 11

        # STEP 10: Turnover and Obligations
        if st.session_state.step >= 11:
            st.write("11. What is the Monthly Turnover?")
            t_col1, t_col2 = st.columns([2, 1])
            with t_col1:
                turnover_value = st.number_input("Value", min_value=0.0, format="%.2f", key="turnover_val_input", label_visibility="collapsed")
            with t_col2:
                turnover_unit = st.selectbox("Unit", utils.UNIT_OPTIONS, key="turnover_unit_input", label_visibility="collapsed")

            st.write("12. What are the Total Obligations?")
            o_col1, o_col2 = st.columns([2, 1])
            with o_col1:
                obligations_value = st.number_input("Value", min_value=0.0, format="%.2f", key="obligations_val_input", label_visibility="collapsed")
            with o_col2:
                obligations_unit = st.selectbox("Unit", utils.UNIT_OPTIONS, key="obligations_unit_input", label_visibility="collapsed")

            if turnover_value > 0 and turnover_unit and obligations_value >= 0 and obligations_unit:
                turnover = turnover_value * utils.UNITS[turnover_unit]
                obligations = obligations_value * utils.UNITS[obligations_unit]
                
                yearly_turnover = turnover * 12 
                st.session_state.lead_data['monthly_turnover'] = turnover
                st.session_state.lead_data['yearly_turnover'] = yearly_turnover
                st.session_state.lead_data['total_obligations'] = obligations
                
                foir = 0.0
                if turnover > 0:
                    foir = obligations / turnover
                st.session_state.lead_data['foir'] = foir
                
                st.info(f"Calculated Monthly Turnover: ₹{turnover:,.2f}")
                st.info(f"Calculated Total Obligations: ₹{obligations:,.2f}")
                
                col1, col2 = st.columns(2)
                col1.metric(label="Calculated Yearly Turnover", value=f"₹{yearly_turnover:,.2f}")
                col2.metric(label="Calculated FOIR", value=f"{foir:.2%}")
                
                if foir > 0.65:
                    st.warning("High FOIR! This may impact eligibility for most lenders.")
                if st.session_state.step == 11: 
                    st.session_state.step = 12
            elif (turnover_value > 0 or obligations_value > 0) and (not turnover_unit or not obligations_unit):
                st.error("Please select a unit (e.g., Lakhs) for both turnover and obligations.")

        # STEP 11: Profit
        if st.session_state.step >= 12:
            profit = st.number_input("12. What was the Net Profit as per ITR for the last financial year?", min_value=0.0, format="%.2f", key="profit_input")
            if profit > 0:
                st.session_state.lead_data['profit_last_year'] = profit
                if st.session_state.step == 12: st.session_state.step = 13
            elif 'profit_last_year' not in st.session_state.lead_data:
                st.session_state.lead_data['profit_last_year'] = 0.0
                if st.session_state.step == 12: st.session_state.step = 13

        # STEP 13: Requested Loan Type (NEW)
        if st.session_state.step >= 13:
            loan_type_display = st.selectbox(
                "13. What type of loan service are you looking for?",
                ["", "Term Loan", "DLOD", "OD", "Loan Against Property (LAP)"],
                key="loan_type_input"
            )
            if loan_type_display:
                if loan_type_display == "Loan Against Property (LAP)":
                    loan_type = "LAP"
                else:
                    loan_type = loan_type_display
                st.session_state.lead_data['requested_loan_type'] = loan_type
                st.session_state.eligibility_results = logic.check_eligibility(st.session_state.lead_data)
                if st.session_state.step == 13:
                    st.session_state.step = 14

        # STEP 14: Summary and Save (was previously step 13)
        if st.session_state.step == 14:
            st.success("All details captured! Please review the summary and eligibility on the right.")

            st.subheader("Remarks (optional)")
            st.write("Add any BDO notes or action items here — these will be saved with the lead.")
            remarks_input = st.text_area("Enter remarks for this lead:", value=st.session_state.lead_data.get('remarks',''), key="remarks_input", height=120)
            st.session_state.lead_data['remarks'] = remarks_input

            col_draft, col_save = st.columns([1,1])
            with col_draft:
                if st.button("💾 Save as Draft"):
                    ok = save_lead_to_storage(is_draft=True)
                    if ok:
                        st.success("Draft saved to data/leads.xlsx. You can continue later and load it using the mobile number.")
            with col_save:
                if st.button("✅ Save Lead (Final)"):
                    try:
                        st.session_state.eligibility_results = logic.check_eligibility(st.session_state.lead_data)
                        ok = save_lead_to_storage(is_draft=False)
                        if ok:
                            st.success(f"Lead for mobile number {st.session_state.lead_data.get('mobile_number')} saved successfully!")
                    except Exception as e:
                        st.error(f"An error occurred while saving the lead: {e}")

    # --- ELIGIBILITY BOARD (Right Column) ---
    with board_col:
        st.header("Lender Eligibility Board")
        
        if st.session_state.lead_data:
            st.session_state.eligibility_results = logic.check_eligibility(st.session_state.lead_data)
        
        if not st.session_state.eligibility_results:
            st.info("The board will update in real-time as you enter lead details.")
        
        for lender, result in st.session_state.eligibility_results.items():
            if result["eligible"]:
                st.success(f"🟢 {lender}: Eligible")
            else:
                with st.expander(f"🔴 {lender}: Not Eligible - Click to see why"):
                    for reason in result.get("reasons", []):
                        st.write(f"- {reason}")

            tips = result.get("tips", [])
            if tips:
                with st.expander(f"💡 {lender} — Tips / Possible Deviations (click to view)"):
                    for tip in tips:
                        st.info(tip)
        
        if st.session_state.step == 14:
            st.subheader("Final Lead Summary")
            st.json(st.session_state.lead_data)
            # Give user a download option for the single lead as excel
            # df_for_download = None
            # try:
            #     df_for_download = utils._read_all_leads()
            # except Exception:
            #     df_for_download = None
            # if df_for_download is not None:
            #     excel_bytes = utils.to_excel(df_for_download)
            #     st.download_button(
            #         label="📥 Download All Leads (Excel)",
            #         data=excel_bytes,
            #         file_name="leads.xlsx",
            #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            #     )
