# process_data.py
import pandas as pd
import json
import sys

def main():
    data = None
    try:
        # 1. Veriyi Excel dosyasından oku
        data = pd.read_excel('src/analysis-py/data/satis_verileri.xlsx')
        
        # 2. Sütun adlarındaki olası baş/son boşluklarını temizle
        data.columns = data.columns.str.strip()
        
        # 3. 'Tarih' sütununu JSON için güvenli string formatına çevir
        data['Tarih'] = data['Tarih'].dt.strftime('%d.%m.%Y')

        # === ANALİZLER (ANLAŞILABİLİR HALE GETİRİLDİ) ===

        # 4. Analiz: En çok satılan ürün
        #    Ürünlere göre grupla, satışları topla, en yüksek olanın adını al.
        en_cok_satan_urun = data.groupby('Ürün_Adı')['Satış_Adedi'].sum().idxmax()
        
        # 5. Analiz: En çok satış yapılan bölge
        #    Bölgelere göre grupla, satışları topla, en yüksek olanın adını al.
        en_cok_satan_bolge = data.groupby('Bölge')['Satış_Adedi'].sum().idxmax()

        # Ürün adlarını JSON için listeye çevir
        ürün_adi = data['Ürün_Adı'].groupby(data['Ürün_Adı']).size().index.tolist()
        # Bölge adlarını JSON için listeye çevir
        bölge_adi = data['Bölge'].groupby(data['Bölge']).size().index.tolist()
        

        # 6. Analiz: Her Ürünün Memnuniyet oranları ayrı ayrı (%100 üzerinden)
        #    Bu, 'Series' hatasını düzelten ve mantığınızı doğru uygulayan koddur.
        # her ürün için Müşteri_Memnuniyeti alanındaki yüksek orta düşük alanlarını sayısal veriye çevirmemiz gerekli
        # yüzdesini almalıyız her ürün için
        memnuniyet_oranlari = {}
        for memnuniyet in data["Müşteri_Memnuniyeti"].unique():
            memnuniyet_oranlari[memnuniyet] = data[data["Müşteri_Memnuniyeti"] == memnuniyet].groupby("Ürün_Adı")["Müşteri_Memnuniyeti"].count().mul(10).mean()

        # 7. React Tablosu için tüm veriyi hazırla
        data_for_json = data.to_dict('records')
        
        # 8. Sonucu hazırla (Tüm analizler Python dict/str/int formatında)
        result = {
            "analysis_result": {
                "en_cok_satan_urun": en_cok_satan_urun,
                "en_cok_satan_bolge": en_cok_satan_bolge,
                "memnuniyet_oranlari_yuzde": memnuniyet_oranlari,
                "ürün_adi": ürün_adi,
                "bölge_adi": bölge_adi
            },
            "data_table": data_for_json 
        }
        
        # 9. Sonucu (bir kez) stdout'a yaz (Türkçe karakter desteğiyle)
        print(json.dumps(result))

    except KeyError as e:
        # Hata ayıklama kodumuz hala çok değerli, kalsın
        available_columns = "Excel dosyası okunamadı veya boş."
        if data is not None:
            available_columns = list(data.columns)
            
        error_message = (
            f"Sütun hatası (KeyError): {str(e)} sütunu bulunamadı. "
            f"Excel dosyasındaki gerçek sütun adları şunlar: {available_columns}"
        )
        error_output = {"status": "error", "message": error_message}
        print(json.dumps(error_output, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        # Diğer tüm hatalar için
        error_output = {"status": "error", "message": str(e)}
        print(json.dumps(error_output, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()