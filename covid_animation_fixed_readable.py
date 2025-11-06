print("Preparing animation...")

# Create Year_Month column as period, then convert to timestamp
case_df['Year_Month'] = case_df['FILE_DATE'].dt.to_period('M').dt.to_timestamp()

# Group by PHU and month
monthly_data = case_df.groupby(['PHU_NUM', 'Year_Month']).agg({
    'PHU_NAME_STD': 'first',
    'TOTAL_CASES': 'last'
}).reset_index()

# ALTERNATIVE FIX: Keep human-readable format but add a sortable column
# Sort by the actual date, then create display labels
monthly_data = monthly_data.sort_values('Year_Month')
monthly_data['Date_Str'] = monthly_data['Year_Month'].dt.strftime('%B %Y')

# Create a categorical type with proper ordering to force chronological display
from pandas.api.types import CategoricalDtype
date_order = monthly_data['Date_Str'].unique()  # Already sorted by Year_Month above
cat_type = CategoricalDtype(categories=date_order, ordered=True)
monthly_data['Date_Str'] = monthly_data['Date_Str'].astype(cat_type)

# Merge with geographic data
temporal_gdf = phu_gdf[['PHU_ID', 'NAME_ENG', 'geometry']].merge(
    monthly_data, left_on='PHU_ID', right_on='PHU_NUM'
)

# Create the animated choropleth map
fig = px.choropleth_mapbox(
    temporal_gdf,
    geojson=temporal_gdf.geometry,
    locations=temporal_gdf.index,
    color='TOTAL_CASES',
    animation_frame='Date_Str',
    color_continuous_scale='Reds',
    mapbox_style="carto-positron",
    zoom=4.5,
    center={"lat": 50, "lon": -85},
    opacity=0.7,
    title='COVID-19 Temporal Evolution',
    category_orders={'Date_Str': list(date_order)}  # Explicitly set frame order
)

fig.update_layout(height=700, margin={"r":0,"t":50,"l":0,"b":0})
print("✓ Ready - press Play")
display(fig)
