# LEVEL BASED PERSONA
################# Before #####################
#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# After #####################
#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C
##############################################

#Variables
#-PRICE– Customer's spending amount
#-SOURCE– The type of device the customer is connecting to
#-SEX– Gender of the client
#-COUNTRY– Customer's country
#-AGE– Age of the customer

import pandas as pd

#GÖREV 1
#Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
def load_dataset():
    df = pd.read_csv(r"C:\Users\User\Desktop\VBO\PycharmProjects\pythonProject\datasets\persona.csv");
    return df

df = load_dataset()

df.head() #ilk 5 gözlem
df.tail() #son 5 gözlem
df.shape #satır ve sutün
df.columns #kolon isimleri
df.index #index bilgileri
df.isnull().sum() #eksik değer gözlemi
df.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T
df.info() #değişken tipleri hakkında biilgiler

#Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique() #sınıf sayısı
df["SOURCE"].unique() #sınıflar gözlemleniyor
df["SOURCE"].value_counts() #frekans

#Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()

#Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

#Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()

#Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE": "sum"})

#Soru 7: SOURCE türlerine göre göre satış sayıları nedir?
df["SOURCE"].value_counts()

#Soru 8 : Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE": "mean"})

#Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE": "mean"})

#Soru 10 :  COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})


#GÖREV 2
#COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"})
df.pivot_table(index=["COUNTRY", "SOURCE", "SEX", "AGE"], values="PRICE")

#GÖREV 3
#Çıktıyı PRICE’a göre sıralayınız.
agg_df = df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"})
agg_df = agg_df.sort_values(by="PRICE", ascending=False)
agg_df.head()

#GÖREV 4
#Index’te yer alan isimleri değişken ismine çeviriniz
agg_df = agg_df.reset_index()
agg_df.head()

#GÖREV 5
#AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
# AGE değişkeninin nerelerden bölüneceğini belirtelim:
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

# Bölünen noktalara karşılık isimlendirmelerin ne olacağını ifade edelim:
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

# age'i bölelim:
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
pd.set_option('display.max_rows', None)
agg_df.head()

# GÖREV 6
# Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
# değişken isimleri:
agg_df.columns

# gözlem değerlerine nasıl erişiriz?
for row in agg_df.values:
    print(row)

# COUNTRY, SOURCE, SEX ve age_cat değişkenlerinin DEĞERLERİNİ yan yana koymak ve alt tireyle birleştirmek istiyoruz.
# Bunu list comprehension ile yapabiliriz.
# Yukarıdaki döngüdeki gözlem değerlerinin bize lazım olanlarını seçecek şekilde işlemi gerçekletirelim:
[row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
# Veri setine ekleyelim:
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper()
                                   for row in agg_df.values]
agg_df.head()

# Gereksiz değişkenleri çıkaralım:
agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

# kontrol edelim:
agg_df["customers_level_based"].value_counts()

# Bu sebeple segmentlere göre groupby yaptıktan sonra price ortalamalarını almalı ve segmentleri tekilleştirmeliyiz.
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df.head()

# customers_level_based index'te yer almaktadır. Bunu değişkene çevirelim.
agg_df = agg_df.reset_index()
agg_df.head()

# kontrol edelim. her bir persona'nın 1 tane olmasını bekleriz:
agg_df["customers_level_based"].value_counts()
agg_df.head()

# GÖREV 7
# Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
# Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
# Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).
# C segmentini analiz ediniz (Veri setinden sadece C segmentini çekip analiz ediniz)

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]})
agg_df[agg_df["SEGMENT"] == "C"]

# GÖREV 8
# Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]