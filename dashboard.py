import streamlit as st
import pandas as pd
import numpy as np

# Set up the ACME hierarchical structure
portfolios = ["Skin/Body", "Fragrance + Color Cosmetics", "Hair/APDO"]
geographies = ["North America", "Europe", "South America", "Asia"]
categories = ["Fragrance", "Hair Dye", "Face Make-Up", "Make-Up Brushes", "Tools"]
brands = ["Bobbi Brown", "Elizabeth Arden", "Aveda", "Kilian", "Frederic Malle", "Balmain"]
segments = ["Lipstick", "Mascara", "Toner", "Bronzer", "Hair Dye", "Face Make-Up", "Make-Up Brushes", "Tools"]

# Generate synthetic data
np.random.seed(42)
num_segments = len(segments)
initial_sales = np.random.randint(1_000_000, 15_000_000, size=num_segments)
margin = np.random.uniform(0.05, 0.3, size=num_segments)
trend = np.random.uniform(-0.02, 0.05, size=num_segments)
contribution = np.random.uniform(0.05, 0.3, size=num_segments)

# Normalize contributions
contribution /= contribution.sum()

structured_data = pd.DataFrame({
    "Portfolio": np.random.choice(portfolios, num_segments),
    "Geography": np.random.choice(geographies, num_segments),
    "Category": np.random.choice(categories, num_segments),
    "Brand": np.random.choice(brands, num_segments),
    "Segment": segments,
    "Initial Sales": initial_sales,
    "Margin": margin,
    "Trend": trend,
    "Contribution": contribution
})

# Streamlit Sidebar - User Input for Constraints
st.sidebar.header("Adjust Constraints")
trend_min = st.sidebar.slider("Min Trend Growth (%)", -5, 0, -2) / 100
trend_max = st.sidebar.slider("Max Trend Growth (%)", 0, 10, 5) / 100
contribution_min = st.sidebar.slider("Min Contribution (%)", 1, 10, 5) / 100
contribution_max = st.sidebar.slider("Max Contribution (%)", 10, 50, 30) / 100
sales_target = st.sidebar.number_input("Sales Target ($)", 50000000, 500000000, 100000000)
margin_target = st.sidebar.slider("Margin Target (%)", 0, 50, 5) / 100

# Apply constraints dynamically
structured_data["Max Growth Factor"] = np.clip(1 + structured_data["Trend"], 1 + trend_min, 1 + trend_max)
structured_data["Max Contribution"] = np.clip(structured_data["Contribution"], contribution_min, contribution_max)
structured_data["Max Sales"] = structured_data["Initial Sales"] * structured_data["Max Growth Factor"]

# Compute contribution at each level
structured_data["Brand Sales"] = structured_data.groupby("Brand")["Initial Sales"].transform("sum")
structured_data["Category Sales"] = structured_data.groupby("Category")["Initial Sales"].transform("sum")
structured_data["Geography Sales"] = structured_data.groupby("Geography")["Initial Sales"].transform("sum")
structured_data["Portfolio Sales"] = structured_data.groupby("Portfolio")["Initial Sales"].transform("sum")

# Display Results
st.title("📊 ACME Business Optimization Dashboard")
st.write("This dashboard allows you to adjust constraints and analyze ACME’s sales and margin growth.")

st.subheader("1️⃣ Sales & Margin Data with Constraints Applied")
st.dataframe(structured_data[["Portfolio", "Geography", "Category", "Brand", "Segment", "Initial Sales", "Max Sales", "Margin", "Max Contribution"]])

# Sales Growth Over Time (5-Year Projection)
st.subheader("2️⃣ Sales Growth Over 5 Years")
years = [1, 2, 3, 4, 5]
sales_projection = structured_data["Initial Sales"].values[:, None] * (1 + structured_data["Trend"].values[:, None]) ** np.array(years)
sales_projection_df = pd.DataFrame(sales_projection, columns=[f"Year {i}" for i in years], index=structured_data["Segment"])
st.line_chart(sales_projection_df.T)

# Contribution Breakdown Pie Chart
st.subheader("3️⃣ Contribution Breakdown")
st.write("How each segment contributes to total sales.")
import plotly.express as px

# Pie Chart for Contribution Breakdown
st.subheader("3️⃣ Contribution Breakdown")
fig = px.pie(structured_data, names="Segment", values="Max Contribution", title="Contribution by Segment")
st.plotly_chart(fig)

# Sales vs. Maximized Sales Bar Chart
st.subheader("4️⃣ Initial vs. Maximized Sales")
st.bar_chart(structured_data.set_index("Segment")[["Initial Sales", "Max Sales"]])

st.success("✅ Adjust the constraints in the sidebar to dynamically update the business projections!")

