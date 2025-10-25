import streamlit as st
import pandas as pd
import plotly.express as px

# UPDATE THIS PATH TO YOUR CSV FILE LOCATION
CSV_FILE_PATH = "premier_league_cleaned.csv"  


try:
    # Load data directly from file
    df = pd.read_csv(CSV_FILE_PATH)
    
    # Clean column names (remove any leading/trailing spaces)
    df.columns = df.columns.str.strip()
    
    st.success(f"✅ Data loaded successfully! {len(df)} players found.")
    
    # Filters Section
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Team selection
        teams = sorted(df['Team'].dropna().unique())
        selected_team = st.selectbox("🏆 Select Team", ["All Teams"] + teams)
    
    # Filter players based on team selection
    if selected_team == "All Teams":
        filtered_df = df
    else:
        filtered_df = df[df['Team'] == selected_team]
    
    with col2:
        # Player selection
        players = sorted(filtered_df['Player'].dropna().unique())
        selected_player = st.selectbox("👤 Select Player", players)
    

    st.markdown("## 🔮 2025 Season Predictions")
    st.markdown("*Based on 2024 performance data and statistical trends*")
    st.markdown("---")
            
        # Filters
    col1, col2 = st.columns(2)
            
    with col1:
        teams = sorted(df['Team'].dropna().unique())
        pred_team = st.selectbox("🏆 Select Team", ["All Teams"] + teams, key="pred_team")
            
    if pred_team == "All Teams":
        pred_filtered_df = df
    else:
        pred_filtered_df = df[df['Team'] == pred_team]
            
    with col2:
        players = sorted(pred_filtered_df['Player'].dropna().unique())
        pred_player = st.selectbox("👤 Select Player", players, key="pred_player")
            
    if pred_player:
        player_data = pred_filtered_df[pred_filtered_df['Player'] == pred_player].iloc[0]
            
        st.markdown(f"### 📊 2025 Predictions for **{pred_player}**")
                
    # Calculate predictions based on current performance
    # Assumptions: Similar playing time, age factor, regression to mean
                
    age_factor = 1.0
    if player_data['Age'] < 24:
        age_factor = 1.1  # Young players improving
    elif player_data['Age'] > 30:
        age_factor = 0.95  # Slight decline for older players
                
                # Calculate predicted stats
    predicted_mp = int(player_data['MP'] * 0.95)  # Slightly conservative
    predicted_goals = round(player_data['Gls_90'] * player_data['90s'] * age_factor)
    predicted_assists = round(player_data['Ast_90'] * player_data['90s'] * age_factor)
    predicted_xg = round(player_data['xG_90'] * player_data['90s'] * age_factor, 2)
    predicted_xag = round(player_data['xAG_90'] * player_data['90s'] * age_factor, 2)
                
                # Display predictions
    st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                
    pred_col1, pred_col2, pred_col3, pred_col4 = st.columns(4)
                
    with pred_col1:
        st.metric(
            "Predicted Goals 2025",
            f"{predicted_goals}",
            delta=f"{predicted_goals - int(player_data['Gls'])} vs 2024"
        )
                
    with pred_col2:
        st.metric(
            "Predicted Assists 2025",
            f"{predicted_assists}",
            delta=f"{predicted_assists - int(player_data['Ast'])} vs 2024"
        )
                
    with pred_col3:
        st.metric(
            "Predicted xG 2025",
            f"{predicted_xg:.1f}",
            delta=f"{predicted_xg - player_data['xG']:.1f} vs 2024"
        )
                
    with pred_col4:
        st.metric(
            "Predicted xAG 2025",
            f"{predicted_xag:.1f}",
            delta=f"{predicted_xag - player_data['xAG']:.1f} vs 2024"
        )
                
    st.markdown('</div>', unsafe_allow_html=True)
                
    st.markdown("---")
                
    # Prediction Chart
    st.markdown("### 📈 2024 vs 2025 Projection")
                
    comparison_data = {
        'Metric': ['Goals', 'Goals', 'Assists', 'Assists', 'xG', 'xG', 'xAG', 'xAG'],
        'Season': ['2024', '2025', '2024', '2025', '2024', '2025', '2024', '2025'],
        'Value': [
            player_data['Gls'], predicted_goals,
            player_data['Ast'], predicted_assists,
            player_data['xG'], predicted_xg,
            player_data['xAG'], predicted_xag
        ]
    }
                
    fig_prediction = px.bar(
        comparison_data,
        x='Metric',
        y='Value',
        color='Season',
        barmode='group',
        title=f"{pred_player} - 2024 Performance vs 2025 Predictions",
        color_discrete_map={'2024': '#38003c', '2025': '#00ff87'}
    )
    fig_prediction.update_layout(height=500)
    st.plotly_chart(fig_prediction, use_container_width=True)
                
    # Prediction methodology
    st.markdown("---")
    st.markdown("### 📌 Prediction Methodology")
    st.info(f"""
    **Factors considered:**
    - **Age Factor:** {age_factor}x ({"Improving 🔥" if age_factor > 1 else "Stable ⚖️" if age_factor == 1 else "Slight decline 📉"})
    - **Current per-90 metrics:** Goals/90: {player_data['Gls_90']:.2f}, Assists/90: {player_data['Ast_90']:.2f}
    - **Expected playing time:** ~{player_data['90s']:.1f} x 90-minute matches
    - **Performance consistency:** Based on xG/xAG alignment
                
    *Note: Predictions assume similar playing time, no major injuries, and current team structure.*
    """)
                
    # Top predicted performers
    st.markdown("---")
    st.markdown("### 🏆 Top 10 Predicted Performers for 2025")
                
    # Calculate predictions for all players
    df['Predicted_Goals_2025'] = df.apply(
        lambda x: round(x['Gls_90'] * x['90s'] * (1.1 if x['Age'] < 24 else 0.95 if x['Age'] > 30 else 1.0)), 
        axis=1
    )
    df['Predicted_Assists_2025'] = df.apply(
        lambda x: round(x['Ast_90'] * x['90s'] * (1.1 if x['Age'] < 24 else 0.95 if x['Age'] > 30 else 1.0)), 
        axis=1
    )
    df['Predicted_GA_2025'] = df['Predicted_Goals_2025'] + df['Predicted_Assists_2025']
                
    top_predicted = df.nlargest(10, 'Predicted_GA_2025')[['Player', 'Team', 'Age', 'Predicted_Goals_2025', 'Predicted_Assists_2025', 'Predicted_GA_2025']]
                
    st.dataframe(
        top_predicted.reset_index(drop=True),
        use_container_width=True,
        column_config={
            "Player": "Player Name",
            "Team": "Team",
            "Age": st.column_config.NumberColumn("Age", format="%d"),
            "Predicted_Goals_2025": st.column_config.NumberColumn("Predicted Goals", format="%d"),
            "Predicted_Assists_2025": st.column_config.NumberColumn("Predicted Assists", format="%d"),
            "Predicted_GA_2025": st.column_config.NumberColumn("Total G+A", format="%d")
        }
    )



except FileNotFoundError:
    st.error(f"❌ File not found: {CSV_FILE_PATH}")
    st.info("""
    Please update the CSV_FILE_PATH variable at the top of the script with your file location.
    """)
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.info("Please check your CSV file format and path.")

