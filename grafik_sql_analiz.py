
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dosya_yolu = r'C:\Users\ASUS\PycharmProjects\veri analizi\.venv\chrun_sql_proje.csv'

try:
    # Veriyi okuyoruz
    df = pd.read_csv(dosya_yolu, sep=';', header=None)
    df.columns = ['State', 'Account_length', 'Area_code', 'International_plan',
                  'Voice_mail_plan', 'Number_vmail_messages', 'Total_day_minutes',
                  'Total_day_calls', 'Total_day_charge', 'Total_eve_minutes',
                  'Total_eve_calls', 'Total_eve_charge', 'Total_night_minutes',
                  'Total_night_calls', 'Total_night_charge', 'Total_intl_minutes',
                  'Total_intl_calls', 'Total_intl_charge', 'Customer_service_calls', 'Churn']

    # Veri Temizliği: Boşlukları temizle ve Churn'ü sayısal yap
    df['Churn'] = df['Churn'].astype(str).str.strip()
    df['International_plan'] = df['International_plan'].astype(str).str.strip()
    df['Churn_Numeric'] = df['Churn'].map({'True': 1, 'False': 0})

    # --- GÖRSELLEŞTİRME BAŞLIYOR ---
    # 2x2'lik bir grafik alanı oluşturalım
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    plt.subplots_adjust(hspace=0.4)

    # 1. Grafik: Müşteri Hizmetleri Etkisi (Zaten biliyoruz)
    sns.countplot(ax=axes[0, 0], x='Customer_service_calls', hue='Churn', data=df, palette='viridis')
    axes[0, 0].set_title('Müşteri Hizmetleri ve Kopuşlar')

    # 2. Grafik: Uluslararası Plan Etkisi (Soru 3'ün kanıtı)
    sns.barplot(ax=axes[0, 1], x='International_plan', y='Churn_Numeric', data=df, palette='magma')
    axes[0, 1].set_title('Uluslararası Planı Olanların Kaçma Oranı')

    # 3. Grafik: Gündüz Ücretleri vs Churn (Soru 7'nin kanıtı)
    # Boxplot analistlerin "dağılımı" görmek için en çok kullandığı şeydir
    sns.boxplot(ax=axes[1, 0], x='Churn', y='Total_day_charge', data=df, palette='Set2')
    axes[1, 0].set_title('Gündüz Ücreti vs Müşteri Sadakati')

    # 4. Grafik: Toplam Arama Sayısı vs Churn
    sns.violinplot(ax=axes[1, 1], x='Churn', y='Total_day_minutes', data=df, inner="quart", palette='coolwarm')
    axes[1, 1].set_title('Gündüz Konuşma Süresi Dağılımı')
    # --- KORELASYON ANALİZİ (İstatistiksel İlişkiler) ---
    # Sadece sayısal sütunları (dakika, ücret, arama sayısı vb.) seçiyoruz
    sayisal_df = df.select_dtypes(include=['float64', 'int64'])

    # Korelasyon matrisini hesaplıyoruz (Pearson Korelasyonu)
    korelasyon = sayisal_df.corr()

    # Yeni bir pencerede Isı Haritasını (Heatmap) açalım
    plt.figure(figsize=(12, 10))
    sns.heatmap(korelasyon, annot=True, cmap='RdYlGn', fmt=".2f")
    plt.title('Değişkenler Arasındaki İstatistiksel Korelasyon (Isı Haritası)')

    # Tüm grafikleri göster
    plt.show()
    import statsmodels.api as sm

    # 1. Sayısal olmayan sütunları 0 ve 1'e çevirelim (Eğer daha önce yapmadıysan)
    df['Churn_Numeric'] = df['Churn'].apply(lambda x: 1 if x == True else 0)
    df['Int_Plan_Numeric'] = df['International_plan'].apply(lambda x: 1 if x == 'Yes' else 0)

    # 2. Modelde kullanacağımız bağımsız değişkenleri seçelim
    # Müşteri hizmetleri aramaları, Gündüz dakikası ve Uluslararası plan en güçlü adaylar
    X = df[['Customer_service_calls', 'Total_day_minutes', 'Int_Plan_Numeric']]
    X = sm.add_constant(X)  # İstatistiksel model için 'intercept' (sabit terim) ekler
    y = df['Churn_Numeric']

    # 3. Lojistik Regresyon Modelini kuralım
    logit_model = sm.Logit(y, X)
    result = logit_model.fit()

    # 4. Sonuçları ekrana yazdıralım
    print(result.summary())
    plt.suptitle('TELEKOM CHURN (MÜŞTERİ KAYBI) ANALİZ PANELİ', fontsize=20)
    plt.show()

except Exception as e:
    print(f"Bir sorun çıktı: {e}")
