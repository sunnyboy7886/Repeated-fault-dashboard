import streamlit as st 
import pandas as pd 
import numpy as np
import plotly_express as px 
import plotly.graph_objects as go
import datetime
import warnings
warnings.filterwarnings('ignore')
from streamlit_option_menu import option_menu

# set page configuration of application Title,Favicon,Layout

st.set_page_config(
    page_title='Repeated Fault dashboard',
    page_icon=':bar_chart:', 
    layout='wide',
    initial_sidebar_state='auto'
)

# hide Main menu, Header Footer and adjust height of header

st_hide_style= '''
<style>
    #MainMenu{visibility:hidden}
    header{visibility:hidden}
    footer{visibility:hidden}
    div.block-container{padding: 0.5rem 1rem}
</style>
'''
st.markdown(st_hide_style,unsafe_allow_html=True)

# open and read external custom css

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

#  Reading excel file and caching the file

@st.cache_data
def read_csv_file():
    select_file= 'Repeated fault Dashboard.csv'
    df = pd.read_csv(select_file)

    #  convert duration object type into int type into Hour, Min and sec column

    df['Hour'] = pd.to_datetime(df['Duration'],format=('%H:%M:%S')).dt.hour
    df['Min'] = pd.to_datetime(df['Duration'],format=('%H:%M:%S')).dt.minute
    df['Sec'] = pd.to_datetime(df['Duration'],format=('%H:%M:%S')).dt.second

    #  convert Main code and Status code from object type into int type

    convert_dt = {'Main code' : int, 'Sub code' : int, 'Date': str}
    df = df.astype(convert_dt)
    return df
    

df = read_csv_file()

# Create dataframe of PAN INdia wec

PAN_India_wec = pd.DataFrame({
    'State': ['AP','GJ','KA-N','KA-S','MH','MP','RJ','TN'],
    'Total_wec' : [272,1398,836,377,538,233,1294,707]   
})

PAN_India_area_wec = pd.DataFrame(
    {
        'Area' : ['PENUKONDA','SINGANAMALA','TADPATRI','BHATIA','KUTCH','LALPUR','MAHIDAD','SAMANA','BELGAUM','GADAG','TADAS','C DURGA','HIRIYUR','JOGIHALLI','ANDRALK','CHVNSWR','KARAD','KHANAPUR','KHANDKE',"P'PATTA",'PATAN','DEWAS','MAHURIYA',"MANDSAUR",'BHAKHRANI','BHUKITA','RAJGARH','SIPLA','TEMDARI','TINWARI','DHARAPURAM','MANUR','MUPANDL','POOLAVADI','PUSHPATHUR',"V'KULAM",'SATARA'],
        'Total_wec' : [151,16,105,235,83,398,144,578,187,388,258,180,127,70,132,73,119,56,62,64,34,118,70,45,275,337,91,287,168,123,126,157,73,91,99,154,34]
    }
)

# Creating NAvbar Dashbaord and Excel File

selected = option_menu(
        menu_title="",
        options=['Dashboard','Excel_file'],
        icons=['house','gear'],
        default_index=0,
        orientation="horizontal")

#  Creating Multi selection Filters for State, Area , MOnth and Maincode

if selected == "Dashboard":
    # to select date start and end date
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Date'] = df['Date'].map(datetime.datetime.date)
    
    
    start_date = pd.to_datetime(df['Date']).min()
    end_date = pd.to_datetime(df['Date']).max()
    
    startingdate,endingdate = st.columns(2)
    with startingdate:
      startdate =  st.date_input('Enter start date', start_date)
        
    with endingdate:
       enddate= st.date_input('Enter end date', end_date)
    
    df1 = df[(df['Date'] >= startdate) & (df['Date'] <= enddate)]
    
    #  Creating Multi selection Filters for State, Area , MOnth and Maincode
    
    state,area,month,maincode=st.columns(4)
    with state:
        state= st.multiselect('Select State', options= df1['State'].unique())
    if not state:
        df2 = df1.copy()
    else:   
        df2 = df1[df1['State'].isin(state)]
        
    with area:
        area = st.multiselect('Select Area', options= df2['Area'].unique())     
    with month:
        month = st.multiselect('Select Month', options= df2['Month'].unique())  
    with maincode:
        maincode = st.multiselect('Select Main code', options= df2['Main code'].unique())

    #  Creating different combination for filtered dataframe by selecting State, Area , Month and Maincode
    
    if not state and not area and not month and not maincode:
        filtered_df = df1.copy()
    elif not area and not month and not maincode:
        filtered_df = df1[df1['State'].isin(state)]
    elif not state and not month and not maincode:
        filtered_df = df2[df2['Area'].isin(area)]
    elif not state and not area and not maincode:
        filtered_df = df2[df2['Month'].isin(month)]
    elif not state and not area and not month:
        filtered_df = df2[df2['Main code'].isin(maincode)]
    elif not month and not maincode:
        filtered_df = df2[df2['State'].isin(state) & df2['Area'].isin(area)]
    elif not state and not maincode:
        filtered_df = df2[df2['Area'].isin(area) & df2['Month'].isin(month)]
    elif not state and not area:
        filtered_df = df2[df2['Month'].isin(month) & df2['Main code'].isin(maincode)]
    elif not area and not maincode:
        filtered_df = df2[df2['State'].isin(state) & df2['Month'].isin(month)]
    elif not area and not month:
        filtered_df = df2[df2['State'].isin(state) & df2['Main code'].isin(maincode)]
    elif not state and not month:
        filtered_df = df2[df2['Area'].isin(area) & df2['Main code'].isin(maincode)]
    elif not state:
        filtered_df = df2[df2['Area'].isin(area) & df2['Month'].isin(month) & df2['Main code'].isin(maincode)]
    elif not area:
        filtered_df = df2[df2['State'].isin(state) & df2['Month'].isin(month) & df2['Main code'].isin(maincode)]
    elif not month:
        filtered_df = df2[df2['State'].isin(state) & df2['Area'].isin(area) & df2['Main code'].isin(maincode)]
    elif not maincode:
        filtered_df = df2[df2['State'].isin(state) & df2['Area'].isin(area) & df2['Month'].isin(month)]
    elif state and area and month and maincode:
        filtered_df = df2[df2['State'].isin(state) & df2['Area'].isin(area) & df2['Month'].isin(month) & df2['Main code'].isin(maincode)]
        
    #  Obtain KPI values from filtered df Sum of freq, Count of freq and Freq per count
    
    sum_of_freq = filtered_df['Frequency'].sum()
    count_of_freq = filtered_df['Frequency'].count()
    freq_per_count = round(sum_of_freq/count_of_freq,2)
    
    #  Obtain Freq per operational Wec KPI value

    if state:
        selected_wec = PAN_India_wec[PAN_India_wec['State'].isin(state)]
    elif area:
        selected_wec = PAN_India_area_wec[PAN_India_area_wec['Area'].isin(area)]
    else:
        selected_wec = PAN_India_wec.copy()
    
    
        
    Total_wec = selected_wec['Total_wec'].sum()
    
    freq_per_operational_wec = round(sum_of_freq/Total_wec,2)
    
    #  Calculate total down hours from filtered df

    hour = filtered_df["Hour"].sum()
    min = filtered_df['Min'].sum()
    sec = filtered_df['Sec'].sum()
    
    total_duration = round((hour + (min/60) + (sec/360)),2)

    # Cards to display Various KPI sum of freq, Fault count, Freq per wec, Total down duration, Freq per operational wec
    
    col1,col2,col3,col4,col5 = st.columns([1,1,1,2,1])
    with col1:
        st.metric("Sum of Freq", sum_of_freq)
    with col2:
        st.metric("WEC Fault count ", count_of_freq)
    with col3:
        st.metric("Freq per fault count ", freq_per_count)
    with col4:
        st.metric("Total down Duration", f'{total_duration} Hrs')
    with col5:
        st.metric('Freq per Operational wec',freq_per_operational_wec)

    # Grouping statewise fault freq
    
    state_wise_freq = filtered_df.groupby(by='State').agg(
        {
            'Frequency' : 'sum',
            'WEC': 'count'
        }
    ).sort_values('State',ascending=True).reset_index()

    

    # Grouping areawise fault freq and percentage of fault freq
    
    area_wise_freq = filtered_df.groupby(by='Area',as_index=False)['Frequency'].sum().sort_values('Frequency',ascending=True).tail(5)

    area_wise_freq["Percentage of Fault freq"] = round((area_wise_freq['Frequency']/area_wise_freq['Frequency'].sum())*100,2)

    # Grouping Month wise fault freq and wec count
    
    monthwise_fault = filtered_df.groupby(by=['Month'], as_index=False).agg({
        'Frequency':'sum',
        'WEC': 'count'
    })

    month_mapping = { 'Jun': 1,'Jul': 2, 'Aug': 3, 'Sept': 4, 'Oct' :5 , 'Nov': 6, 'Dec': 7}

    monthwise_fault['month_num'] = monthwise_fault['Month'].map(month_mapping)

    monthwise_fault = monthwise_fault.sort_values('month_num')

    #  Grouping Wec wise Fault freq

    wec_wise_freq = filtered_df.groupby(by='WEC', as_index=False)['Frequency'].sum().sort_values('Frequency', ascending=True).tail(5)
    
    #  Grouping Status code wise fault freq

    statuscode_wise_freq = filtered_df.groupby(by=['State','Area','WEC','StatusCode'], as_index=False)['Frequency'].sum().sort_values('Frequency',ascending=True)

    statuscode_wise_freq = statuscode_wise_freq[statuscode_wise_freq['Frequency']>50]

    status_wise_freq = statuscode_wise_freq.tail(5)

    # Grouping High duration wec 

    filtered_df['Total_hours'] = round((filtered_df['Hour'] + filtered_df['Min']/60 + filtered_df['Sec']/360),2)

    duration_wise_wec = filtered_df.groupby(by=['State','Area','WEC', 'StatusCode'],as_index=False).agg({
        'Total_hours' : 'sum',
        'Frequency':'sum'
    }).sort_values('Total_hours',ascending=True)

    duration_wise_wec = duration_wise_wec[duration_wise_wec['Total_hours']>50.00].sort_values('Total_hours')

    top_5_high_duration_wec = duration_wise_wec.tail(5)
    
    # Repeated fault continue 3 month

    repeated_fault_df = df.pivot_table(index=['State','Area','WEC','StatusCode'],columns='Month', values='Frequency', aggfunc='sum', margins=True, margins_name='Sum of Frequency').sort_values('Sum of Frequency', ascending=False).iloc[1:]

    repeated_fault_df = repeated_fault_df.fillna(0)
    
    repeated_fault_df = repeated_fault_df[repeated_fault_df['Sum of Frequency']>50]

    #  Creating combination for conitinuos repeated error
    
    repeated_fault_df['Fault repeated continue > 3 months'] = np.where((
        ((repeated_fault_df['Jun']>0) & (repeated_fault_df['Jul']>0) & (repeated_fault_df['Aug']>0)) | 
        ((repeated_fault_df['Jul']>0) & (repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0))| 
        ((repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0)) |
        ((repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0) & (repeated_fault_df['Nov']>0)) | 
        ((repeated_fault_df['Oct']>0) & (repeated_fault_df['Nov']>0) & (repeated_fault_df['Dec']>0)) |
        ((repeated_fault_df['Jun']>0) & (repeated_fault_df['Jul']>0) & (repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0)) |  
        ((repeated_fault_df['Jul']>0) & (repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0)) | 
        ((repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0) & (repeated_fault_df['Nov']>0)) |
        ((repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0) & (repeated_fault_df['Nov']>0) & (repeated_fault_df['Dec']>0)) |
        ((repeated_fault_df['Jun']>0) & (repeated_fault_df['Jul']>0) & (repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0)) |
        ((repeated_fault_df['Jul']>0) & (repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0) & (repeated_fault_df['Nov']>0)) |
        ((repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0) & (repeated_fault_df['Nov']>0) & (repeated_fault_df['Dec']>0)) |
        ((repeated_fault_df['Jun']>0) & (repeated_fault_df['Jul']>0) & (repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0) & (repeated_fault_df['Nov']>0)) |
        ((repeated_fault_df['Jul']>0) & (repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0) & (repeated_fault_df['Nov']>0) & (repeated_fault_df['Dec']>0))|
        ((repeated_fault_df['Jun']>0) & (repeated_fault_df['Jul']>0) & (repeated_fault_df['Aug']>0) & (repeated_fault_df['Sept']>0) & (repeated_fault_df['Oct']>0) & (repeated_fault_df['Nov']>0) & (repeated_fault_df['Dec']>0))),'repeated','not repeated')
    
    repeated_fault_df = repeated_fault_df[repeated_fault_df['Fault repeated continue > 3 months']=='repeated']

    Top_10_wec_repeated_fault = repeated_fault_df.head(10)
    
    #  Creating Bar Charts for state wise freq
    
    left_col1,right_col1 = st.columns(2)
    
    with left_col1:
        #  Creating Bar Charts for state wise freq

        st.subheader('Statewise Fault Frequency')
        # fig1 = px.bar(data_frame=state_wise_freq, x= 'State', y='Frequency', text= ['{:,}'.format(x) for x in state_wise_freq['Frequency']],height=350)
        # st.plotly_chart(fig1,use_container_width=True)

        fig1= go.Figure()
        fig1.add_trace(go.Bar(x=state_wise_freq['State'], y=state_wise_freq['Frequency'], name='Sum ofFrequency', text=['{:,}'.format(x) for x in state_wise_freq['Frequency']], textposition='outside'))
        fig1.add_trace(go.Scatter(x =state_wise_freq['State'], y=state_wise_freq['WEC'], mode='lines',name='Count of WEC', yaxis='y2'))
        
        fig1.update_layout(
            xaxis = dict(title='State'),
            yaxis = dict(title='Sum of Frequency', showgrid=False),
            yaxis2= dict(title= 'Count of wec', overlaying= 'y', side='right'),
            template= 'gridon',
            legend = dict(x=1,y=1))
        st.plotly_chart(fig1, use_container_width=True)
        
        #  download data for state wise freq
        if state:
            with st.expander('Download Statewise_fault_freq'):
                st.dataframe(filtered_df,height=200)
                csv = filtered_df.to_csv(index=False, encoding='utf-8')
                st.download_button(label='Download Data',data=csv,file_name='Statewise_fault_freq.csv',mime='text/csv',help="click here to download Statewise_fault_freq file")
        
        #  Creating pie chart for Area wise high fault frq
    with right_col1:
        st.subheader('Top 5 High Fault freq Area')
        fig2 = px.pie(data_frame=area_wise_freq,names='Area',values='Percentage of Fault freq',hole=0.5,height=450, hover_data='Frequency')
        fig2.update_traces( text=area_wise_freq['Area'],textposition = 'outside')
        st.plotly_chart(fig2,use_container_width=True)
        
        #  Download areawise_fault_freq data file
        if area:
            with st.expander('Download areawise_fault_freq'):
                st.dataframe(filtered_df,height=200)
                csv = filtered_df.to_csv(index=False, encoding='utf-8')
                st.download_button(label='Download Data',data=csv,file_name='Areawise_fault_freq.csv',mime='text/csv',help="click here to download Areawise_fault_freq file")
    
    #  create a bar chart for Monthwise freq fault
    left_col2,right_col2 = st.columns(2)
    with left_col2:
        st.subheader('Month wise Fault freq')
        fig3 = px.bar(data_frame=monthwise_fault, x= 'Month', y = ['Frequency','WEC'],barmode='group',height= 450, text_auto=True)
        st.plotly_chart(fig3, use_container_width=True)
    
    # create pie chart for Top 5 high fault freq
    with right_col2:
        st.subheader('Top 5 High Fault Freq Wec')
        fig4 = px.pie(data_frame=wec_wise_freq, names= 'WEC', values= 'Frequency', hole=0.5, height=450, template="plotly_dark" )
        fig4.update_traces(text=wec_wise_freq['WEC'], textposition= 'outside')
        st.plotly_chart(fig4, use_container_width=True)
        
    left_col3,right_col3 = st.columns(2)
    # create bar chart for Top 5 High Fault Frequ Status code
    with left_col3:
        st.subheader('Top 5 High Fault Frequ Status code')
        fig5 = px.bar(status_wise_freq, x= 'Frequency', y= 'StatusCode', text=['{:,}'.format(x) for x in status_wise_freq['Frequency']], height=450)
        st.plotly_chart(fig5, use_container_width=True)
        with st.expander('Download Statuscode_wise_fault_freq'):
                st.dataframe(statuscode_wise_freq,height=200)
                csv = statuscode_wise_freq.to_csv(index=False, encoding='utf-8')
                st.download_button(label='Download Data',data=csv,file_name='Stauscode_fault_freq.csv',mime='text/csv',help="click here to download Statuscode_fault_freq file")
                
    # create pie chart for High down time wec
    with right_col3:
        st.subheader('Top 5 High downtime Wec')
        fig6 = px.pie(data_frame=top_5_high_duration_wec,values='Total_hours', names='WEC', hole=0.5, height=450, template="plotly_white" , hover_data=['StatusCode'])
        fig6.update_traces(text= top_5_high_duration_wec['WEC'],textposition= 'outside')
        st.plotly_chart(fig6, use_container_width=True)
        with st.expander('Download Duration_wise_fault_freq'):
                st.dataframe(duration_wise_wec,height=200)
                csv = duration_wise_wec.to_csv(index=False, encoding='utf-8')
                st.download_button(label='Download Data',data=csv,file_name='Duration_fault_freq.csv',mime='text/csv',help="click here to download Duration_wise_fault_freq file")
                
    # repeated fault continue for > 3 months
    st.subheader('Top 10 wec repeated fault continue for > 3 months')
    st.dataframe(Top_10_wec_repeated_fault)
    csv = repeated_fault_df.to_csv(index=True, encoding='utf-8')
    st.download_button(label='Download Data',data=csv,file_name='Repeated fault continue more than 3 months.csv',mime='text/csv',help="click here to download Repeated fault continue more than 3 months")

else:
    st.dataframe(df,height=350)
    csv = df.to_csv(index=False, encoding='utf-8')
    st.download_button('Download file',data=csv,file_name='Repeated fault.csv', mime='text/csv',help='click here to download the data')