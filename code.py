Nous importons ici les librairie dont nous avons besoin; nous renommons nos fichier pour une meilleur lisibilité. 

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
erp = pd.read_csv("erp.csv")
web = pd.read_csv("web.csv")
liaison = pd.read_csv("liaison.csv")

Nous allons procéder à la vérification de nos fichiers 

# On affiche les premieres ligne du fichier;
erp.head()

# on vérifie les valeurs manquantes sur le fichier;
erp.isnull().sum()

# On affiche les premieres ligne du fichier;
web.head()

# on vérifie les valeurs manquantes sur le fichier;
web.isnull().sum()

# on supprime tous les valeurs manquantes;
web.dropna(subset= ['sku','post_mime_type'],inplace= True)

# On affiche les premieres ligne du fichier;
liaison

# on vérifie les valeurs manquantes sur le fichier;
liaison.isnull().sum()

# on supprime tous les valeurs manquantes;
liaison.dropna(inplace= True)

# Requete 1: mise en relation erp et web; 
web.rename(columns={'sku': 'id_web'}, inplace=True)
liaison_erp = pd.merge(erp,liaison)
tableau = pd.merge(web, liaison_erp, how = 'left', on= ['id_web'])
tableau.shape

# requete 2: chiffre d'affaire par produit et chiffre d'affaitre total en ligne;

tableau.insert(4,'CA_product',tableau['price'] * tableau['total_sales'])
CA = tableau[["product_id", "id_web", "price", "total_sales", "CA_product"]]
CA

print("Le chiffre d'affaire total est de : ", tableau['CA_product'].sum(),'€')
# on repère visuellement les outliers 
plt.figure(figsize=(5,10))
sns.boxplot(y = tableau['price'])
plt.title('boxplot des prix')
plt.show()

# on repere mathématiquement les outliers 

# méthode interquartille
# quartille q1, q3 et écart inter:
 
price = sorted(tableau['price'])
q1 = round(np.percentile(price, 25))
print("Le premier quartille q1 est de:", q1)
q3 = round(np.percentile(price, 75))
print("Le troisieme quartille q3 est de:", q3)
iqr = q3 - q1
print("L'écart interquartille iqr est de:", iqr)

# borne inf et sup: 

lower_bound = q1 -(1.5 * iqr)
upper_bound = q3 +(1.5 * iqr)
print('les valeurs sont considéré comme abérante si elles sont compris hors de l intervalle, ',
lower_bound, upper_bound, 'selon la méthode interquartille')

# mise en évidences du nbrs de valeurs abérantes: 

tableau_outliers_up= tableau[tableau["price"]>upper_bound]
val_abe_up = tableau_outliers_up['price'].count()
tableau_outliers_down = tableau[tableau["price"]<lower_bound]
val_abe_down = tableau_outliers_down['price'].count()
print("Le nombre de valeurs abérantes est de:", val_abe_up + val_abe_down)

# On se créé 2 DataFrame pour séparé les couleurs
price_ok = tableau[(tableau['price'] < upper_bound) & (tableau['price'] > lower_bound)]
price_outliers = tableau_outliers_up 

# On creer le schema scatter; 
plt.figure(figsize=(15,7))
plt.scatter(price_ok['price'].index, price_ok['price'].values, label= 'prix')
plt.scatter(price_outliers['price'].index, price_outliers['price'].values,c='red', label= 'valeurs abérantes')
plt.title('Nuage de point des prix et valeurs abérantes')
plt.xlabel('index')
plt.ylabel('price')
plt.legend(loc="upper left")
plt.show()
Grâce de nos donnée et ce graphique nous pouvons voir la limite de notre analyse interquartille, on voit ici un nuage de point pour les valeurs abérantes et les valeurs dite conventionnelles; ici on voit que certaine valeur abérantes on été vendue et donc ne sont pas des valeurs abérantes mais des valeur exceptionnelles.
Notre analyse et certe utile et nous montre toute les valeurs qui sont hors normes mais cette analyse dois etre en correlation avec une analyse humaine.
#methode z score

mean = np.mean(tableau['price'])
std = np.std(tableau['price'])
print('la moyenne des prix est de:', mean)
print("l'écart type des prix est de:", std)
#valeur abérantes avec zscore:
limite = 3
limite_down = -3
outlier = []
for VA_abe in tableau['price']:
    z = (VA_abe-mean)/std
    if z > limite:
        outlier.append(VA_abe)
        
    elif z < limite_down:
        outlier.append(VA_abe)

print('les valeurs abérantes sont:', outlier) 
# affichage du nbrs de valeurs abérantes 
tableau['zscore']= (tableau['price']-mean)/std
val_sup = tableau[tableau['zscore']>3]
val_inf = tableau[tableau['zscore']<-3]
sup = val_sup['price'].count()
inf = val_inf['price'].count()
print("Les valeurs abérantes selon la méthode zscore sont de:",sup + inf)
