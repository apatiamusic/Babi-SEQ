# sequencer/pattern_manager.py
# Bu dosya, pattern'lerin yüklenmesi, kaydedilmesi ve yönetilmesi işlevlerini içerir

import os
import json
import config

class PatternManager:
    """Pattern yükleme, kaydetme ve yönetme sınıfı"""
    
    def __init__(self, stepController=None):
        """PatternManager sınıfını başlat
        
        Args:
            stepController: StepController nesnesi, None ise sonradan setStepController() ile atanabilir
        """
        self.stepController = stepController
        self.modsDir = config.ModsDir
        
        # Klasörün var olduğundan emin ol
        self._ensureModsDirectory()
    
    def setStepController(self, stepController):
        """Step controller referansını ayarla
        
        Args:
            stepController: StepController nesnesi
        """
        self.stepController = stepController
    
    def _ensureModsDirectory(self):
        """Mods dizininin var olduğundan emin ol"""
        try:
            # Ana Mods dizinini kontrol et ve oluştur
            if self.modsDir not in os.listdir('/'):
                os.mkdir(self.modsDir)
                print(f"Mods dizini oluşturuldu: {self.modsDir}")
        except OSError as e:
            print(f"Mods dizini oluşturma hatası: {e}")
    
    def savePattern(self, filename):
        """Mevcut pattern verilerini kaydeder
        
        Args:
            filename: Dosya adı
            
        Returns:
            bool: Kaydetme başarılıysa True, değilse False
        """
        if self.stepController is None:
            print("StepController referansı henüz atanmamış")
            return False
        
        # Dosya uzantısını kontrol et
        if not filename.endswith('.json'):
            filename += '.json'
        
        pattern_path = f"{self.modsDir}/{filename}"
        
        # Sequencer'dan pattern verilerini al
        pattern_data = self.stepController.getPatternData()
        
        try:
            with open(pattern_path, 'w') as f:
                json.dump(pattern_data, f)
            print(f"Pattern kaydedildi: {filename}")
            return True
        except OSError as e:
            print(f"Pattern kaydetme hatası: {e}")
            return False
    
    def loadPattern(self, filename):
        """Pattern verilerini yükler
        
        Args:
            filename: Dosya adı
            
        Returns:
            bool: Yükleme başarılıysa True, değilse False
        """
        if self.stepController is None:
            print("StepController referansı henüz atanmamış")
            return False
        
        # Dosya uzantısını kontrol et
        if not filename.endswith('.json'):
            filename += '.json'
        
        pattern_path = f"{self.modsDir}/{filename}"
        
        try:
            with open(pattern_path, 'r') as f:
                pattern_data = json.load(f)
                
                # Kontrol et: Daha karmaşık bir mod koleksiyonu mu?
                if "collections" in pattern_data:
                    return self._handleModCollection(pattern_data)
                else:
                    # Basit pattern formatı
                    result = self.stepController.loadPatternData(pattern_data)
                    if result:
                        print(f"Pattern yüklendi: {filename}")
                    return result
        except OSError as e:
            print(f"Pattern dosyası açılamadı: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"JSON ayrıştırma hatası: {e}")
            return False
        except Exception as e:
            print(f"Pattern yükleme hatası: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def _handleModCollection(self, pattern_data):
        """Mod koleksiyonu içeren pattern verilerini işler
        
        Args:
            pattern_data: Pattern verileri
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        print("Mod koleksiyonu tespit edildi")
        
        # Tüm modları topla
        all_modes = []
        mode_names = []
        
        # Tüm koleksiyonları dolaş
        for collection in pattern_data.get("collections", []):
            # Koleksiyon adını al
            collection_name = collection.get("collectionName", "İsimsiz Koleksiyon")
            
            # Koleksiyondaki tüm modları dolaş
            for mode in collection.get("modes", []):
                # Mod adını ve mode objesini sakla
                mode_name = mode.get("name", "İsimsiz Mod")
                all_modes.append(mode)
                mode_names.append(f"{mode_name}")
        
        # Mod bulunmadıysa hata ver
        if not mode_names:
            print("Dosyada mod bulunamadı")
            return False
        
        print(f"Toplam {len(mode_names)} mod bulundu")
        print(f"Modlar: {mode_names}")
        
        # Şu aşamada dokunmatik ekran yönetimi olmadığı için
        # ilk modu otomatik seçelim veya kullanıcıya bilgi verelim
        if len(all_modes) == 1:
            # Tek mod varsa direkt yükle
            selected_mode = all_modes[0]
            return self._loadStepsFromMode(selected_mode)
        else:
            # Birden çok mod var - ilk modu yükle ve kullanıcıya bilgi ver
            print("Birden çok mod bulundu, ilk mod yükleniyor")
            print("Diğer modları seçmek için ileri aşamada UI kullanabilirsiniz")
            selected_mode = all_modes[0]
            return self._loadStepsFromMode(selected_mode)
    
    def _loadStepsFromMode(self, mode_data):
        """Mod verisinden steps bilgilerini alıp sequencer'a yükler
        
        Args:
            mode_data: Mod verileri
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        try:
            # Mode içindeki steps verisini al
            steps = mode_data.get("steps", [])
            
            if not steps:
                print("Adım verisi bulunamadı")
                return False
            
            print(f"Mod içinde {len(steps)} adım bulundu")
            mode_name = mode_data.get("name", "İsimsiz Mod")
            
            # StepController için uygun formata dönüştür
            pattern_data = {"steps": steps}
            
            # StepController'a yükle
            result = self.stepController.loadPatternData(pattern_data)
            
            if result:
                print(f"Mod yüklendi: {mode_name}")
            return result
            
        except Exception as e:
            print(f"Mod yükleme hatası: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def listPatterns(self):
        """Mods dizinindeki tüm pattern dosyalarını listeler
        
        Returns:
            list: Pattern dosya adlarının listesi
        """
        try:
            # Debug bilgileri
            print(f"ModsDir: {self.modsDir}")
            
            # Mods dizini var mı kontrol et
            if self.modsDir not in os.listdir('/'):
                print(f"Mods dizini bulunamadı: {self.modsDir}")
                self._ensureModsDirectory()
                return []
                
            # Dosyaları listele
            all_files = os.listdir(self.modsDir)
            
            # JSON dosyalarını filtrele
            patterns = [f for f in all_files if f.endswith('.json') and f != 'config.json']
            print(f"Bulunan patterns: {patterns}")
            return patterns
        except OSError as e:
            print(f"Pattern listesi alma hatası: {e}")
            return []
    
    def saveConfig(self, configData):
        """Konfigürasyon verilerini kaydeder
        
        Args:
            configData: Konfigürasyon verileri
            
        Returns:
            bool: Kaydetme başarılıysa True, değilse False
        """
        config_path = f"{self.modsDir}/config.json"
        
        try:
            with open(config_path, 'w') as f:
                json.dump(configData, f)
            print("Konfigürasyon kaydedildi")
            return True
        except OSError as e:
            print(f"Konfigürasyon kaydetme hatası: {e}")
            return False
    
    def loadConfig(self):
        """Kaydedilmiş konfigürasyonu yükler
        
        Returns:
            dict: Konfigürasyon verileri, yükleme başarısız olursa None
        """
        config_path = f"{self.modsDir}/config.json"
        
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                print("Konfigürasyon yüklendi")
                return config_data
        except (OSError, json.JSONDecodeError) as e:
            print(f"Konfigürasyon yükleme hatası: {e}")
            return None