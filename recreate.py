import straxen
import scanner

data_path= '/dali/lgrandi/liuhy/get_new_pax/converted'
data_path2= '/dali/lgrandi/liuhy/get_new_pax/processed'

st = scanner.get_context(data_path, data_path2)

runs = st.select_runs()

# Select only when raw data available but high level is not
runs = runs[(runs['raw_records_available'] == True) & (runs['event_info_available'] == False)]

strax_options = [{'run_id': run_id, 'config' : {},
                  'data_path' : data_path,
                  'data_path2' : data_path2} for run_id in runs['name']]

print(strax_options)

scanner.scan_parameters(strax_options)




