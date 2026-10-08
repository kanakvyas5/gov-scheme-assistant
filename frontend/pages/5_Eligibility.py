import streamlit as st

import api_client

st.set_page_config(page_title="Eligibility Check", page_icon="✅")
st.title("✅ Eligibility Check")

if not st.session_state.get("token"):
    st.warning("Please log in first (see the Login page in the sidebar).")
    st.stop()

schemes_data, error = api_client.list_schemes()
if error:
    st.error(error)
    st.stop()

if schemes_data["count"] == 0:
    st.info("No schemes are available to check yet.")
    st.stop()

scheme_options = {s["name"]: s["scheme_id"] for s in schemes_data["schemes"]}
selected_name = st.selectbox("Choose a scheme to check", list(scheme_options.keys()))

if st.button("Check My Eligibility"):
    scheme_id = scheme_options[selected_name]
    result, error = api_client.check_eligibility(scheme_id)

    if error:
        st.error(error)
        if "profile" in error.lower():
            st.info("Go to the Profile page to fill in your details first.")
    else:
        if result["eligible"]:
            st.success(f"🎉 You ARE eligible for **{result['scheme_name']}**!")
        else:
            st.error(f"You are NOT currently eligible for **{result['scheme_name']}**.")

        if result["matched_rules"]:
            st.subheader("✅ Requirements you meet")
            for rule in result["matched_rules"]:
                st.write(f"- {rule['field_name']} {rule['operator']} {rule['expected_value']} (your value: {rule['your_value']})")

        if result["failed_rules"]:
            st.subheader("❌ Requirements you don't meet")
            for rule in result["failed_rules"]:
                st.write(f"- {rule['reason']}")