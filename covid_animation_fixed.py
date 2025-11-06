print("Preparing animation...")

# Create Year_Month column as period, then convert to timestamp
case_df['Year_Month'] = case_df['FILE_DATE'].dt.to_period('M').dt.to_timestamp()

# Group by PHU and month
monthly_data = case_df.groupby(['PHU_NUM', 'Year_Month']).agg({
    'PHU_NAME_STD': 'first',
    'TOTAL_CASES': 'last'
}).reset_index()

# FIX: Use sortable date format (YYYY-MM) instead of month name
# This ensures chronological ordering in the animation
monthly_data['Date_Str'] = monthly_data['Year_Month'].dt.strftime('%Y-%m')

# OPTIONAL: Sort the data explicitly to ensure proper ordering
monthly_data = monthly_data.sort_values('Year_Month')

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
    title='COVID-19 Temporal Evolution'
)

fig.update_layout(height=700, margin={"r":0,"t":50,"l":0,"b":0})
print("✓ Ready - press Play")
display(fig)
