// Gerekli modülleri import et
const { spawn } = require('child_process');
const path = require('path'); // Dosya yolunu doğru oluşturmak için

const data_get = (req, res) => {
  // 1. Python'a göndereceğimiz veri
  const dataToPython = {
    message: "Data controller is working",
  };
  // Veriyi JSON string formatına çevir
  const dataString = JSON.stringify(dataToPython);

  // 2. Python betiğinin yolunu belirle
  // __dirname, bu JS dosyasının bulunduğu dizini verir
  const scriptPath = path.join(__dirname, '../analysis-py/main.py');

  // 3. 'spawn' ile Python betiğini çalıştır
  // 'python3' komutu sisteminizde 'python' olabilir, gerekirse değiştirin
  const pythonProcess = spawn('py', [scriptPath, dataString]);

  // 4. Python'dan gelen verileri (çıktıları) biriktirmek için değişkenler
  let pythonResult = '';
  let pythonError = '';

  // 5. Python betiğinin 'print()' çıktılarını (stdout) dinle
  pythonProcess.stdout.on('data', (data) => {
    pythonResult += data.toString();
  });

  // 6. Python betiğinin hata (stderr) çıktılarını dinle
  pythonProcess.stderr.on('data', (data) => {
    pythonError += data.toString();
  });

  // 7. Python betiği çalışmayı bitirdiğinde (kapandığında)
  pythonProcess.on('close', (code) => {
    console.log(`Python betiği ${code} koduyla kapandı.`);

    // 8. Önce HATA kontrolü yap
    if (pythonError) {
      console.error("Python Hatası (stderr):", pythonError);
      try {
        // Hata mesajı JSON olabilir
        const errorJson = JSON.parse(pythonError);
        return res.status(500).json({ error: "Python betiğinde hata oluştu", details: errorJson });
      } catch (e) {
        return res.status(500).json({ error: "Python betiğinde hata oluştu", details: pythonError });
      }
    }

    // 9. Hata yoksa, BAŞARILI sonucu gönder
    try {
      // Python'dan gelen JSON string'i parse et
      const finalResult = JSON.parse(pythonResult);
      // React'e (veya isteği atana) sonucu gönder
      res.status(200).json(finalResult);

    } catch (e) {
      console.error("Python çıktısı parse hatası:", e);
      res.status(500).json({ error: "Python çıktısı (JSON) parse edilemedi", details: pythonResult });
    }
  });
};

module.exports = {
  data_get
};