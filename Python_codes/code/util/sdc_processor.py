import numpy as np
import pandas as pd


def process_sdc(sdc_src, pop_src, dst):
    county_col = 'countyFIPS'
    state_col = 'StateFIPS'
    pop_col = 'population'

    demographic_cols = ['POP13_SQMI', 'WHITE', 'BLACK', 'AMERI_ES', 'ASIAN',
        'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'MALES', 'FEMALES',
        'AGE_UNDER5', 'AGE_5_9', 'AGE_10_14', 'AGE_15_19', 'AGE_20_24',
        'AGE_25_34', 'AGE_35_44', 'AGE_45_54', 'AGE_55_64', 'AGE_65_74',
        'AGE_75_84', 'AGE_85_UP','HOUSEHOLDS', 'AVE_HH_SZ', 
        'HSEHLD_1_M', 'HSEHLD_1_F', 'MARHH_CHD', 'MARHH_NO_C', 
        'MHH_CHILD', 'FHH_CHILD', 'FAMILIES', 'AVE_FAM_SZ',
        'HSE_UNITS', 'VACANT', 'OWNER_OCC', 'RENTER_OCC']
    comorbidities_cols = ['Prevalence of obesity','Hypertension', 'Diabetes','CVD','HIV/AIDS']

    cols_to_normalize = ['WHITE', 'BLACK', 'AMERI_ES', 'ASIAN',
        'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'MALES', 'FEMALES',
        'AGE_UNDER5', 'AGE_5_9', 'AGE_10_14', 'AGE_15_19', 'AGE_20_24',
        'AGE_25_34', 'AGE_35_44', 'AGE_45_54', 'AGE_55_64', 'AGE_65_74',
        'AGE_75_84', 'AGE_85_UP','HOUSEHOLDS', 'HSEHLD_1_M', 'HSEHLD_1_F', 'MARHH_CHD',
        'MARHH_NO_C', 'MHH_CHILD', 'FHH_CHILD', 'FAMILIES',
        'HSE_UNITS', 'VACANT', 'OWNER_OCC', 'RENTER_OCC'] + comorbidities_cols

    sdc_cols = [state_col, pop_col] + demographic_cols + comorbidities_cols

    sdc_df = pd.read_excel(sdc_src)\
                .rename(columns={'FIPS': county_col, 'STATE_FIPS': state_col})\
                .set_index(county_col)

    pop_df = pd.read_csv(pop_src, index_col=county_col).drop(columns=['County Name', 'State'])

    joined_df = sdc_df.join(pop_df, how='inner')
    population = joined_df[pop_col]
    sdc_df = joined_df.loc[:, sdc_cols]

    df = sdc_df.loc[:, cols_to_normalize]
    df[df < 0] = np.nan
    df = df.div(population, axis=0)
    df = df.fillna(df.median())

    sdc_df.update(df)
    sdc_df.to_csv(dst)