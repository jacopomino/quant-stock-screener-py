import yahooquery as yq
import pandas as pd
import csv
from tqdm import tqdm
import logging
from pathlib import Path

# === CONFIGURAZIONE ===
NOME_FILE = "etf"  # Nome base dei file CSV
PERCORSO_INPUT = Path("azioni/CSVInput")
PERCORSO_OUTPUT = Path("azioni/CSVOutput")
PERCORSO_OUTPUT.mkdir(parents=True, exist_ok=True)

FILE_INPUT = PERCORSO_INPUT / f"{NOME_FILE}.csv"
FILE_OUTPUT = PERCORSO_OUTPUT / f"{NOME_FILE}DaComprare.csv"
FILE_LOG = PERCORSO_OUTPUT / f"{NOME_FILE}_log.txt"

# === LOGGING ===
logging.basicConfig(
    filename=FILE_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.info("=== Avvio analisi " + NOME_FILE + " ===")

FIELDNAMES = ["ticker", "volume_medio", "nome"]

# === CREA FILE CSV CON INTESTAZIONE ===
with open(FILE_OUTPUT, "w", encoding="UTF-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()


# === FUNZIONE PER CALCOLARE INDICATORI TECNICI ===
def calcola_indicatori(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) < 40:
        return df  # troppo pochi dati, evita errori

    df['SMA_14'] = df['close'].rolling(window=14).mean()
    df['SMA_40'] = df['close'].rolling(window=40).mean()

    df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    gain = df['close'].diff()
    df['Gain'] = gain.where(gain > 0, 0)
    df['Loss'] = -gain.where(gain < 0, 0)

    avg_gain = df['Gain'].rolling(window=14).mean()
    avg_loss = df['Loss'].rolling(window=14).mean()

    RS = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + RS))

    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['std_20'] = df['close'].rolling(window=20).std()
    df['Upper_Band'] = df['SMA_20'] + 2 * df['std_20']
    df['Lower_Band'] = df['SMA_20'] - 2 * df['std_20']
    df['volume_media_14'] = df['volume'].rolling(window=14).mean()

    df['Segnale_Acquisto'] = (
        (df['RSI'] < 45)
        & (df['SMA_14'] < df['SMA_40'])
        & (df["close"] - df['Lower_Band'] < df["Upper_Band"] - df["close"])
        & (df["RSI"].diff() > 0)
        & (df['Signal_Line'] > df['MACD'])
        & (df['volume'] > df['volume_media_14'])
    )
    return df


# === CARICA I TICKER ===
try:
    with open(FILE_INPUT, "r", encoding="utf-8") as filecsv:
        lettore = csv.reader(filecsv, delimiter=",")
        tickers = [(r[0].strip(), r[1].strip() if len(r) > 1 else "") for r in lettore]
except FileNotFoundError:
    print(f"❌ File di input non trovato: {FILE_INPUT}")
    logging.error("File di input mancante.")
    exit()

ticker_list = [t[0] for t in tickers]
ticker_nome = {t[0]: t[1] for t in tickers}

# === SCARICA TUTTI I DATI IN UN'UNICA CHIAMATA ===
print(f"📡 Download dati Yahoo Finance per {len(ticker_list)} ticker...")
stocks = yq.Ticker(
    ticker_list,
    asynchronous=True,  # scarica in parallelo
    max_workers=10,     # thread simultanei
    verify=False        # evita problemi SSL
)

data = stocks.history(interval="1wk", period="3y")  # 1 settimana x 3 anni = veloce e sufficiente
#data = stocks.history(interval="1mo", period="5y")

if data is None or data.empty:
    print("❌ Nessun dato scaricato.")
    logging.error("Nessun dato disponibile da YahooQuery.")
    exit()

if isinstance(data.index, pd.MultiIndex):
    data = data.reset_index()

# === CICLO SUI TICKER (LOCALE, SENZA NUOVE CHIAMATE) ===
with open(FILE_OUTPUT, "a", encoding="UTF-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

    for ticker in tqdm(sorted(data['symbol'].unique()), desc="Analisi titoli"):
        try:
            df = data[data['symbol'] == ticker].copy()
            df = calcola_indicatori(df)

            somma = df['close'].diff().dropna().sum()
            if somma > 0 and df.tail(3)['Segnale_Acquisto'].any():
                writer.writerow({
                    "ticker": ticker,
                    "volume_medio": round(float(df['volume'].mean()), 2),
                    "nome": ticker_nome.get(ticker, "")
                })
        except Exception as e:
            logging.error(f"Errore con {ticker}: {e}")
            continue

# === DEDUPLICAZIONE E ORDINAMENTO ===
try:
    df_out = pd.read_csv(FILE_OUTPUT)
    df_out = df_out.drop_duplicates(subset=["ticker"])
    df_out = df_out.sort_values(by="volume_medio", ascending=False)
    df_out.to_csv(FILE_OUTPUT, index=False, encoding="utf-8")
    logging.info("File ordinato e pulito con successo.")
except Exception as e:
    logging.error(f"Errore nel riordinamento finale: {e}")

print("✅ Analisi completata.")
print(f"📊 File salvato in: {FILE_OUTPUT}")
print(f"🪵 Log dettagliato: {FILE_LOG}")
