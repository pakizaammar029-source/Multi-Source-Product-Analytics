import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "processed" / "cleaned_products.csv"

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stMetric"] {
        background-color: #172033;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #263449;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    [data-testid="stMetricValue"] {
        color: #60a5fa;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
    }

    .dashboard-subtitle {
        color: #94a3b8;
        font-size: 15px;
    }

    div[data-testid="stTabs"] button {
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    numeric_columns = [
        "price",
        "rating",
        "discount_percentage"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()

df = load_data()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📊 Product Analytics")
st.sidebar.caption("Multi-Source E-Commerce Platform")

st.sidebar.divider()

st.sidebar.subheader("Dashboard Filters")

sources = sorted(df["data_source"].dropna().unique())
selected_sources = st.sidebar.multiselect(
    "Data Source",
    sources,
    default=sources
)

brands = sorted(df["brand"].dropna().unique())
selected_brands = st.sidebar.multiselect(
    "Brand",
    brands
)

categories = sorted(df["category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Category",
    categories
)

search = st.sidebar.text_input(
    "Search Product",
    placeholder="Enter product name..."
)

st.sidebar.divider()

if st.sidebar.button("🔄 Refresh Dashboard", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.caption("Data: DummyJSON + Open Beauty Facts")


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if selected_sources:
    filtered_df = filtered_df[
        filtered_df["data_source"].isin(selected_sources)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_brands:
    filtered_df = filtered_df[
        filtered_df["brand"].isin(selected_brands)
    ]

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["category"].isin(selected_categories)
    ]

if search:
    filtered_df = filtered_df[
        filtered_df["product_name"]
        .fillna("")
        .str.contains(search, case=False, na=False)
    ]


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("E-Commerce Product Intelligence")
st.markdown(
    '<p class="dashboard-subtitle">'
    'A multi-source platform for product analysis, '
    'pricing insights and data quality monitoring.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total_products = len(filtered_df)
total_brands = filtered_df["brand"].nunique()
total_categories = filtered_df["category"].nunique()

avg_rating = filtered_df["rating"].mean()
avg_price = filtered_df["price"].mean()
avg_discount = filtered_df["discount_percentage"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Products", f"{total_products:,}")
c2.metric("Unique Brands", f"{total_brands:,}")
c3.metric("Categories", f"{total_categories:,}")
c4.metric(
    "Average Rating",
    f"{avg_rating:.2f}/5" if pd.notna(avg_rating) else "N/A"
)

c5, c6 = st.columns(2)

c5.metric(
    "Average Price",
    f"${avg_price:,.2f}" if pd.notna(avg_price) else "N/A"
)

c6.metric(
    "Average Discount",
    f"{avg_discount:.2f}%" if pd.notna(avg_discount) else "N/A"
)

st.divider()


# --------------------------------------------------
# DASHBOARD TABS
# --------------------------------------------------

overview, analytics, explorer, quality = st.tabs([
    "📈 Overview",
    "📊 Analytics",
    "🔎 Product Explorer",
    "🛡️ Data Quality"
])


# --------------------------------------------------
# OVERVIEW TAB
# --------------------------------------------------

with overview:

    st.subheader("Dataset Overview")

    col1, col2 = st.columns(2)

    with col1:
        source_counts = filtered_df["data_source"].value_counts().reset_index()
        source_counts.columns = ["Data Source", "Products"]

        fig = px.pie(
            source_counts,
            names="Data Source",
            values="Products",
            hole=0.55,
            title="Products by Data Source",
            color_discrete_sequence=["#3b82f6", "#10b981"]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        brand_counts = (
            filtered_df["brand"]
            .dropna()
            .value_counts()
            .head(10)
            .reset_index()
        )

        brand_counts.columns = ["Brand", "Products"]

        fig = px.bar(
            brand_counts.sort_values("Products"),
            x="Products",
            y="Brand",
            orientation="h",
            title="Top 10 Brands",
            color="Products",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        rating_data = filtered_df.dropna(subset=["rating"])

        fig = px.histogram(
            rating_data,
            x="rating",
            nbins=15,
            title="Product Rating Distribution",
            color_discrete_sequence=["#8b5cf6"]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col4:
        discount_data = filtered_df.dropna(
            subset=["discount_percentage"]
        )

        fig = px.histogram(
            discount_data,
            x="discount_percentage",
            nbins=15,
            title="Discount Distribution",
            color_discrete_sequence=["#f59e0b"]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120"
        )

        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# ANALYTICS TAB
# --------------------------------------------------

with analytics:

    st.subheader("Advanced Product Analytics")

    dummy_df = filtered_df[
        filtered_df["data_source"] == "DummyJSON"
    ].copy()

    col1, col2 = st.columns(2)

    with col1:
        category_prices = (
            dummy_df.dropna(subset=["price", "category"])
            .groupby("category")
            .agg(
                Average_Price=("price", "mean"),
                Product_Count=("product_id", "count")
            )
            .reset_index()
        )

        category_prices = category_prices[
            category_prices["Product_Count"] >= 2
        ].nlargest(10, "Average_Price")

        fig = px.bar(
            category_prices.sort_values("Average_Price"),
            x="Average_Price",
            y="category",
            orientation="h",
            title="Average Price by Category (DummyJSON)",
            labels={
                "Average_Price": "Average Price",
                "category": "Category"
            },
            color="Average_Price",
            color_continuous_scale="Viridis"
        )

        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        price_rating = dummy_df.dropna(
            subset=["price", "rating"]
        )

        fig = px.scatter(
            price_rating,
            x="price",
            y="rating",
            hover_name="product_name",
            title="Price vs Product Rating",
            color="category",
            labels={
                "price": "Price",
                "rating": "Rating"
            }
        )

        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Statistical Summary")

    numeric_data = filtered_df[
        ["price", "rating", "discount_percentage"]
    ].describe().T

    st.dataframe(
        numeric_data,
        use_container_width=True
    )

    st.subheader("Correlation Analysis")

    correlation_data = dummy_df[
        ["price", "rating", "discount_percentage"]
    ].corr()

    fig = px.imshow(
        correlation_data,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        title="Price, Rating and Discount Correlation"
    )

    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# PRODUCT EXPLORER TAB
# --------------------------------------------------

with explorer:

    st.subheader("Explore Product Dataset")

    st.caption(
        f"Showing {len(filtered_df)} products based on selected filters."
    )

    display_columns = [
        "product_name",
        "brand",
        "category",
        "price",
        "rating",
        "discount_percentage",
        "data_source"
    ]

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Products CSV",
        data=csv_data,
        file_name="filtered_products.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# DATA QUALITY TAB
# --------------------------------------------------

with quality:

    st.subheader("Data Quality Monitoring")

    missing = filtered_df.isnull().sum()

    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values,
        "Missing Percentage": (
            missing.values / max(len(filtered_df), 1) * 100
        ).round(2)
    })

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Missing Cells",
            f"{int(missing.sum()):,}"
        )

    with col2:
        completeness = (
            100 - (missing.sum() / max(filtered_df.size, 1) * 100)
        )

        st.metric(
            "Data Completeness",
            f"{completeness:.2f}%"
        )

    fig = px.bar(
        missing_df,
        x="Column",
        y="Missing Percentage",
        title="Missing Values by Column",
        color="Missing Percentage",
        color_continuous_scale="Reds"
    )

    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True
    )

    duplicate_count = filtered_df.duplicated(
        subset=["data_source", "product_id"]
    ).sum()

    st.metric(
        "Duplicate Product Records",
        int(duplicate_count)
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<center style='color:#64748b;'>"
    "Multi-Source E-Commerce Product Analytics | "
    "Built with Python, Pandas, Plotly & Streamlit"
    "</center>",
    unsafe_allow_html=True
)


