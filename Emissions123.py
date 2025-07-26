import streamlit as st
import pandas as pd

# Set the title of the dashboard
st.title("🌍 Emissions Dashboard")

# Sidebar navigation
view = st.sidebar.radio("Select View", ["Current Year Summary", "Yearly Trend Analysis"])

# Function to show progress bar beside input
def input_with_progress(label, key):
    col1, col2 = st.columns([3, 1])
    with col1:
        value = st.text_input(f"{label} (tCO2e)", key=key)
    with col2:
        if value:
            progress = min(len(value) / 10, 1.0)
            st.progress(progress)
            if progress == 1.0:
                st.caption("✅ Complete")
        else:
            st.caption("⏳ Waiting...")
    return value

# -------------------- TAB 1 --------------------
if view == "Current Year Summary":
    st.markdown("### Enter your Scope 1, Scope 2, and Scope 3 emissions below (in **tCO2e**)")

    scope1 = input_with_progress("Scope 1 Emissions", "scope1")
    scope2 = input_with_progress("Scope 2 Emissions", "scope2")
    scope3 = input_with_progress("Scope 3 Emissions", "scope3")

    if scope1 and scope2 and scope3:
        try:
            s1 = float(scope1)
            s2 = float(scope2)
            s3 = float(scope3)

            emissions_data = pd.DataFrame({
                "Scope": ["Scope 1", "Scope 2", "Scope 3"],
                "Emissions (tCO2e)": [s1, s2, s3]
            })

            st.subheader("📊 Emissions Bar Chart")
            st.bar_chart(emissions_data.set_index("Scope"))

            st.subheader("🥧 Emissions Pie Chart (Text Summary)")
            total = s1 + s2 + s3
            percentages = [s1 / total * 100, s2 / total * 100, s3 / total * 100]
            pie_chart_text = "\n".join(
                f"{label}: {percent:.1f}%" for label, percent in zip(["Scope 1", "Scope 2", "Scope 3"], percentages)
            )
            st.text(pie_chart_text)

        except ValueError:
            st.error("Please enter valid numeric values for all scopes.")
    else:
        st.info("Please enter all three emission values to view the charts.")

# -------------------- TAB 2 --------------------
elif view == "Yearly Trend Analysis":
    st.header("📈 Yearly Emissions Trend")

    years = st.multiselect("Select years to enter data for", options=[2020, 2021, 2022, 2023, 2024], default=[2020, 2021, 2022, 2023, 2024])

    if years:
        scope1_trend = []
        scope2_trend = []
        scope3_trend = []

        st.subheader("Enter yearly emissions for each scope (in tCO2e)")
        for year in years:
            col1, col2, col3 = st.columns(3)
            with col1:
                val1 = st.number_input(f"Scope 1 - {year}", key=f"s1_{year}", min_value=0.0)
                scope1_trend.append(val1)
            with col2:
                val2 = st.number_input(f"Scope 2 - {year}", key=f"s2_{year}", min_value=0.0)
                scope2_trend.append(val2)
            with col3:
                val3 = st.number_input(f"Scope 3 - {year}", key=f"s3_{year}", min_value=0.0)
                scope3_trend.append(val3)

        trend_df = pd.DataFrame({
            "Year": years,
            "Scope 1": scope1_trend,
            "Scope 2": scope2_trend,
            "Scope 3": scope3_trend
        }).set_index("Year")

        st.subheader("📉 Scope 1 Emissions Trend")
        st.line_chart(trend_df[["Scope 1"]])

        st.subheader("📉 Scope 2 Emissions Trend")
        st.line_chart(trend_df[["Scope 2"]])

        st.subheader("📉 Scope 3 Emissions Trend")
        st.line_chart(trend_df[["Scope 3"]])
