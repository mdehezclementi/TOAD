import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from termcolor import colored
from matplotlib.ticker import FixedLocator, FormatStrFormatter


#%%%% INIT
#columns = ["function_name", "gas_cost", "user_id", "block_number"]
columns = ["function_name", "block_number", "block_timestamp", "gas_cost", "number_of_tx_per_block","gas_used","user_id","last_block_number","input_size","tx_size"]

file_path_0 = "client/gas_cost/gas_cost_10_since_b0.csv"
df = pd.read_csv(file_path_0, names=columns, sep=",",header = None)
df.sort_values(by="block_number", inplace=True)

# list of function
fun_list = df.function_name.unique()

N_fun = len(df.function_name.unique())

# group_size computation
group_size = len(df.user_id.unique())
group = list(df.user_id.unique())

print(fun_list)


bandwidth_occupation_df = df[['block_timestamp','block_number','input_size']].drop_duplicates(subset=['block_number'])
bandwidth_occupation_df['time'] = bandwidth_occupation_df['block_timestamp']-bandwidth_occupation_df['block_timestamp'][0]
print(bandwidth_occupation_df)
# _,ax = plt.subplots()
# bandwidth_occupation_df.plot('time','input_size', label="bandwidth occupation",ax=ax, kind='line',  color="black")
# plt.show()


#%%%% BLOCK NO. PER TIME   <----- THIS ONE IS BETTER


time_evolution_df = df[['block_timestamp','block_number']].drop_duplicates(subset=['block_number'])
time_evolution_df.sort_values(by="block_number", inplace=True)
time_evolution_df['time'] = time_evolution_df['block_timestamp']-time_evolution_df['block_timestamp'][0]
print(time_evolution_df)

checkpoint_part1 = df[['function_name','block_timestamp','block_number']][0:df[df['function_name']=="send_file"]['block_number'].min()+1].drop_duplicates(subset=['function_name'])
checkpoint_part2 = df[['function_name','block_timestamp','block_number']][df[df['function_name']=="send_file"]['block_number'].min()+1:].drop_duplicates(subset=['function_name'])
checkpoint_df = pd.concat([checkpoint_part1,checkpoint_part2]).reset_index()
print(checkpoint_df)
checkpoint_df.sort_values(by="block_number", inplace=True)
checkpoint_df['time'] = checkpoint_df['block_timestamp']-checkpoint_df['block_timestamp'][0]
print(checkpoint_df)


cumulative_input_df = df[['function_name','block_timestamp','input_size','block_number']].drop_duplicates(subset=['block_number'])
cumulative_input_df.sort_values(by="block_number", inplace=True)
cumulative_input_df['time'] = time_evolution_df['block_timestamp']-time_evolution_df['block_timestamp'][0]
cumulative_input_df['cumul_input_size'] = cumulative_input_df['input_size'].cumsum()
print(cumulative_input_df)

checkpoint_input_part1 = cumulative_input_df[['function_name','time','cumul_input_size','block_number']][0:cumulative_input_df[cumulative_input_df['function_name']=="send_file"]['block_number'].min()+1].drop_duplicates(subset=['function_name'])
checkpoint_input_part2 = cumulative_input_df[['function_name','time','cumul_input_size','block_number']][cumulative_input_df[cumulative_input_df['function_name']=="send_file"]['block_number'].min()+1:].drop_duplicates(subset=['function_name'])
checkpoint_input_df = pd.concat([checkpoint_input_part1,checkpoint_input_part2]).reset_index()
checkpoint_input_df.sort_values(by="block_number", inplace=True)
#checkpoint_input_df['time'] = checkpoint_input_df['block_timestamp']-checkpoint_input_df['block_timestamp'][0]
#checkpoint_input_df = pd.merge(left=checkpoint_input_df, right=cumulative_input_df['cumul_input_size'])

print(checkpoint_input_df)


#quit()

_,ax = plt.subplots()

# colors = ["orange","orange","orange","red","green","blue","yellow","purple","green","blue","yellow","purple"]
# labels = ['deploy_migrations','deploy_TOAD','saving_migrations','group_creation','send_file','send_share']

colors = {'deploy_migrations':"orange",
          'deploy_TOAD':"orange",
          'saving_migrations':"orange",
          'group_creation':"red",
          'publish_tpk':"green",
          'encrypt_shares':"blue",
          'publish_group_key':"yellow",
          'send_file': "purple" ,
          'send_share':"purple"
          }

labels = {'deploy_migrations':"(1) deploy migrations",
          'deploy_TOAD':"(2) deploy TOAD",
          'saving_migrations':"(3) save migrations",
          'group_creation':"(4) group creation",
          'publish_tpk':"(5) publish tpk",
          'encrypt_shares':"(6) encrypt shares",
          'publish_group_key':"(7) publish group key",
          'send_file': "(8) encryption" ,
          'send_share':"(9) decryption"
          }

## BLOCK PRODUCTION
time_evolution_df.plot('time','block_number', label="block production",ax=ax, kind='line',  color="black")
ax.set_xlabel("Time (in seconds)",fontsize=24)
ax.set_ylabel("No. Block",fontsize=24)



for i in range(checkpoint_df["function_name"].size):
    if i<8 or i==11:
        ax.scatter(checkpoint_df['time'][i],checkpoint_df['block_number'][i], label=labels[checkpoint_df['function_name'][i]],c=colors[checkpoint_df['function_name'][i]],alpha=0.75)
        if i==11:
            ax.text(checkpoint_df['time'][i]-1.5, checkpoint_df['block_number'][i]+1, str(9),fontsize=22)
        else:
            ax.text(checkpoint_df['time'][i]-1.5, checkpoint_df['block_number'][i]+1, str(i+1),fontsize=22)
    else:
        ax.scatter(checkpoint_df['time'][i],checkpoint_df['block_number'][i], c=colors[checkpoint_df['function_name'][i]],alpha=0.75)
        ax.text(checkpoint_df['time'][i]-1.5, checkpoint_df['block_number'][i]+1, str(i+1-4),fontsize=22)

plt.title("Block production rate over time")
plt.legend(framealpha=1,loc='lower right')
plt.show()


# OR STORAGE/BANDWIDTH OCCUPATION
_,ax = plt.subplots()
bandwidth_occupation_df.plot('time','input_size', label="bandwidth occupation",ax=ax,alpha=0.75)
plt.fill_between(bandwidth_occupation_df['time'], bandwidth_occupation_df['input_size'],alpha=0.75)


cumulative_input_df.plot('time','cumul_input_size', label="cumulative amount of data (in bytes)",ax=ax, kind='line',  color="black")
ax.set_xlabel("Time (in seconds)",fontsize=24)
ax.set_ylabel("Input size (in bytes)",fontsize=24)

for i in range(checkpoint_input_df["function_name"].size):
    if i<8 or i==11:
        ax.scatter(checkpoint_input_df['time'][i],checkpoint_input_df['cumul_input_size'][i], label=labels[checkpoint_df['function_name'][i]],c=colors[checkpoint_df['function_name'][i]],alpha=0.75)
        if i==11:
            ax.text(checkpoint_input_df['time'][i]-1.5, checkpoint_input_df['cumul_input_size'][i]+1, str(9),fontsize=22)
        else:
            ax.text(checkpoint_input_df['time'][i]-1.5, checkpoint_input_df['cumul_input_size'][i]+1, str(i+1),fontsize=22)
    else:
        ax.scatter(checkpoint_input_df['time'][i],checkpoint_input_df['cumul_input_size'][i], c=colors[checkpoint_df['function_name'][i]],alpha=0.75)
        ax.text(checkpoint_input_df['time'][i]-1.5, checkpoint_input_df['cumul_input_size'][i]+1, str(i+1-4),fontsize=22)


plt.title("Amount of data transiting in the contract and bandwidth occupation over time",fontsize=20)
plt.legend(framealpha=1,loc='center right')

plt.show()


quit()

#quit()
#%%%%% COMPARING INPUT SIZE VS GAS COST ONTO TWO DIFFERENT CHARTS
columns = ["function_name", "block_number", "block_timestamp", "gas_cost", "number_of_tx_per_block","gas_used","user_id","last_block_number","input_size","tx_size"]

file_path = "client/gas_cost/gas_cost_10.csv"
df = pd.read_csv(file_path, names=columns, sep=",",header = None)
df.sort_values(by="block_number", inplace=True)

print(df)
# list of function
fun_list = df.function_name.unique()

N_fun = len(df.function_name.unique())

# group_size computation
group_size = len(df.user_id.unique())
group = list(df.user_id.unique())

print(fun_list)

_, ax = plt.subplots(2,1)

gas_cost_per_function = df[['function_name','gas_cost']].drop_duplicates(subset=['function_name'])
gas_cost_per_function.plot(kind="bar",ax=ax[0], width=0.35, alpha=0.75,edgecolor="black")
ax[0].set_xticklabels(labels=["group creation", "publish tpk","encrypt shares","publish group key","encryption", "decryption"],fontsize=14,rotation=0)
ax[0].set_ylabel("Gas consumption (in gas)",fontsize=24)
ax[0].set_title("Comparing input size/gas consumption per contract function",fontsize=20)

input_size_per_function = df[['function_name','input_size']].drop_duplicates(subset=['function_name'])
input_size_per_function.plot(kind="bar",ax=ax[1], width=0.35, alpha=0.75,edgecolor="black")
ax[1].set_xticklabels(labels=["group creation", "publish tpk","encrypt shares","publish group key","encryption", "decryption"],fontsize=14,rotation=0)
ax[1].set_xlabel('Function name',fontsize=24)
ax[1].set_ylabel("Input size (in bytes)",fontsize=24)


plt.show()
#%%%%%  COMPARING INPUT SIZE VS GAS COST ONTO SAME CHART


_,ax = plt.subplots()

combined_df = pd.merge(left=gas_cost_per_function,right=input_size_per_function)
print(combined_df)

ax = combined_df.plot(kind='bar', secondary_y=['input_size'],color=["blue","green"], alpha=0.75, edgecolor="black")
# ax = combined_df.plot(kind='bar', y='gas_cost',color="blue", alpha=0.75, edgecolor="black")
# ax = combined_df.plot(kind='bar', y='input_size',color="green", alpha=0.75, edgecolor="black")


#ax.legend(["Gas consumption","Input size"])
ax.set_ylabel('Gas cost (in gas)',fontsize=24)
ax.right_ax.set_ylabel('Input size (in bytes)',fontsize=24,rotation=-90,labelpad=20)
ax.grid(True)
ax.set_axisbelow(True)
ax.set_xticklabels(labels=["group creation", "publish tpk","encrypt shares","publish group key","encryption", "decryption"],fontsize=14,rotation=0)
ax.set_xlabel("Function name",fontsize=24)

ax.set_title("Comparing input size/gas consumption per contract function",fontsize=20)

plt.show()


#%%% CUMULATIVE GAS CONSO PER CONTRACT FUNCTION

fig, ax = plt.subplots()
#axes = [ax, ax.twinx()]
#axes[-1].spines['right']


### CHOOSE YOUR BACKGROUND
# # Frise
# dimensions_barh = (5e6,0.5e6)
# location_title = [6,4.8e6]
# # Colored Background
dimensions_barh = (0.25e6, 4.5e6)
location_title = [10,0.1e6]
# # Adaptative Colored Background
# dimensions_barh = [(1437078-0.25e6, 0.5e6),(1713452-0.25e6,0.5e6), (2380203-0.25e6,0.5e6),(3431871-0.25e6,0.5e6),
#                    (3487695-0.25e6, 0.5e6),(3764189-0.25e6,0.5e6), (4431559-0.25e6,0.5e6),(4708079-0.25e6,0.5e6),  (4893035-0.25e6,0.5e6)]
# location_title = [10,0.1e6]



mapping = {
    "group_creation":"group initialization",
    "publish_tpk":"group initialization",
    "encrypt_shares":"group initialization",
    "publish_group_key":"group initialization",
    "send_file":"encryption",
    "send_share":"decryption"
}
# # CUMULATIVE DISTRIBUTION OF GAS CONSUMPTION
df['phase'] = df['block_number']
newdf = df[['gas_cost','block_number']].drop_duplicates(subset=['block_number'])
newdf.loc[-1] = [0,0]
newdf.sort_values(by="block_number", inplace=True)
newdf['cumul_gas_cost'] = newdf['gas_cost'].cumsum()
print(newdf)
#newdf.loc[-1] = [0,0,0]  # adding a row
#newdf.index = newdf.index + 1  # shifting index

print(newdf)
newdf.plot('block_number','cumul_gas_cost', label="gas consumption",ax=ax, kind='line',  color="black")
#ax.set_title("Cumulative Distribution of Gas Consumption")
ax.set_ylabel("Gas consumption",fontsize=24)
plt.xlabel("No. Block")

#plt.show()

group_creation_event = df[df['function_name']=='group_creation']['block_number'].min()

ax.broken_barh([(0,group_creation_event),
                ], dimensions_barh, facecolors=('red'), edgecolors=('red'), alpha=0.5, label="group creation")#,edgecolors=('black'),hatch="//")#, label="publish tpk", hatch="--")


publish_tpk_1 = df[df['block_number']<df[df['function_name']=='send_file']['block_number'].min()]
publish_tpk_1_min = publish_tpk_1[publish_tpk_1['function_name']=='publish_tpk']['block_number'].min()
publish_tpk_1_max = publish_tpk_1[publish_tpk_1['function_name']=='publish_tpk']['block_number'].max()
ax.broken_barh([(publish_tpk_1_min,publish_tpk_1_max-publish_tpk_1_min),
                ], dimensions_barh, facecolors=('green'), edgecolors=('black'), alpha=0.25,hatch="o",label="publish tpk (1)")#, label="publish tpk", hatch="--")

encrypt_shares_1 = df[df['block_number']<df[df['function_name']=='send_file']['block_number'].min()]
encrypt_shares_1_min = encrypt_shares_1[encrypt_shares_1['function_name']=='encrypt_shares']['block_number'].min()
encrypt_shares_1_max = encrypt_shares_1[encrypt_shares_1['function_name']=='encrypt_shares']['block_number'].max()
ax.broken_barh([(encrypt_shares_1_min,encrypt_shares_1_max-encrypt_shares_1_min),
                ], dimensions_barh, facecolors=('blue'), edgecolors=('black'), alpha=0.25,hatch=".",label="encrypt shares (1)")#, label="publish tpk", hatch="--")

# Récupère le block_number de publish_group_key avant la deuxième publication
publish_group_key_1 = df[df['block_number']<df[df['function_name']=='send_file']['block_number'].min()]
publish_group_key_1_min = publish_group_key_1[publish_group_key_1['function_name']=='publish_group_key']['block_number'].min()
publish_group_key_1_max = publish_group_key_1[publish_group_key_1['function_name']=='publish_group_key']['block_number'].max()
ax.broken_barh([(publish_group_key_1_min,publish_group_key_1_max-publish_group_key_1_min),
                ], dimensions_barh, facecolors=('yellow'), edgecolors=('black'), alpha=0.25,hatch="--",label="publish group key (1)")#, label="publish tpk", hatch="--")

#print(test[test['function_name']=='publish_group_key']['block_number'].max())

# Considering the init_phase = group_creation+publish_tpk+encrypt_shares+publish_group_key
#min_block_init = df[df['function_name']=='group_creation']['block_number'].min()
#max_block_init = df[df['function_name']=='send_file']['block_number'].max()-1

min_block_encryption = df[df['function_name']=='send_file']['block_number'].min()
max_block_encryption = df[df['function_name']=='send_file']['block_number'].max()

ax.broken_barh([(min_block_encryption,1),
                ], dimensions_barh, facecolors=('purple'), edgecolors=('black'), alpha=0.5,hatch="\\",label="file encryption")#, label="publish tpk", hatch="--")


#min_block_newtpk = df[df['function_name']=='send_file']['block_number'].min()+1
#max_block_newtpk = df[df['function_name']=='publish_group_key']['block_number'].max()

publish_tpk_2 = df[df['block_number']>df[df['function_name']=='send_file']['block_number'].min()]
publish_tpk_2_min = publish_tpk_2[publish_tpk_2['function_name']=='publish_tpk']['block_number'].min()
publish_tpk_2_max = publish_tpk_2[publish_tpk_2['function_name']=='publish_tpk']['block_number'].max()
ax.broken_barh([(publish_tpk_2_min,publish_tpk_2_max-publish_tpk_2_min),
                ], dimensions_barh, facecolors=('green'), edgecolors=('black'), alpha=0.25,hatch="o",label="publish tpk (2)")#, label="publish tpk", hatch="--")

encrypt_shares_2 = df[df['block_number']>df[df['function_name']=='send_file']['block_number'].max()]
encrypt_shares_2_min = encrypt_shares_2[encrypt_shares_2['function_name']=='encrypt_shares']['block_number'].min()
encrypt_shares_2_max = encrypt_shares_2[encrypt_shares_2['function_name']=='encrypt_shares']['block_number'].max()
ax.broken_barh([(encrypt_shares_2_min,encrypt_shares_2_max-encrypt_shares_2_min),
                ], dimensions_barh, facecolors=('blue'), edgecolors=('black'), alpha=0.25,hatch=".",label="encrypt shares (2)")#, label="publish tpk", hatch="--")

# Récupère le block_number de publish_group_key avant la deuxième publication
publish_group_key_2 = df[df['block_number']>df[df['function_name']=='send_file']['block_number'].max()]
publish_group_key_2_min = publish_group_key_2[publish_group_key_2['function_name']=='publish_group_key']['block_number'].min()
publish_group_key_2_max = publish_group_key_2[publish_group_key_2['function_name']=='publish_group_key']['block_number'].max()
ax.broken_barh([(publish_group_key_2_min,publish_group_key_2_max-publish_group_key_2_min),
                ], dimensions_barh, facecolors=('yellow'), edgecolors=('black'), alpha=0.25,hatch="--",label="publish group key (2)")#, label="publish tpk", hatch="--")




min_block_decryption = df[df['function_name']=='send_share']['block_number'].min()
max_block_decryption = df[df['function_name']=='send_share']['block_number'].max()

ax.broken_barh([(min_block_decryption,max_block_decryption-min_block_decryption),
                ], dimensions_barh, facecolors=('purple'), edgecolors=('black'), alpha=0.5,hatch="/",label="file decryption")#, label="publish tpk", hatch="--")



ax.text(x=location_title[0],
                    y=location_title[1],
                    s="Protocol phases",
                    ha='center',
                    va='center',
                    color='black',
                    fontsize=24,
                   )

ax.legend(loc="lower right",title="Legend",framealpha=1)

# ax.broken_barh([#(group_creation_event,1),
#                 #(min_block_init,max_block_init-min_block_init),
#                 (min_block_encryption,max_block_encryption-min_block_encryption+1),
#                 #(min_block_newtpk,max_block_newtpk-min_block_newtpk),
#                 (min_block_decryption,max_block_decryption-min_block_decryption),
#                 ], (0.25e7,1.5e7), facecolors=('purple','orange'), edgecolors=('black'), alpha=0.25)#, label="publish tpk", hatch="--")

#axes[-1].set_ylabel('Phase',fontsize=24)
#ax.tick_params(axis='y')
#axes[-1].set_yticklabels([])
#axes[0].set_xlabel('No. Block',fontsize=24)
ax.set_xlabel('No. Block',fontsize=24)
plt.title("Cumulative Gas Consumption Distribution per protocol phase",fontsize=20)
plt.show()


#%%% EVOLUTION OF GAS CONSO PER NUMBER OF GROUP MEMBERS

_,ax = plt.subplots()
file_path_2 = "client/gas_cost/gas_cost_2.csv"
df_2 = pd.read_csv(file_path_2, names=columns)
file_path_4 = "client/gas_cost/gas_cost_4.csv"
df_4 = pd.read_csv(file_path_4, names=columns)
file_path_6 = "client/gas_cost/gas_cost_6.csv"
df_6 = pd.read_csv(file_path_6, names=columns)
file_path_8 = "client/gas_cost/gas_cost_8.csv"
df_8 = pd.read_csv(file_path_8, names=columns)
file_path_10 = "client/gas_cost/gas_cost_10.csv"
df_10 = pd.read_csv(file_path_10, names=columns)

list_df = [(2,df_2),(4,df_4),(6,df_6),(8,df_8),(10,df_10)]

# associate round to each function
for i,df in list_df:
    group_size = len(df.user_id.unique())
    group = list(df.user_id.unique())

    df['round'] = 0
    for user in group:
        for fun in fun_list:
            df.loc[(df['user_id']==user) & (df['function_name']==fun),'round'] = range(len(df[(df['user_id']==user) & (df['function_name']==fun)]))

df_2['client_number'] = 2
df_4['client_number'] = 4
df_6['client_number'] = 6
df_8['client_number'] = 8
df_10['client_number'] = 10

df = pd.concat([df_2, df_4, df_6, df_8, df_10])
df = df.groupby(['client_number', 'round', 'function_name']).mean().drop(columns=['block_number']).reset_index()
# analyse round 0
round_0 = df[df['round']==0].drop(columns='round').groupby(['client_number','function_name']).mean().unstack(level=1)['gas_cost']
round_0.plot.bar(alpha=0.75, edgecolor="black",ax=ax)
round_0=round_0.reset_index()
print(round_0)
for i in range(round_0["client_number"].size):

    print(round_0['group_creation'][i])
    ax.text(i-0.3,round_0['group_creation'][i]+2.5e4, str(format(round_0['group_creation'][i]/1000000,".2f"))+'e6',verticalalignment='center')#,withdash=True)


linear_regressor_gc = LinearRegression()
linear_regressor_gc.fit(np.array(round_0.index).reshape((-1,1)), round_0['group_creation'])
x=np.linspace(0,4,100)
y = linear_regressor_gc.predict(x.reshape(-1,1))
plt.plot(x-0.125,y, label='a0={:.0f} a1={:.0f}'.format(linear_regressor_gc.intercept_, linear_regressor_gc.coef_[0]),color="orange")
#plt.legend()

round_0['cumul']=round_0['encrypt_shares']+round_0['publish_tpk']+round_0['publish_group_key']+round_0['send_file']+round_0['send_share']
linear_regressor_es = LinearRegression()
linear_regressor_es.fit(np.array(round_0.index).reshape((-1,1)), (round_0['cumul']))
x=np.linspace(0,4,100)
y = linear_regressor_es.predict(x.reshape(-1,1))
plt.plot(x-0.2,y, label='a0={:.0f} a1={:.0f}'.format(linear_regressor_es.intercept_, linear_regressor_es.coef_[0]),color="black")


plt.xlabel("No. of group members",fontsize=24)
plt.ylabel('Gas cost',fontsize=24)
plt.title("Evolution of the gas cost for each function per number of group members", fontsize=20)
plt.legend(["linear group","linear others","encrypt shares","group creation","publish group key", "publish tpk", "file encryption","file decryption"],title="Legend",framealpha=1)
plt.show()

quit()
