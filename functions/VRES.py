import pandas as pd
import matplotlib.pyplot as plt

print("test")

# Funksjon som returnerer ønsket data ved å kombinere gammel og ny data

def VRES_data(category, country, starting_year = 2005, ending_year = 2018, plot=False):
    
    path_ENTSOE_new = "riskpremium/datasets/ENTSOE_new.xlsx"
    path_ENTSOE_old = "riskpremium/datasets/ENTSOE_post_processed.xlsx"

    df_2005_2009 = pd.read_excel(path_ENTSOE_old, "MDV 2005-2009")
    df_2010_2013 = pd.read_excel(path_ENTSOE_old, "MDV 2010-2013")
    df_2014_2015 = pd.read_excel(path_ENTSOE_old, "MDV 2014-2015")
    df_2015_2019 = pd.read_excel(path_ENTSOE_new)
  
    a = df_2005_2009.drop(
        df_2005_2009.columns.difference(["Country", "Month", "Year", category]),
        axis = 1, inplace = False)

    b = df_2010_2013.drop(
        df_2010_2013.columns.difference(["Country", "Month", "Year", category]),
        axis = 1, inplace = False)

    c = df_2014_2015.drop(
        df_2014_2015.columns.difference(["Country", "Month", "Year", category]),
        axis = 1, inplace = False)

    temp = a.append(b).append(c)
    temp = temp.loc[temp["Country"] == country]


    d = df_2015_2019.loc[(df_2015_2019.Country == country) & (df_2015_2019.Category == category)]
    d = d[["Country", "Month", "Year", "ProvidedValue"]]
    d.rename(columns={"ProvidedValue": category}, inplace = True)


    df = temp.append(d)
    df.sort_values(["Year", "Month"], axis = 0, inplace = True)
    df.reset_index(inplace = True)
    df.drop("index", axis = 1, inplace=True)

    df = df[(df.Year >= starting_year) & (df.Year <= ending_year)]

    df = df.astype({category: float})
    df.dropna(inplace=True)
    
    df["Day"] = 1
    df["DateTime"] = pd.to_datetime(df[['Year', 'Month', "Day" ]])
    df.drop(columns=["Month", "Year", "Day", "Country"], inplace=True)
    df.set_index("DateTime", inplace=True)
    

        if plot:
            # years = range(starting_year, ending_year+1, 1)
            #years = df.Year.unique()

            # for year in years:
            #   plt.plot(df[df.Year == year].Month, df[df.Year == year][category], label = str(year))
            plt.plot(df.groupby(by=df.index.month)[category].mean())
            plt.title(f"{category} production in {country} during the year")
            plt.xlabel("Month")
            plt.legend(loc='upper right');


    return df