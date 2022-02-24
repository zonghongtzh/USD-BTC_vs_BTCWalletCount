'''
Hypothesis: 
If wallet count is increasing -> there should be more users for BTC -> more demand for BTC hence likely price rise 

Strategy 
Wallet count increasing 4 days in a row 
+
btc price has uncertain direction [up,down] or [down,up] in the past 2 days 
'''

from utils import *
from tools.Functions import * 
from tools.Analysis import * 

btc_df = pd.read_csv(os.path.join(utils.mypath, 'data', 'BTC-USD.csv'), index_col = [0]).rename(columns = {'adjclose' : 'BTC-USD'})
walletCount_df = pd.read_csv(os.path.join(utils.mypath, 'data', 'BTC_Wallet_Count.csv'), index_col = [0])
data_dfs = [btc_df, walletCount_df]
data_df = pd.concat(data_dfs, axis=1, join='outer').sort_index().dropna()

# 5-days mean of wallet count diff
walletCount_growth = data_df[walletCount_df.columns].diff().rolling(5).mean()
positions_df = pd.DataFrame(
    data = (
        (delta(walletCount_growth, 4) == 4).all(axis = 1) &             # 4 days wallet count increase 
        (delta(data_df[btc_df.columns], 2) == 0).all(axis = 1)          # uncertain btc price movements
    ).astype(int).values,
    index = data_df.index,
    columns = ['BTC-USD']
)

# adding next date
last_dt = datetime.datetime.strptime(positions_df.index[-1], '%Y-%m-%d')
next_date = (last_dt + datetime.timedelta(1)).strftime('%Y-%m-%d')
positions_df.loc[next_date] = [np.NaN] * positions_df.shape[1]

# plot
weights_df = positions_df.shift(1).fillna(0)
returns_df = btc_df.pct_change()
pnl_df = pnl(weights_df, returns_df)
pnl_df.plot(figsize = (10, 5))
plt.show()
