import pandas as pd
import streamlit as st
import altair as alt
import os
import matplotlib.pyplot as plt

try:
    import geopandas as gpd
    HAS_GPD = True
except Exception:
    HAS_GPD = False

from state_utils import normalize_state_names

st.set_page_config(page_title="Silver Price Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>Silver Price Calculator & Sales Dashboard</h1><p>R.Karan RegNo: 2547241 Class 3MCA-B</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Price Calculator", "Historical Prices", "State-wise Sales", "January Trends"])


with tab1:
    st.markdown("### Silver Price Calculator")
    st.write("Calculate the cost of your silver purchase instantly!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Input Parameters**")
        unit = st.radio("Unit", ["grams", "kilograms"], horizontal=True)
        if unit == "kilograms":
            weight = st.slider("Weight of silver (kg)", min_value=0.0, max_value=100.0, value=1.0, step=0.1)
        else:
            weight = st.slider("Weight of silver (grams)", min_value=0.0, max_value=1000.0, value=100.0, step=1.0)
        price_per_gram = st.slider("Current price per gram (INR)", min_value=50.0, max_value=150.0, value=75.0, step=1.0)
    
    with col2:
        st.markdown("**Currency Conversion**")
        currency = st.selectbox("Convert to", ["INR", "USD", "EUR", "GBP", "AUD"])
        
        currency_rates = {
            "INR": 1.0,
            "USD": 0.012,
            "EUR": 0.011,
            "GBP": 0.0095,
            "AUD": 0.018
        }
        fx_rate = currency_rates.get(currency, 1.0)
    
    weight_in_grams = weight * 1000 if unit == "kilograms" else weight
    total_cost_inr = weight_in_grams * price_per_gram
    total_cost_converted = total_cost_inr * fx_rate
    
    st.divider()
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Weight (grams)", f"{weight_in_grams:,.2f} g", delta=f"{weight_in_grams/1000:.2f} kg")
    col_m2.metric("Total Cost (INR)", f"Rs {total_cost_inr:,.2f}", delta=f"+{price_per_gram:.2f}/gram")
    col_m3.metric(f"Total Cost ({currency})", f"{total_cost_converted:,.2f}", delta=f"@{fx_rate}")
    
    st.success(f"At Rs{price_per_gram}/gram, {weight_in_grams:,.0f}g costs Rs{total_cost_inr:,.2f}")
    
    with st.expander("See price breakdown"):
        breakdown = pd.DataFrame({
            "Description": ["Weight", "Price per gram", "Total (INR)", f"Converted ({currency})"],
            "Value": [f"{weight_in_grams:,.2f} g", f"Rs {price_per_gram:,.2f}", f"Rs {total_cost_inr:,.2f}", f"{total_cost_converted:,.2f}"]
        })
        st.dataframe(breakdown, use_container_width=True, hide_index=True)


with tab2:
    st.markdown("### Historical Silver Price Trends")
    st.write("Track silver price movements over time with interactive filters!")
    
    col_filter1, col_filter2 = st.columns([2, 1])
    
    with col_filter1:
        price_filter = st.selectbox(
            "Filter by price range (INR/kg)",
            ["All", "Less than or equal to 20000", "Between 20000 and 30000", "Greater than or equal to 30000"],
            key="price_filter"
        )
    
    with col_filter2:
        show_stats = st.checkbox("Show Statistics", value=True)
    
    hist_csv_path = "historical_silver_price.csv"

    if os.path.exists(hist_csv_path):
        hist_raw = pd.read_csv(hist_csv_path)
        hist = pd.DataFrame({
            "Date": pd.to_datetime(hist_raw["Year"].astype(str) + "-" + hist_raw["Month"], format="%Y-%b"),
            "Price_INR_per_kg": hist_raw["Silver_Price_INR_per_kg"]
        })
    else:
        st.error(f"File not found: {hist_csv_path}")
        st.info("Please ensure the CSV file is in the same directory as this script.")
        dates = pd.date_range(start='2023-01-01', end='2024-01-30', freq='D')
        prices = [18000 + i*5 + (i%7)*500 for i in range(len(dates))]
        hist = pd.DataFrame({"Date": dates, "Price_INR_per_kg": prices})
    
    if price_filter == "Less than or equal to 20000":
        hist_filtered = hist[hist["Price_INR_per_kg"] <= 20000]
    elif price_filter == "Between 20000 and 30000":
        hist_filtered = hist[(hist["Price_INR_per_kg"] > 20000) & (hist["Price_INR_per_kg"] < 30000)]
    elif price_filter == "Greater than or equal to 30000":
        hist_filtered = hist[hist["Price_INR_per_kg"] >= 30000]
    else:
        hist_filtered = hist
    
    chart = alt.Chart(hist_filtered).mark_line(point=True, color='#FF6B6B', size=3).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Price_INR_per_kg:Q", title="Price (INR/kg)", scale=alt.Scale(zero=False)),
        tooltip=["Date:T", alt.Tooltip("Price_INR_per_kg:Q", format=",.0f")]
    ).properties(height=400, width=900).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    if show_stats:
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("Max Price", f"Rs {hist_filtered['Price_INR_per_kg'].max():,.0f}")
        col_s2.metric("Min Price", f"Rs {hist_filtered['Price_INR_per_kg'].min():,.0f}")
        col_s3.metric("Avg Price", f"Rs {hist_filtered['Price_INR_per_kg'].mean():,.0f}")
        col_s4.metric("Price Range", f"Rs {hist_filtered['Price_INR_per_kg'].max() - hist_filtered['Price_INR_per_kg'].min():,.0f}")


with tab3:
    st.markdown("### State-wise Silver Purchases Dashboard")
    st.write("Explore regional silver consumption patterns across India!")
    
    csv_path = "state_wise_silver_purchased_kg.csv"
    
    if os.path.exists(csv_path):
        state_df = pd.read_csv(csv_path)
        st.success(f"Loaded {len(state_df)} states from dataset")
    else:
        st.error(f"File not found: {csv_path}")
        st.info("Please ensure the CSV file is in the same directory as this script.")
        state_df = pd.DataFrame({
            "State": ["Rajasthan", "Gujarat", "Karnataka", "Telangana", "Maharashtra", 
                      "Uttar Pradesh", "Delhi", "Tamil Nadu", "Punjab", "Bihar"],
            "Silver_Purchased_kg": [2500, 2200, 1800, 1600, 1400, 1200, 1100, 950, 850, 700]
        })
    
    col_info1, col_info2, col_info3 = st.columns(3)
    col_info1.metric("Total Purchases", f"{state_df['Silver_Purchased_kg'].sum():,.0f} kg", delta="All states")
    col_info2.metric("Top State", state_df.sort_values('Silver_Purchased_kg', ascending=False).iloc[0]['State'], delta="Highest")
    col_info3.metric("Avg per State", f"{state_df['Silver_Purchased_kg'].mean():,.0f} kg", delta="Average")
    
    st.divider()

    tab3_1, tab3_2, tab3_3 = st.tabs(["Data Table", "Top 5 Chart", "Map"])
    
    with tab3_1:
        st.markdown("**State-wise Data Table**")
        sorted_state_df = state_df.sort_values('Silver_Purchased_kg', ascending=False)
        
        search_state = st.text_input("Search state", placeholder="Type state name...")
        if search_state:
            sorted_state_df = sorted_state_df[sorted_state_df['State'].str.contains(search_state, case=False, regex=False)]
        
        st.dataframe(sorted_state_df, use_container_width=True, hide_index=True)
    
    with tab3_2:
        st.markdown("**Top 5 States by Silver Purchases**")
        top5 = state_df.sort_values("Silver_Purchased_kg", ascending=False).head(5)
        
        bar = alt.Chart(top5).mark_bar(color='#4ECDC4').encode(
            x=alt.X("Silver_Purchased_kg:Q", title="Silver Purchased (kg)"),
            y=alt.Y("State:N", sort="-x", title="State"),
            tooltip=["State", alt.Tooltip("Silver_Purchased_kg:Q", format=",.0f")]
        ).properties(height=350).interactive()
        st.altair_chart(bar, use_container_width=True)
        
        st.markdown("**Key Insights**")
        top_state = state_df.loc[state_df['Silver_Purchased_kg'].idxmax()]
        bottom_state = state_df.loc[state_df['Silver_Purchased_kg'].idxmin()]
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        insight_col1.success(f"Highest: {top_state['State']}\n{top_state['Silver_Purchased_kg']:.0f} kg")
        insight_col2.warning(f"Lowest: {bottom_state['State']}\n{bottom_state['Silver_Purchased_kg']:.0f} kg")
        insight_col3.info(f"Difference:\n{top_state['Silver_Purchased_kg'] - bottom_state['Silver_Purchased_kg']:.0f} kg")
    
    with tab3_3:
        if HAS_GPD:
            st.markdown("**Geo Map Visualization**")
            st.write("Uses the bundled `india_state_geo.json` by default, with darker shades representing higher purchases. Upload your own GeoJSON to override it.")

            geo_file = st.file_uploader("Upload India States GeoJSON (optional)", type=["geojson", "json"], key="geo_upload")

            default_geo_path = "india_state_geo.json"
            geo_source = geo_file if geo_file else (default_geo_path if os.path.exists(default_geo_path) else None)

            if geo_source:
                try:
                    gdf = gpd.read_file(geo_source)
                    
                    st.write("**Available columns in GeoJSON:**")
                    st.write(gdf.columns.tolist())
                    
                    state_col = st.selectbox("Select State column from GeoJSON", gdf.columns.tolist())
                    
                    # Normalize state names on both sides so alternate/legacy
                    # spellings in the GeoJSON line up with the CSV.
                    gdf[state_col] = normalize_state_names(gdf[state_col])
                    state_df_copy = state_df.copy()
                    state_df_copy['State'] = normalize_state_names(state_df_copy['State'])
                    
                    # Show sample data for debugging
                    with st.expander("View GeoJSON state names"):
                        st.write(sorted(gdf[state_col].unique()))
                    
                    with st.expander("View CSV state names"):
                        st.write(sorted(state_df_copy['State'].unique()))
                    
                    # Merge the dataframes
                    merged = gdf.merge(state_df_copy, left_on=state_col, right_on="State", how="left")
                    
                    # Check if merge was successful
                    matched = merged['Silver_Purchased_kg'].notna().sum()
                    total = len(merged)
                    st.write(f"**Matched states:** {matched} out of {total}")
                    
                    if matched == 0:
                        st.warning("No states matched! Please check state names in both files.")
                    
                    # Create the map
                    fig, ax = plt.subplots(figsize=(16, 12))
                    
                    merged.plot(
                        column="Silver_Purchased_kg",
                        ax=ax,
                        cmap="YlOrRd",
                        edgecolor="black",
                        linewidth=0.8,
                        legend=True,
                        legend_kwds={
                            "label": "Silver Purchased (kg)",
                            "orientation": "vertical",
                            "shrink": 0.8,
                            "pad": 0.05
                        },
                        missing_kwds={
                            'color': 'lightgrey',
                            'edgecolor': 'black',
                            'hatch': '///',
                            'label': 'No data'
                        }
                    )
                    
                    # Add state labels
                    for idx, row in merged.iterrows():
                        if pd.notna(row['Silver_Purchased_kg']):
                            centroid = row.geometry.centroid
                            ax.text(
                                centroid.x, centroid.y, 
                                f"{row[state_col]}\n{row['Silver_Purchased_kg']:.0f} kg",
                                fontsize=6, ha='center', va='center',
                                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
                            )
                    
                    ax.set_title("India State-wise Silver Purchases\n(Darker Red = Higher Purchases)", 
                           fontsize=16, fontweight="bold", pad=20)
                    ax.axis("off")
                    plt.tight_layout()
                    
                    st.pyplot(fig)
                    
                    # Color scale explanation
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info("🟡 Light Yellow/Orange = Lower purchases")
                    with col2:
                        st.info("🔴 Dark Red = Higher purchases")
                    
                    st.success("✓ Map generated successfully! Darker shades represent higher silver purchases.")
                    
                    # Show unmatched states
                    if matched < total:
                        unmatched = merged[merged['Silver_Purchased_kg'].isna()][state_col].tolist()
                        with st.expander(f"⚠️ Unmatched states ({total - matched})"):
                            st.write(unmatched)
                
                except Exception as e:
                    st.error(f"Error loading GeoJSON: {str(e)}")
                    st.write("**Troubleshooting tips:**")
                    st.write("1. Make sure state names in CSV match the GeoJSON")
                    st.write("2. Check if the selected column contains state names")
                    st.write("3. Try a different column from the dropdown")
                    st.write("4. Ensure the GeoJSON file is properly formatted")
            else:
                st.info("📌 No bundled GeoJSON found — upload a GeoJSON file of India states to see the choropleth map")
                st.write("**Expected format:** GeoJSON file with state boundaries and a column containing state names")
        else:
            st.warning("GeoPandas not installed. Install with: pip install geopandas matplotlib")


with tab4:
    st.markdown("### January Monthly Silver Purchases Trend")
    st.write("Track daily silver purchase trends for January with interactive visualizations!")
    
    jan_data = pd.DataFrame({
        "Day": range(1, 32),
        "Silver_Purchased_kg": [120, 135, 128, 142, 155, 148, 160, 175, 182, 165,
                                170, 185, 192, 188, 195, 205, 210, 198, 215, 220,
                                225, 235, 240, 230, 245, 250, 255, 260, 248, 270, 275]
    })
    
    col_jan1, col_jan2, col_jan3, col_jan4 = st.columns(4)
    col_jan1.metric("Total (January)", f"{jan_data['Silver_Purchased_kg'].sum():,.0f} kg", delta="All days")
    col_jan2.metric("Highest Day", f"Day {jan_data.loc[jan_data['Silver_Purchased_kg'].idxmax(), 'Day']:.0f}", delta=f"{jan_data['Silver_Purchased_kg'].max():.0f} kg")
    col_jan3.metric("Daily Avg", f"{jan_data['Silver_Purchased_kg'].mean():,.1f} kg", delta="Average")
    col_jan4.metric("Lowest Day", f"Day {jan_data.loc[jan_data['Silver_Purchased_kg'].idxmin(), 'Day']:.0f}", delta=f"{jan_data['Silver_Purchased_kg'].min():.0f} kg")
    
    st.divider()
    
    tab4_1, tab4_2, tab4_3 = st.tabs(["Data Table", "Line Chart", "Analysis"])
    
    with tab4_1:
        st.markdown("**Daily Breakdown**")
        st.dataframe(jan_data, use_container_width=True, hide_index=True)
    
    with tab4_2:
        st.markdown("**Daily Trend Line**")
        line = alt.Chart(jan_data).mark_line(point=True, color='#95E1D3', size=3).encode(
            x=alt.X("Day:Q", title="Day of January"),
            y=alt.Y("Silver_Purchased_kg:Q", title="Silver Purchased (kg)"),
            tooltip=["Day", alt.Tooltip("Silver_Purchased_kg:Q", format=",.0f")]
        ).properties(height=400).interactive()
        st.altair_chart(line, use_container_width=True)
        
        st.markdown("**Cumulative Silver Purchases**")
        jan_data['Cumulative'] = jan_data['Silver_Purchased_kg'].cumsum()
        area = alt.Chart(jan_data).mark_area(color='#FFB6C1', opacity=0.5).encode(
            x=alt.X("Day:Q", title="Day of January"),
            y=alt.Y("Cumulative:Q", title="Cumulative (kg)"),
            tooltip=["Day", alt.Tooltip("Cumulative:Q", format=",.0f")]
        ).properties(height=350).interactive()
        st.altair_chart(area, use_container_width=True)
    
    with tab4_3:
        st.markdown("**Daily Statistics**")
        
        week_1 = jan_data[jan_data['Day'] <= 7]['Silver_Purchased_kg'].sum()
        week_2 = jan_data[(jan_data['Day'] > 7) & (jan_data['Day'] <= 14)]['Silver_Purchased_kg'].sum()
        week_3 = jan_data[(jan_data['Day'] > 14) & (jan_data['Day'] <= 21)]['Silver_Purchased_kg'].sum()
        week_4 = jan_data[jan_data['Day'] > 21]['Silver_Purchased_kg'].sum()
        
        st.write("**Weekly Breakdown:**")
        weekly_data = pd.DataFrame({
            "Week": ["Week 1 (1-7)", "Week 2 (8-14)", "Week 3 (15-21)", "Week 4 (22-31)"],
            "Total (kg)": [week_1, week_2, week_3, week_4]
        })
        st.dataframe(weekly_data, use_container_width=True, hide_index=True)
        
        week_chart = alt.Chart(weekly_data).mark_bar(color='#667eea').encode(
            x=alt.X("Week:N", title="Week"),
            y=alt.Y("Total (kg):Q", title="Silver Purchased (kg)"),
            tooltip=["Week", "Total (kg)"]
        ).properties(height=300).interactive()
        st.altair_chart(week_chart, use_container_width=True)
        
        best_week = weekly_data.loc[weekly_data["Total (kg)"].idxmax()]

        col_growth1, col_growth2 = st.columns(2)
        col_growth1.metric("Growth (Week 1 to Week 4)", f"{week_4 - week_1:.0f} kg", delta=f"{((week_4 - week_1) / week_1 * 100):.1f}%")
        col_growth2.metric("Best Week", best_week["Week"], delta=f"{best_week['Total (kg)']:.0f} kg")