import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# 1. Télécharger les prix d'un ETF (ici SPY, qui suit le S&P 500)
data = yf.download(['SOL-EUR', 'BTC-EUR', 'ETH-EUR'], start="2014-01-01", auto_adjust=True)
prix = data["Close"]

# 2. Calculer les rendements journaliers : (prix_aujourd'hui / prix_hier) - 1
rendements = prix.pct_change().dropna()


# 4. Rendement cumulé et volatilité glissante sur 20 jours
cumule = (1 + rendements).cumprod()
vol_glissante = rendements.rolling(15).std() * (252 ** 0.5)
pire_jour = rendements.min()
pire_date = rendements.idxmin()
for ticker in rendements.columns:
    print(f"Le pire jour pour {ticker} était le {pire_date[ticker].date()} avec un rendement de {pire_jour[ticker]:.2%}")
# 5. Graphiques

fig, axes = plt.subplots(4, 1, figsize=(10, 13))
prix.plot(ax=axes[0], title="Prix de clôture ajusté")
cumule.plot(ax=axes[1], title="Rendement cumulé (1 = départ)")
vol_glissante.plot(ax=axes[2], title="Volatilité annualisée (fenêtre de 15 jours)")
rendements.plot(kind='hist', bins=70, alpha=0.5, ax=axes[3], title="Histogramme des rendements journaliers")
plt.tight_layout()
plt.show()