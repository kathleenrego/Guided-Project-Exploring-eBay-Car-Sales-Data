# -*- coding: utf-8 -*-
"""Basics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cNUEWr1NPEQ9Y0tQru3gfUhqr5H6sFNg

# **Projeto de exploração de dados de vendas de carros do eBay**

Prof. Ivanovitch Silva

UFRN - 2021.2

## **Integrantes**

*   Kathleen Noemi Duarte Rego

*   Pedro Henrique de Souza Fonsêca dos Santos

## **Informações do Projeto**

### O dataset é composto de 50.000 dados de vendas
e nosso objetivo é limpar os dados e analisar as listagens de carros.



A base é composta pelos dados a seguir:

* **dateCrawled:** Quando este anúncio foi rastreado pela primeira vez.
Todos os valores de campo são obtidos a partir desta data;
* **name:** Nome do carro;
* **seller:** Se o vendedor é particular ou revendedor.
* **offerType:** O tipo de listagem
* **price:** O preço do anúncio de venda do carro.
* **abtest:** Se a lista está incluída em um teste A / B.
* **vehicleType:** O tipo de veículo.
* **yearOfRegistration:** O ano em que o carro foi registrado pela primeira vez.
* **gearbox:** O tipo de transmissão.
* **powerPS:** O poder do carro no PS.
* **model:** O nome do modelo do carro.
* **kilometer:** Quantos quilômetros o carro percorreu.
* **monthOfRegistration:** O mês em que o carro foi registrado pela primeira vez.
* **fuelType:** Que tipo de combustível o carro usa.
* **brand:** A marca do carro.
* **notRepairedDamage:** Se o carro apresentar danos que ainda não foram reparados.
* **dateCreated:** A data em que a lista do eBay foi criada.
* **nrOfPictures:** O número de fotos no anúncio.
* **postalCode:** O código postal da localização do veículo.
* **lastSeenOnline:** Quando o rastreador viu este anúncio online pela última vez.
"""

import pandas as pd

autos = pd.read_csv("autos.csv", encoding="Latin-1")

print(autos)

autos.info()
autos.head()

print(autos.columns)

mapping_dict = {'yearOfRegistration': 'registration_year',
                'monthOfRegistration': 'registration_month',
                'notRepairedDamage': 'unrepaired_damage',
                'dateCreated': 'ad_created',
                'postalCode': 'postal_code',
                'lastSeen': 'last_seen',
                'nrOfPictures': 'number_of_pictures',
                'vehicleType': 'vehicle_type',
                'fuelType': 'fuel_type',
                'dateCrawled': 'ad_crawled',
                'offerType': 'offer_type',
                'powerPS': 'power_ps'}
autos.rename(columns = mapping_dict, inplace=True)
autos.head()

autos.describe(include='all')

autos['price'] = autos['price'].str.replace('$','').str.replace(',','').astype(int)
autos['odometer'] = autos['odometer'].str.replace('km','').str.replace(',','').astype(int)
autos.rename(columns = {'odometer' : 'odometer_km'}, inplace = True)

autos.head()

autos['odometer_km'].describe()
autos['odometer_km'].value_counts().sort_index(ascending=True)

autos['price'].describe()
autos['price'].value_counts().sort_index(ascending=True).tail(50)

autos = autos[autos['price'].between(500,100000)]

autos['ad_crawled'].str[:10].value_counts(normalize = True, dropna = False).sort_index()

autos['ad_created'].str[:10].value_counts(normalize = True, dropna = False).sort_index()

autos['last_seen'].str[:10].value_counts(normalize = True, dropna = False).sort_index()

autos['registration_year'].describe()

autos = autos[autos['registration_year'].between(1950, 2016)]

autos['registration_year'].value_counts(normalize = True, dropna = False).sort_index().head(50)

autos['brand'].unique()

autos['brand'].value_counts(normalize=True)

brand_counts = autos['brand'].value_counts(normalize=True)
best_brands = brand_counts[brand_counts > 0.05].index
print(best_brands)

def brands_mean_column(some_brands, data, column):
    """Retorna uma média da coluna escolhida para as marcas selecionadas.

    Args:
        some_brands (str): Marcas escolhidas.
        data (pandas dataframe): DataFrame com os dados.
        column (str): Coluna escolhida.

    Return:
        Dict: Um dicionário com as marcas como palavras chaves
        e os valores médios das marcas.
    """
    brands_mean = {}
    for brand in some_brands:
        brand_chosen = data[data['brand'] == brand]
        mean_column = brand_chosen[column].mean()
        brands_mean[brand] = int(mean_column)
    return brands_mean

brands_mean_prices = brands_mean_column(best_brands, autos, column='price')
print(brands_mean_prices)

brands_mean_km = brands_mean_column(best_brands, autos, column='odometer_km')
print(brands_mean_km)

bmp_series = pd.Series(brands_mean_prices).sort_values()
bmk_series = pd.Series(brands_mean_km)

df = pd.DataFrame(bmp_series, columns = ['mean_price'])
df['mean_km'] = bmk_series
print(df)