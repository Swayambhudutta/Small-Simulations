
import streamlit as st
import matplotlib.pyplot as plt

# Set the title of the dashboard
st.title("🌍 Emissions Dashboard")

st.markdown("Enter your Scope 1, Scope 2, and Scope 3 emissions below (in **tCO2e**)")

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

# Input fields with progress bars
scope1 = input_with_progress("Scope 1 Emissions", "scope1")
scope2 = input_with_progress("Scope 2 Emissions", "scope2")
scope3 = input_with_progress("Scope 3 Emissions", "scope3")

# Check if all values are entered and valid
if scope1 and scope2 and scope3:
    try:
        s1 = float(scope1)
        s2 = float(scope2)
        s3 = float(scope3)

        emissions = [s1, s2, s3]
        labels = ["Scope 1", "Scope 2", "Scope 3"]
        colors = ["#FF5733", "#33C1FF", "#33FF99"]

        st.subheader("📊 Emissions Bar Chart")
        fig_bar, ax_bar = plt.subplots()
        ax_bar.bar(labels, emissions, color=colors)
        ax_bar.set_ylabel("Emissions (tCO2e)")
        ax_bar.set_title("Emissions by Scope")
        st.pyplot(fig_bar)

        st.subheader("🥧 Emissions Pie Chart")
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(emissions, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax_pie.axis('equal')
        st.pyplot(fig_pie)

    except ValueError:
        st.error("Please enter valid numeric values for all scopes.")
else:
    st.info("Please enter all three emission values to view the charts.")
