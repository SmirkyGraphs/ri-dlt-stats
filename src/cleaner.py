from pathlib import Path
import pandas as pd

def make_date(df, m_format):
    # create date column & remove year+month
    df['month'] = pd.to_datetime(df['month'], format=m_format).dt.month
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

    # remove month + year
    df = df.drop(columns=['month', 'year'])

    # sort by date
    df = df.sort_values(by='date')

    return df

def get_industry_ces(df):
    shift_cols = df.iloc[:, 0:8]
    shift_cols = shift_cols.apply(lambda x: pd.Series(x.dropna().values), axis=1).fillna('')
    df = df.iloc[:, 8:]
    df.insert(0, 'industry', shift_cols)

    return df

def combine_ces(report_types, rename_cols):
    report_types = ['seasonal_adjusted', 'non_adjusted']

    merge_frames = []
    for report in report_types:
        if report == "non_adjusted":
            skip_r = 5
        else:
            skip_r = 4
            
        files = Path(f'./data/raw/current_employment/{report}/').rglob('*')

        frames = []
        for f in files:
            df = pd.read_excel(f, skiprows=skip_r)
                    
            # fix column naming errors and lowercase    
            df.columns = [x.strip().replace('.', '').lower() for x in df.columns]
            df = df.rename(columns=rename_cols)
            
            # skip average
            if report == 'non_adjusted':
                df = df.iloc[:, 0:-1]

            # add year and report_type
            df['year'] = f.name[:4]
            df['report_type'] = report

            # add to list of frames
            frames.append(df)        
        
        # merge frames of report type
        df = pd.concat(frames, sort=False)

        if report == "non_adjusted":
            # fix naming issue and remove nulls
            df = get_industry_ces(df)
            df = df[df['jun'].notnull()]
            df = df[~df['industry'].str.contains('Dispute')]
        else:
            # fix column name and remove nulls
            df = df.rename(columns={'unnamed: 0':'industry'})
            df = df.dropna(subset=['industry'])

        # add to list of report_type frames
        merge_frames.append(df)
    
    # merge the 2 datasets together
    df = pd.concat(merge_frames).reset_index(drop=True)

    return df

def clean_ces(rename_dict):
    # get dictionary values
    rename_cols = rename_dict['rename_ces_cols']
    rename_act = rename_dict['rename_act']
    rename_adj = rename_dict['rename_adj']
    level_act = rename_dict['level_act']
    level_adj = rename_dict['level_adj']

    report_types = ['seasonal_adjusted', 'non_adjusted']
    df = combine_ces(report_types, rename_cols)

    # fix casing to normalize
    df['industry'] = df['industry'].str.strip()
    df['industry'] = df['industry'].str.lower()

    # melt columns to make data vertical 
    var_cols = ['industry', 'year', 'report_type']
    df = df.melt(id_vars=var_cols, var_name='month')

    # fix date column
    df = make_date(df, '%b')

    # convert numbers (in thousands)
    df['value'] = df['value'] * 1000

    # calculations MoM & YoY
    df['MoM_%'] = df.groupby(['industry', 'report_type'])['value'].pct_change()
    df['MoM_#'] = df.groupby(['industry', 'report_type'])['value'].diff()

    df['YoY_%'] = df.groupby(['industry', 'report_type'])['value'].pct_change(12)
    df['YoY_#'] = df.groupby(['industry', 'report_type'])['value'].diff(12)

    # rename values using dictionary
    df.loc[df['report_type'] == 'non_adjusted', 'industry'] = df['industry'].map(rename_act).fillna(df['industry'])
    df.loc[df['report_type'] == 'seasonal_adjusted', 'industry'] = df['industry'].map(rename_adj).fillna(df['industry'])

    # get level from dictionary
    df.loc[df['report_type'] == 'non_adjusted', 'level'] = df['industry'].map(level_act)
    df.loc[df['report_type'] == 'seasonal_adjusted', 'level'] = df['industry'].map(level_adj)

    # title case industry
    df['industry'] = df['industry'].str.title()

    # re order columns
    order = rename_dict['order_ces']
    df = df[order]

    # sort & export cleaned csv file
    df.to_csv('./data/clean/current_employment_cleaned.csv', index=False)

def combine_statewide():
    files = Path(f'./data/raw/geographic/state/').rglob('*')

    frames = []
    for f in files:
        df = pd.read_excel(f, skiprows=5)
        print(f.name)

        # add report_type
        df['report_type'] = f.name[:-5]

        # add to list of frames
        frames.append(df)        
    
    # merge frames of report type and remove nulls
    df = pd.concat(frames, sort=False)
    df = df.dropna(how='all', axis=1)

    return df

def clean_statewide(rename_dict):
    order_cols = rename_dict['order_state']

    # generate dataframe
    df = combine_statewide()

    # lowercase columns and remove avg
    df.columns = [x.lower() for x in df.columns]
    df = df[df['month']!='Annual Average']

    # fix date column
    df = make_date(df, '%B')

    # set column order
    df.columns = order_cols

    df.to_csv('./data/clean/statewide_employment_cleaned.csv', index=False)

