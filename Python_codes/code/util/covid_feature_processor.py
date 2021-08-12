import numpy as np
import pandas as pd


def cleanup(df, window=10):
    # start_date: starting date of deaths
    start_date = df.columns[0]
    # diff_df: new covid deaths in each day
    diff_df = df.diff(axis=1)
    diff_df[start_date] = df[start_date]
    # err_pos: error positions
    err_pos = (diff_df < 0)
    mask = (diff_df >= 0).shift(axis=1, fill_value=False)

    def fix(periods, mask):
        err_df = diff_df[err_pos & mask]
        avg_df = (diff_df + err_df.shift(periods, axis=1)) / 2
        avg_df[avg_df < 0] = np.nan
        diff_df.update(avg_df)
        avg_df = avg_df.shift(-periods, axis=1)
        diff_df.update(avg_df)
        err_pos[avg_df.notna()] = False

    for i in range(1,window+1):
        fix(i,mask.shift(periods=(-i-1), axis=1, fill_value=True))
        fix(-i,mask)
        mask &= mask.shift(axis=1, fill_value=True)
        
    diff_df[diff_df < 0] = 0
    return diff_df


def cleanup_covid_confirmed(src, dst):
    # read from source
    covid_confirmed_df = pd.read_csv(src, index_col='countyFIPS').drop(index=0)
    # drop unnecessary columns
    df = covid_confirmed_df.drop(columns=["County Name", "State", "StateFIPS"])

    def update(fips, date, value=None, other_date=None, sort=False):
        if sort:
            value = np.sort(df.loc[fips, date])
        elif other_date is not None:
            value = df.loc[fips, other_date]
        df.loc[fips, date] = value

    def update_extend(fips, start_date, end_date=None, value=None, other_date=None, from_start=True):
        if other_date is not None:
            value = df.loc[fips, other_date]
        addend = value - df.loc[fips, (start_date if from_start else end_date)]
        if end_date is None:
            df.loc[fips, start_date:] += addend
        else:
            df.loc[fips, start_date:end_date] += addend

    def interpolate(fips, date):
        df.loc[fips, date] = np.nan

    def invert(fips, start_date, end_date=None):
        df.loc[fips, start_date:end_date] = df.loc[fips, start_date] + df.loc[fips, start_date:end_date].diff().fillna(0).abs().cumsum()

    # one extra 3 on 2nd MSD
    update(55053, '2020-12-26', value=2359) # 23359

    # 2 instead of 0 in 2nd MSD (values are 20000 higher)
    update(48029, ['2020-12-23','2020-12-24'], value=[105348,105649]) # [125348,125649]
    update(48029, '2020-08-03', value=41238) # 41138

    # 2nd-3rd MSD is 77 instead of 64 (value is 13000 higher)
    update(6037, '2020-12-24', value=664299) # 677299

    # on 2020-08-01, the values of 18087, 18089, 18091 were rotated (18087, 18089, 18091 <- 18091, 18087, 18091)
    update([18087, 18089, 18091], '2020-08-01', value=[539, 6994, 818]) # [818, 539, 6994]
    # on 2020-08-02, the value of 18089 was copied from previous day (which is wrong)
    update(18089, '2020-08-02', value= 6994) # 539

    # 1st-2nd MSD is 63 instead of 59 and then copy that trend to end
    update_extend(6029, '2020-12-25', value=63601) # 59601

    # 1st-2nd MSD is 101 instead of 81 and then copy that trend to end
    update_extend(48355, '2020-07-25', value=10127) # 8127

    # interpolate all the values between `start_date` and `end_date` (interpolate forward)
    interpolate(29189, slice('2020-12-22','2020-12-31'))

    # the values of 37111 and 37113 were interchanged and that trend was followed for 37111
    update(37113, '2020-12-28', value=1272) # 2981
    update_extend(37111, '2020-12-28','2021-01-01', value=2981) # 1272

    # 2nd MSD is 5 instead of 7 (value is 2000 higher)
    update(29189, '2020-11-11', value=35658) # 37658

    interpolate(slice(29001,29510), slice('2020-12-25','2020-12-31'))

    # interpolate
    interpolate(45001, '2020-08-07')
    interpolate(slice(27001,27173), '2020-10-24')
    interpolate(6101, '2020-08-21')
    interpolate(49053, '2020-09-13')
    interpolate(46117, '2020-12-28')
    interpolate(slice(53001,53077), '2020-10-24')
    interpolate(36089, '2020-07-06')
    interpolate(53005, slice('2021-01-30','2021-01-31'))
    interpolate(6059, '2020-09-03')
    interpolate(23031, '2020-09-14')
    interpolate(48039, '2020-10-13')
    interpolate(29097, '2020-07-03')
    interpolate(28135, '2020-08-06')
    interpolate(12055, '2020-06-27')
    interpolate(23005, '2020-09-14')

    # interpolate between
    interpolate(slice(25001,25027), slice('2020-12-21','2020-12-27'))

    # value was higher by 1100
    update_extend(54053, '2021-01-03','2021-01-06', from_start=False, value=1145) # 2245

    # (interpolate forward)
    interpolate(slice(54051,54055), slice('2020-12-22','2021-01-02'))

    # interpolate between
    interpolate(slice(16001,16087), ['2020-12-25','2020-12-26'])

    # 1st-2nd MSD is 101 instead of 81 and then copy that trend to end
    update_extend(48415, '2021-04-01', value=3381) # 2369

    interpolate(56001, ['2020-10-24', '2020-10-25'])
    interpolate(56013, '2020-10-24')
    update_extend(56021, '2020-10-24','2020-10-25', value=1327) # 327
    update(56025, '2020-10-24', value= 1206) # 206

    update(4019, '2020-09-21', value= 24647) # 25647

    interpolate(slice(53001,53077), slice('2020-12-25','2020-12-29'))

    update(slice(54001,54109), '2020-12-25', other_date='2020-12-24')
    update_extend(54049, '2021-01-03', value=2021) # 1021
    interpolate(slice(54001,54109), slice('2020-12-28','2021-01-02'))

    update(12029, '2020-11-22', value=953) # 253

    update_extend(48241, '2021-01-09','2021-01-12', value=1781) # 2481

    update(6071, '2020-07-29', value=31309) # 32309

    update(6013, '2020-07-29', value=7414) # 7714

    update_extend(20055, '2021-03-26', value=5961) # 5350

    update(6035, '2020-08-07', value=65) # 638

    update(15001, '2021-01-14', value=2053) # 2653

    update(48099, '2020-11-14', value=2172) # 2712

    update(slice(37001,37199), slice('2020-10-17','2020-10-25'), sort=True)

    # the values of 37115 and 37117 were interchanged and that trend was followed for 37117
    update(37115, '2020-12-28', value=785) # 1339
    update_extend(37117, '2020-12-28','2021-01-01', value=1339) # 785

    update_extend(48277, '2020-11-09','2020-12-20', value=2073) # 1573

    update(48471, '2020-09-12', value=3470) # 3370
    update(48471, '2020-09-16', value=3556) # 3686
    update_extend(48471, '2020-09-03','2020-09-04', value=3717) # 3417
    update_extend(48471, '2020-08-29','2020-09-04', value=3527) # 3627
    update_extend(48471, '2020-09-05','2020-09-08', value=3628) # 3828
    update_extend(48471, '2020-09-09', value=3703) # 3403

    update(48215, ['2020-12-21','2020-12-22'], value=[48094, 48176]) # [47594, 47976]

    update_extend(48457, '2021-01-09','2021-01-12', value=969) # 1369

    update_extend(2261, '2021-04-08', value=400) # 0
    update_extend(20161, '2021-03-26', value=6148) # 5775

    update(6071, '2020-09-19', value=52127) # 52827

    update(6099, ['2020-11-19','2020-11-22'], value=[19510, 19802]) # [19802, 19510]

    update_extend(51590, '2021-04-01', value=4469) # 4169

    update_extend(42101, '2020-09-19','2020-09-20', value=30876) # 31176

    update_extend(20161, '2020-09-18','2020-09-20', value=1562) # 1262

    update_extend(6051, '2020-12-03','2020-12-20', value=560) # 320

    update_extend(6083, '2020-10-12','2020-10-13', value=9445) # 9745

    update_extend(48351, '2021-01-09','2021-01-12', value=441) # 661

    update(48099, slice('2021-02-01','2021-02-07'), value=[4754, 5034, 5384, 5561, 5835, 6151, 6339]) # [6954, 7034, 7084, 7061, 7035, 7051, 6839])
    update_extend(48099, '2020-08-29','2020-08-30', value=966) # 866

    update_extend(48451, '2020-07-14','2020-07-17', value=765) # 1065

    update(19187, '2020-08-19', value=923) # 893
    update_extend(19187, '2020-08-20','2020-08-27', value=935) # 685

    update_extend(48225, '2020-08-25','2020-08-30', value=326) # 526

    update_extend(6035, '2020-12-15','2020-12-18', value=3384) # 3584

    update_extend(48329, '2020-07-21','2020-07-31', value=1399) # 1199

    update_extend(48209, '2020-10-26','2020-11-30', value=6309) # 6109

    update(48371, '2020-12-28', value=1282) # 1102
    update_extend(48371, '2021-01-16', value=1413) # 1313

    update_extend(6041, '2020-07-13','2020-07-14', value=3044) # 3244
    # 6053, 5968, 6068, ...
    update(6041, '2020-08-28', value=6068) # 5968
    update_extend(6041, '2020-07-28','2020-07-29', value=4327) # 3327

    update(6031, '2020-09-07', value=6827) # 7027

    update(34039, slice('2020-07-04','2020-07-21'), sort=True)
    update(34039, '2020-07-22', value=16651) # 16351
    update_extend(34039, '2020-07-23', value=16697) # 16297

    update_extend(48403, '2021-01-09','2021-01-12', value=435) # 599

    update(26121, '2020-08-15', value=1217) # 1377

    update_extend(26103, '2020-10-17','2020-10-18', 756) # 956

    update_extend(24510, '2020-09-16', value=15285) # 15085
    update_extend(24510, '2020-09-15', value=15336) # 15236

    update_extend(6093, '2020-12-19', value=1070) # 870

    update(46085, '2020-12-28', value=512) # 672
    update_extend(46087, '2020-12-28','2021-01-01', value=672) # 512

    update_extend(29145, '2020-09-30', value=1563) # 1363

    update(slice(18029,18033), '2020-08-01', value=[456, 310, 214]) # [214, 456, 310]
    update(slice(18031,18033), '2020-08-02', value=[310, 214]) # [456, 310]

    update_extend(48313, '2020-07-27','2020-08-30', value=309) # 609

    update_extend(29101, '2020-09-30','2020-10-09', value=1174) # 974

    update(6071, '2020-10-21', value=60995) # 60495
    update_extend(6045, '2020-12-19', value=2233) # 2033

    update(24005, '2020-07-16', value=9341) # 9141
    update_extend(48061, '2021-01-31','2021-02-01', value=35141) # 34841

    # 6142
    update(6097, '2020-09-05', value=6142) # 6421

    # 957
    update(48043, '2021-01-23', value=968) # 948
    update(48043, ['2021-01-24','2021-01-25'], value=991) # 841
    update_extend(48043, '2021-01-26', value=1027) # 827

    # 4727,4623,...,4948, 5244
    update_extend(29019, '2020-09-30','2020-10-09', value=4823) # 4623

    # 5192, 5089, 5316
    update(48361, '2020-12-31', value=5289) # 5089
    update_extend(48361, '2021-03-23','2021-03-31', value=8111) # 8211
    update_extend(48361, '2021-04-06', value=8211) # 8111
    update_extend(48361, '2020-09-05', value=1867) # 1767

    interpolate(20055, slice('2020-09-18','2020-09-20'))

    # 165, 265, 165
    update(48175, '2020-11-01', value=165) # 265

    # 511, 635, 536
    update(49037, '2020-07-19', value=535) # 635

    # 402, 403, 502, 408
    update(48049, '2020-08-14', value=403) # 502

    # 457, 549, 457
    update(46003, '2021-03-27', value=457) # 549

    # 4288, 4300, 4295, 4204, ...
    update(51031, ['2021-04-12','2021-04-13'], value=[4295,4300]) # [4300,4295]
    update_extend(51031, '2021-04-14', value=4304) # 4204

    # 271, 181, ...
    update_extend(6049, '2020-12-19', value=281) # 181

    # 451, 545, 456, ...
    update(48089, '2020-09-11', value=454) # 545

    # 754, 896, 808, ...
    update(48367, '2020-07-23', value=796) # 896

    # 1254, 1166, ...
    update_extend(48199, '2020-09-02', value=1266) # 1166
    # 1254, 1206, ...
    update_extend(48199, '2020-08-27', value=1306) # 1206

    # 4495, 4646, ..., 4558
    update_extend(29097, '2020-10-10','2020-10-13', value=4546) # 4646

    # 522, 436, 554, ...
    update(5033, '2020-08-02', value=536) # 436

    # 2688, 2602, ...
    update_extend(6103, '2020-12-19', value=2702) # 2602

    # 1421, 1414, 1417, 1429, ...
    update_extend(21033, '2021-04-10','2021-04-11', value=1424) # 1414
    # 1397, 1311, ...
    update_extend(21033, '2021-04-01', value=1411) # 1311

    # 12874, 12976, 12891
    update(48451, '2021-04-14', value=12876) # 12976

    # 434, 408, ..., 408, 460
    update_extend(32510, '2020-09-03','2020-09-07', value=434) # 408
    # 466, 408, 408, 408, 487 
    update_extend(32510, '2020-09-10','2020-09-12', value=466) # 408
    # 487, 408, 494, ...
    update(32510, '2020-09-14', value=487) # 408
    # 525, 494, ..., 494, 547
    update_extend(32510, '2020-09-23','2020-09-29', value=525) # 494
    # 547, 494, ..., 494, 626
    update_extend(32510, '2020-10-01','2020-10-14', value=547) # 494

    update(12085, slice('2020-08-31','2020-09-13'), sort=True)

    update_extend(22109, '2020-08-25', value=3359) # 3259

    update(13153, '2021-02-03', value=8777) # 8877

    update_extend(48185, '2021-01-17', value=1989) # 1889

    update(28011, '2020-08-06', value=1063) # 1163

    update(26067, '2020-09-04', value=315) # 385

    update_extend(48001, '2021-01-12', value=5521) # 5421
    update_extend(48001, '2020-09-18', value=2844) # 2744

    update(48103, '2021-01-06', value=519) # 591
    update_extend(48103, '2020-12-21','2021-01-09', value=394) # 494

    update_extend(6019, '2020-10-05','2020-10-07', 28965) # 29065

    update(36067, '2020-07-01', value=2863) # 2963

    update(48085, '2020-07-23', value=5648) # 5748

    update_extend(29047, '2020-09-30', value=1861) # 1761

    update_extend(47065, '2020-09-16', value=8959) # 8859

    update(22017, '2020-08-25', value=7217) # 7117

    update_extend(51790, '2021-04-08', value=2537) # 2437
    update_extend(51790, '2021-04-07', value=2599) # 2499

    update_extend(49005, '2020-07-17', value=1720) # 1620

    update_extend(48229, '2021-02-04', value=564) # 464

    update_extend(54047, '2021-01-07', value=1149) # 1049

    # 57, 0, 58
    update(29075, '2020-07-03', value=57) # 0

    # 57, 0, ..., 0
    update_extend(2105, '2021-04-08', value=57) # 0

    update_extend(20103, '2020-08-31','2020-09-01', value=1677) # 1777

    # 8188, 8132, ...
    update_extend(39157, '2021-03-12', value=8232) # 8132

    interpolate(20005, ['2020-08-29','2020-08-30'])
    # interpolate(20005, '2020-08-28','2020-08-31', 3)

    update_extend(4017, '2020-10-15','2020-10-16', value=6020) # 6120

    update_extend(2090, '2020-11-19','2020-11-21', value=2860) # 2960

    update_extend(29147, '2020-09-30', value=651) # 601

    update(41047, '2020-09-06', value=4013) # 3964

    update(53025, '2020-10-09', value=3084) # 3035

    update_extend(13183, '2021-04-01', value=688) # 638

    update_extend(20153, '2021-03-26', value=398) # 298

    update_extend(48383, '2020-12-31', value=371) # 321

    update_extend(34003, '2020-08-20', value=21361) # 21261

    update_extend(47179, '2020-09-03', value=1866) # 1766

    update_extend(51159, '2021-04-01', value=1495) # 1395

    update_extend(47141, '2020-09-03', value=2484) # 2384

    update_extend(26157, '2021-02-02', value=3080) # 3030

    update(36059, '2020-08-03', value=43380) # 43480

    update_extend(27053, '2020-09-10', value=24489) # 24389

    update_extend(48389, '2021-01-09', value=1496) # 1446

    update_extend(20069, '2021-03-26', value=656) # 556

    update_extend(32031, '2021-04-09', value=44600) # 44500

    # 47+5
    update_extend(6003, '2020-12-03','2020-12-20', value=52) # 5

    update_extend(48199, '2021-04-06', value=5654) # 5554

    invert(48253, '2021-03-31')

    update_extend(51580, '2021-04-01', other_date='2021-03-31')

    invert(21143, '2021-03-31')

    update(12125, '2020-08-06', value=274) # 244
    update_extend(12125, '2020-07-29', value=306) # 206

    update_extend(37131, '2020-08-08','2020-08-12', value=299) # 349

    update_extend(47187, '2020-09-03', value=4524) # 4424

    update_extend(26161, '2020-07-19', value=2203) # 2103

    update(slice(41001,41071), '2020-08-30', other_date='2020-08-29')
    update(slice(41001,41071), '2020-09-06', other_date='2020-09-05')

    update(slice(23001,23031), '2020-09-08', other_date='2020-09-07')

    update_extend(20145, '2020-08-31', value=271) # 171

    update(slice(38001,38105), '2020-11-11', other_date='2020-11-10')

    update_extend(48413, '2020-12-21','2021-01-02', value=159) # 139

    update(20045, slice('2021-03-26','2021-03-30'), other_date='2021-03-25')

    update_extend(48249, '2020-10-17', value=1564) # 1524

    update_extend(48161, '2021-04-01', value=1852) # 1812

    update_extend(48139, '2021-04-03', value=22264) # 22164

    update_extend(48361, '2020-08-26','2020-08-28', value=1767) # 1817

    update_extend(30003, '2020-12-15','2020-12-23', value=1932) # 1972

    update_extend(37013, '2021-04-13', value=4449) # 4444
    update_extend(37013, '2021-04-09', value=4474) # 4434

    interpolate(26121, ['2020-09-05','2020-09-06','2020-09-12','2020-09-13'])

    # 1031 + (998 - 997)
    update_extend(48273, '2020-10-17', value=1032) # 998

    update_extend(48371, '2021-01-10','2021-01-15', value=1396) # 1356
    update_extend(48371, '2021-01-16', value=1413) # 1313

    # 964, 932
    update_extend(20067, '2021-03-26', value=972) # 932

    # actual interpolation
    df = df.interpolate(axis=1)
    # final process
    diff_df = cleanup(df)
    # update dataframe with result
    covid_confirmed_df.update(diff_df)
    # write to destination
    covid_confirmed_df.to_csv(dst)


def cleanup_covid_deaths(src, dst):
    # read from source
    covid_deaths_df = pd.read_csv(src, index_col='countyFIPS').drop(index=0)
    # drop unnecessary columns
    df = covid_deaths_df.drop(columns=["County Name", "State", "StateFIPS"])
    # process
    diff_df = cleanup(df)
    # update dataframe with result
    covid_deaths_df.update(diff_df)
    # write to destination
    covid_deaths_df.to_csv(dst)


def aggregate_covid_feature(src, dst, segments):
    src_df = pd.read_csv(src)
    dst_df = src_df.iloc[:,:4]

    for name, start_date, end_date in segments:
        dst_df[name] = src_df.loc[:, start_date:end_date].sum(axis=1)
    
    dst_df.to_csv(dst, index=False)