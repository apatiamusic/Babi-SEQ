# hardware/display.py
# Kısmi güncelleme desteği ile geliştirilmiş versiyon

from machine import Pin, SPI
import time
import config
from lib.ili9341 import Display, color565
from lib.xglcd_font import XglcdFont

class DisplayManager:
    """TFT ekran yönetimi için geliştirilmiş sınıf - kısmi güncelleme desteği ile"""
    
    # Renk sabitleri - Önceden hesaplanmış sabit değerler
    COLOR_BLUE = color565(0, 86, 255)      # Mavi
    COLOR_RED = color565(210, 11, 0)       # Kırmızı
    COLOR_GREEN = color565(0, 201, 51)     # Yeşil
    COLOR_PURPLE = color565(223, 0, 194)   # Mor
    COLOR_ORANGE = color565(255, 132, 42)  # Turuncu
    COLOR_GRAY = color565(198, 198, 198)   # Gri
    COLOR_WHITE = color565(255, 255, 255)  # Beyaz
    COLOR_BLACK = color565(0, 0, 0)        # Siyah
    
    def __init__(self):
        """DisplayManager sınıfını başlat - ekranTest.py yaklaşımı ile"""
        # SPI bağlantısını kur
        self.spi = SPI(0, baudrate=40000000, sck=Pin(config.tftSck), mosi=Pin(config.tftMosi))
        self.display = Display(self.spi,
                             dc=Pin(config.tftDc),
                             cs=Pin(config.tftCs),
                             rst=Pin(config.tftRst),
                             rotation=90)
        
        # Boyutları değişkenlere al
        self.width = self.display.width
        self.height = self.display.height
        
        # Fontları yükle
        try:
            self.unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
            print("Unispace font yüklendi")
        except Exception as e:
            print(f"Unispace font yüklenemedi: {e}")
            self.unispace = None
        
        # Ekranı temizle
        self.clear()
        
        # Bölge takibi için değişkenler
        self.dirty_regions = []  # Güncellenmesi gereken bölgeler [(x, y, w, h), ...]
        self.last_states = {}   # Son durumlar - key: bölge_id, value: durum
        
        print(f"DisplayManager başlatıldı: {self.width}x{self.height} piksel")

    def clear(self):
        """Tüm ekranı siyah yapar"""
        try:
            self.display.fill_rectangle(0, 0, self.width, self.height, self.COLOR_BLACK)
            # Tüm güncelleme bölgelerini temizle
            self.dirty_regions = []
            self.last_states = {}
        except Exception as e:
            print(f"Ekran temizleme hatası: {e}")
    
    def mark_region_dirty(self, x, y, width, height, region_id=None):
        """Bir bölgeyi güncellenecek olarak işaretle
        
        Args:
            x, y, width, height: Bölge koordinatları ve boyutları
            region_id: Bölge ID'si (opsiyonel), belirtilirse bu ID'ye sahip önceki bölge güncellenir
        """
        # Koordinatları ekran sınırları içinde tut
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))
        width = max(1, min(width, self.width - x))
        height = max(1, min(height, self.height - y))
        
        region = (x, y, width, height)
        
        # Eğer belirli bir bölge ID'si belirtilmişse
        if region_id is not None:
            # Eğer aynı ID'ye sahip bir bölge varsa, güncelle
            for i, (rx, ry, rw, rh, rid) in enumerate(self.dirty_regions):
                if rid == region_id:
                    self.dirty_regions[i] = (x, y, width, height, region_id)
                    return
            
            # Aynı ID'ye sahip bölge yoksa, yeni ekle
            self.dirty_regions.append((x, y, width, height, region_id))
        else:
            # ID belirtilmemişse doğrudan ekle
            self.dirty_regions.append((x, y, width, height, None))
    
    def compare_and_update(self, region_id, new_state):
        """Durum değişikliğini kontrol et ve değişiklik varsa bölgeyi güncelle
        
        Args:
            region_id: Bölge ID'si
            new_state: Yeni durum değeri (herhangi bir tip)
            
        Returns:
            bool: Durum değişti mi?
        """
        # Mevcut durumu kontrol et
        old_state = self.last_states.get(region_id)
        
        # Eğer durum değişmişse
        if old_state != new_state:
            # Yeni durumu kaydet
            self.last_states[region_id] = new_state
            return True
        
        return False
    
    def update_dirty_regions(self):
        """İşaretlenmiş bölgeleri güncelle"""
        if not self.dirty_regions:
            return
        
        # Optimize edilmiş bölgeler (birleşebilecek alanlar birleştirilir)
        optimized_regions = self._optimize_regions(self.dirty_regions)
        
        # Her bölgeyi güncelle
        for region in optimized_regions:
            x, y, w, h = region[:4]  # ID varsa 5. eleman olacak
            
            # Bölgeyi güncelle burada - özel güncelleme fonksiyonları kullanılabilir
            # Bu örnek için sadece siyah dikdörtgen çiziyoruz
            self.display.fill_rectangle(x, y, w, h, self.COLOR_BLACK)
        
        # Kirli bölgeleri temizle
        self.dirty_regions = []
    
    def _optimize_regions(self, regions):
        """Bölgeleri optimize et - çakışan veya yakın bölgeleri birleştir
        
        Args:
            regions: Bölgeler listesi [(x, y, w, h, id), ...]
            
        Returns:
            list: Optimize edilmiş bölgeler [(x, y, w, h), ...]
        """
        if not regions:
            return []
        
        # ID'leri sil ve sadece koordinatları kullan
        simple_regions = [(r[0], r[1], r[2], r[3]) for r in regions]
        
        # Basit yaklaşım: Tüm bölgeleri kapsayan tek bir dikdörtgen oluştur
        # Daha gelişmiş optimizasyon için algoritma geliştirilebilir
        min_x = min(r[0] for r in simple_regions)
        min_y = min(r[1] for r in simple_regions)
        max_x = max(r[0] + r[2] for r in simple_regions)
        max_y = max(r[1] + r[3] for r in simple_regions)
        
        # Tek bir optimize edilmiş bölge döndür
        return [(min_x, min_y, max_x - min_x, max_y - min_y)]
    
    # Status alanlarında kullanılacak özel fonksiyonlar 
    def update_status_area(self, mode, tempo, playing, step):
        """Durum alanını güncelle - sadece gerekli alanları günceller
        
        Args:
            mode: Mod ("FREQ" veya "MIDI")
            tempo: Tempo değeri
            playing: Çalıyor mu?
            step: Mevcut adım
        """
        # Durum alanının boyutları ve konumu
        status_x = 0
        status_y = 0
        status_width = self.width
        status_height = 30
        
        # Mod değişti mi?
        if self.compare_and_update("mode", mode):
            # Modu güncelle
            self.mark_region_dirty(status_x, status_y, 60, status_height, "mode_area")
            # Siyahla temizle ve yeni modu yaz
            self.display.fill_rectangle(status_x, status_y, 60, status_height, self.COLOR_BLACK)
            self.display.draw_text8x8(status_x + 5, status_y + 10, mode, self.COLOR_WHITE)
        
        # Tempo değişti mi?
        if self.compare_and_update("tempo", tempo):
            # Tempo alanını güncelle
            self.mark_region_dirty(status_x + 60, status_y, 70, status_height, "tempo_area")
            # Siyahla temizle ve yeni tempoyu yaz
            self.display.fill_rectangle(status_x + 60, status_y, 70, status_height, self.COLOR_BLACK)
            self.display.draw_text8x8(status_x + 65, status_y + 10, f"T:{tempo}", self.COLOR_WHITE)
        
        # Çalma durumu değişti mi?
        if self.compare_and_update("playing", playing):
            # Çalma durumu alanını güncelle
            self.mark_region_dirty(status_x + 130, status_y, 60, status_height, "play_area")
            # Siyahla temizle ve yeni durumu yaz
            self.display.fill_rectangle(status_x + 130, status_y, 60, status_height, self.COLOR_BLACK)
            status_text = "PLAY" if playing else "STOP"
            status_color = self.COLOR_GREEN if playing else self.COLOR_RED
            self.display.draw_text8x8(status_x + 135, status_y + 10, status_text, status_color)
        
        # Mevcut adım değişti mi?
        if self.compare_and_update("step", step):
            # Adım alanını güncelle
            self.mark_region_dirty(status_x + 190, status_y, 50, status_height, "step_area")
            # Siyahla temizle ve yeni adımı yaz
            self.display.fill_rectangle(status_x + 190, status_y, 50, status_height, self.COLOR_BLACK)
            self.display.draw_text8x8(status_x + 195, status_y + 10, f"S:{step+1}", self.COLOR_WHITE)
    
    
    def _draw_step_cell(self, x, y, size, step_idx, stepController, midiOutput, is_current):
        """Bir adım hücresini çiz
        
        Args:
            x, y: Hücre konumu
            size: Hücre boyutu
            step_idx: Adım indeksi
            stepController: Step Controller
            midiOutput: MIDI Output
            is_current: Mevcut adım mı?
        """
        # Adım nesnesini al
        step = stepController.steps[step_idx]
        
        # Hücre rengini belirle
        if is_current:
            cell_color = self.COLOR_RED  # Çalınan adım
        elif step.isSelected:
            cell_color = self.COLOR_WHITE  # Seçili adım
        elif step.isSolo:
            cell_color = self.COLOR_BLUE  # Solo adım
        elif step.isMuted:
            cell_color = self.COLOR_ORANGE  # Sessiz adım
        else:
            cell_color = self.COLOR_BLUE  # Normal adım
        
        # Hücreyi çiz
        self.display.fill_rectangle(x, y, size, size, cell_color)
        
        # Adım numarasını çiz
        text = str(step_idx + 1)
        text_color = self.COLOR_BLACK if cell_color in (self.COLOR_WHITE, self.COLOR_ORANGE) else self.COLOR_WHITE
        
        # Metin genişliğini hesapla ve ortala
        text_x = x + (size - len(text) * 8) // 2
        text_y = y + (size - 8) // 2
        
        self.display.draw_text8x8(text_x, text_y, text, text_color)
    


    
    def showStartupScreen(self):
        """Başlangıç ekranı - test programınızdaki drawText ve fill_rectangle kullanarak"""
        # Tamamen temizle önce
        self.clear()
        
        # Orta kısımda mavi arka plan
        self.display.fill_rectangle(0, 60, self.width, 100, color565(0, 0, 120))
        
        # Uygulama adı
        if self.unispace:
            text_x = (self.width - len(config.appName) * 12) // 2
            self.display.draw_text(text_x, 80, config.appName, self.unispace, color565(255, 255, 0))
            
            # Versiyon
            version_text = f"v{config.appVersion}"
            text_x = (self.width - len(version_text) * 12) // 2
            self.display.draw_text(text_x, 120, version_text, self.unispace, color565(255, 255, 255))
        else:
            # Sistem fontu ile
            self.display.draw_text8x8(10, 90, config.appName, color565(255, 255, 0))
            self.display.draw_text8x8(10, 120, f"v{config.appVersion}", color565(255, 255, 255))
        
        # Alt bilgi
        self.display.draw_text8x8(110, 200, "BASLATILIYOR...", color565(0, 255, 0))
    


    def showSequencerScreen(self, stepController, midiOutput):
        """Sequencer ana ekranını göster - kısmi güncelleme desteği ile
        
        Args:
            stepController: StepController nesnesi
            midiOutput: MidiOutput nesnesi
        """
        # Menü göründüyse temizle
        if hasattr(self, "_menu_initialized"):
            self.clear()
            delattr(self, "_menu_initialized")
            delattr(self, "_menu_selected_index")
        
        # İlk çağrıda tüm ekranı çiz
        if not hasattr(self, 'sequencer_screen_init') or not self.sequencer_screen_init:
            # Ekranı temizle
            self.clear()
            
            # Başlık alanı
            self.display.fill_rectangle(0, 0, self.width, 30, color565(0, 0, 100))
            self.display.draw_text8x8(10, 10, f"{'FREQ' if stepController.frequencyMode else 'MIDI'} T:{midiOutput.tempo}", self.COLOR_WHITE)
            status = "PLAY" if midiOutput.isRunning else "STOP"
            self.display.draw_text8x8(170, 10, status, self.COLOR_GREEN if midiOutput.isRunning else self.COLOR_RED)
            
            # Adım bilgisi
            self.display.draw_text8x8(10, 25, f"STEP: {midiOutput.currentStep + 1}/{stepController.totalSteps}", self.COLOR_WHITE)
            
            # Grid arka planı - gri
            self.display.fill_rectangle(0, 50, self.width, self.height - 50, color565(50, 50, 50))
            
            # Grid çizimi - ilk kez tüm grid'i çiz
            step_count = stepController.totalSteps
            cols = 8
            rows = (step_count + cols - 1) // cols
            
            cell_size = 26
            spacing = 4
            
            grid_start_x = 10
            grid_start_y = 100
            
            for step_idx in range(step_count):
                row = step_idx // cols
                col = step_idx % cols
                
                x = grid_start_x + col * (cell_size + spacing)
                y = grid_start_y + row * (cell_size + spacing)
                
                # Adım hücresini çiz
                self._draw_step_cell(x, y, cell_size, step_idx, stepController, midiOutput, step_idx == midiOutput.currentStep)
            
            # Başlangıç durumunu kaydet
            self.last_states["mode"] = "FREQ" if stepController.frequencyMode else "MIDI"
            self.last_states["tempo"] = midiOutput.tempo
            self.last_states["playing"] = midiOutput.isRunning
            self.last_states["step"] = midiOutput.currentStep
            self.last_states["previous_step"] = midiOutput.currentStep
            
            # İlk çizim tamamlandı
            self.sequencer_screen_init = True
        else:
            # Sadece değişen kısımları güncelle
            # Durum alanını güncelle
            self.update_status_area(
                "FREQ" if stepController.frequencyMode else "MIDI",
                midiOutput.tempo,
                midiOutput.isRunning,
                midiOutput.currentStep
            )
            
            # Adım grid'ini güncelle
            self.update_step_grid(stepController, midiOutput)
            
            # Tüm işaretli bölgeleri güncelle (gerekirse)
            # self.update_dirty_regions()

    
    def _drawSimpleGrid(self, stepController, midiOutput):
        """Basit step grid - sadece temel dikdörtgenler"""
        grid_start_y = 50
        
        # Basit dikdörtgen ızgara
        step_count = stepController.totalSteps
        cols = 8
        rows = (step_count + cols - 1) // cols
        
        cell_width = 30
        cell_height = 30
        spacing = 5
        
        # Arka plan - gri
        self.display.fill_rectangle(0, grid_start_y, self.width, rows * (cell_height + spacing), color565(50, 50, 50))
        
        # Grid çizimi
        for step_idx in range(step_count):
            row = step_idx // cols
            col = step_idx % cols
            
            x = col * (cell_width + spacing) + 10
            y = grid_start_y + row * (cell_height + spacing) + 5
            
            # Aktif adım farklı renk
            color = color565(255, 0, 0) if step_idx == midiOutput.currentStep else color565(0, 0, 255)
            
            # Seçili adımlar beyaz renk
            if stepController.steps[step_idx].isSelected:
                color = color565(255, 255, 255)
            
            # Basit bir kutu çiz
            self.display.fill_rectangle(x, y, cell_width, cell_height, color)
            
            # Adım numarası
            self.display.draw_text8x8(x + 10, y + 10, str(step_idx + 1), color565(0, 0, 0))
    

    def showMessage(self, message, duration=None):
        """Mesaj göster
        
        Args:
            message: Gösterilecek mesaj
            duration: Mesaj süresi (saniye), None ise kullanıcı girdisi bekler
        """
        # Mesaj kutusu boyutları
        msg_x = 30
        msg_y = 100
        msg_width = self.width - 60
        msg_height = 50
        
        # Mesaj kutusunu çiz
        self.display.fill_rectangle(msg_x, msg_y, msg_width, msg_height, color565(0, 0, 100))
        self.display.draw_rectangle(msg_x, msg_y, msg_width, msg_height, self.COLOR_WHITE)
        
        # Mesaj metnini yazdır
        if len(message) > 20:  # Çok uzunsa kes
            message = message[:17] + "..."
        
        text_x = msg_x + 10
        text_y = msg_y + 20
        self.display.draw_text8x8(text_x, text_y, message, self.COLOR_WHITE)
        
        # Süre belirtilmişse bekle
        if duration is not None and duration > 0:
            time.sleep(duration)
    
    def update_step_grid(self, stepController, midiOutput):
        """Adım grid'ini güncelle - sadece değişen adımları günceller
        
        Args:
            stepController: Step Controller
            midiOutput: MIDI Output
        """
        if not stepController or not midiOutput:
            return
        
        # Grid başlangıç pozisyonu ve hücre boyutları 
        grid_start_x = 10
        grid_start_y = 100
        cell_size = 26
        spacing = 4
        cols = 8
        
        # Mevcut adımı kontrol et ve güncelle
        current_step = midiOutput.currentStep
        if self.compare_and_update("current_step", current_step):
            # Eski mevcut adımı temizle (son durumu al)
            old_step = self.last_states.get("previous_step")
            if old_step is not None and 0 <= old_step < stepController.totalSteps:
                # Eski adımın konumunu hesapla
                old_row = old_step // cols
                old_col = old_step % cols
                old_x = grid_start_x + old_col * (cell_size + spacing)
                old_y = grid_start_y + old_row * (cell_size + spacing)
                
                # Eski adımı yeniden çiz
                self._draw_step_cell(old_x, old_y, cell_size, old_step, stepController, midiOutput, False)
            
            # Yeni mevcut adımı çiz
            if 0 <= current_step < stepController.totalSteps:
                # Yeni adımın konumunu hesapla
                new_row = current_step // cols
                new_col = current_step % cols
                new_x = grid_start_x + new_col * (cell_size + spacing)
                new_y = grid_start_y + new_row * (cell_size + spacing)
                
                # Yeni adımı çiz
                self._draw_step_cell(new_x, new_y, cell_size, current_step, stepController, midiOutput, True)
                
                # Şimdiki adımı bir sonraki karşılaştırma için sakla
                self.last_states["previous_step"] = current_step
        
        # Step durumlarını kontrol et ve değişenleri güncelle
        for step_idx in range(stepController.totalSteps):
            step = stepController.steps[step_idx]
            
            # Step durumunu bir dizi olarak temsil et (seçili, mute, solo)
            step_state = (step.isSelected, step.isMuted, step.isSolo)
            step_key = f"step_state_{step_idx}"
            
            # Durum değişti mi?
            if self.compare_and_update(step_key, step_state):
                # Adımın konumunu hesapla
                row = step_idx // cols
                col = step_idx % cols
                x = grid_start_x + col * (cell_size + spacing)
                y = grid_start_y + row * (cell_size + spacing)
                
                # Değişen adımı yeniden çiz
                self._draw_step_cell(x, y, cell_size, step_idx, stepController, midiOutput, step_idx == current_step)
                print(f"Step {step_idx+1} durumu güncellendi: {step_state}")

    def showMenu(self, items, selected_index, title="MENU"):
        """Menü ekranı - seçilen öğeyi vurgular
        
        Args:
            items: Menü öğeleri listesi
            selected_index: Seçili öğe indeksi
            title: Menü başlığı
        """
        # Önceki menü seçimini sakla
        previous_index = getattr(self, "_menu_selected_index", -1)
        
        # İlk defa çizim mi?
        if not hasattr(self, "_menu_initialized") or self._menu_initialized != title:
            # Ekranı tamamen temizle
            self.clear()
            
            # Menü başlığı
            self.display.fill_rectangle(0, 0, self.width, 30, color565(0, 0, 100))
            self.display.draw_text8x8(10, 10, title, self.COLOR_WHITE)
            
            # Menü öğelerini çiz
            max_items = min(10, len(items))
            for i in range(max_items):
                y_pos = 40 + i * 25
                
                # Seçili öğeyi vurgula
                if i == selected_index:
                    self.display.fill_rectangle(5, y_pos - 2, self.width - 10, 20, color565(0, 100, 0))
                else:
                    # Normal öğe arka planı
                    self.display.fill_rectangle(5, y_pos - 2, self.width - 10, 20, self.COLOR_BLACK)
                
                # Menü öğe metni
                self.display.draw_text8x8(10, y_pos, items[i], self.COLOR_WHITE)
            
            # Menü durumunu kaydet
            self._menu_initialized = title
            self._menu_items = items
            self._menu_max_items = max_items
        else:
            # Sadece seçili öğe değiştiyse güncelle
            if previous_index != selected_index and previous_index >= 0:
                max_items = min(10, len(items))
                
                # Eski seçili öğeyi normal hale getir
                if 0 <= previous_index < max_items:
                    prev_y_pos = 40 + previous_index * 25
                    self.display.fill_rectangle(5, prev_y_pos - 2, self.width - 10, 20, self.COLOR_BLACK)
                    self.display.draw_text8x8(10, prev_y_pos, items[previous_index], self.COLOR_WHITE)
                
                # Yeni seçili öğeyi vurgula
                if 0 <= selected_index < max_items:
                    new_y_pos = 40 + selected_index * 25
                    self.display.fill_rectangle(5, new_y_pos - 2, self.width - 10, 20, color565(0, 100, 0))
                    self.display.draw_text8x8(10, new_y_pos, items[selected_index], self.COLOR_WHITE)
        
        # Şimdiki seçili indeksi sakla
        self._menu_selected_index = selected_index
        
        print(f"Menü güncellendi: {previous_index} -> {selected_index}")
    
    
    def showPatternListScreen(self, patterns, selected_index):
        """Pattern listesi ekranı
        
        Args:
            patterns: Pattern listesi
            selected_index: Seçili pattern indeksi
        """
        # Menü formatında pattern listesini göster
        menu_items = []
        for i, pattern in enumerate(patterns):
            # Uzun isimleri kısalt
            if len(pattern) > 20:
                display_name = pattern[:17] + "..."
            else:
                display_name = pattern
            menu_items.append(f"{i+1}. {display_name}")
        
        self.showMenu(menu_items, selected_index, "PATTERNS")
    
    def showEnvelopeScreen(self, envelope, current_parameter):
        """Envelope ekranı
        
        Args:
            envelope: Envelope parametreleri
            current_parameter: Seçili parametre
        """
        # Ekranı temizle
        self.clear()
        
        # Başlık
        self.display.fill_rectangle(0, 0, self.width, 30, color565(100, 0, 100))
        self.display.draw_text8x8(10, 10, "ENVELOPE", self.COLOR_WHITE)
        
        # Parametreler
        params = [
            ("Attack", envelope.get("attack", 10), "ms"),
            ("Decay", envelope.get("decay", 100), "ms"),
            ("Sustain", envelope.get("sustain", 70), "%"),
            ("Release", envelope.get("release", 100), "ms")
        ]
        
        for i, (param_name, value, unit) in enumerate(params):
            y_pos = 40 + i * 25
            
            # Parametre seçiliyse vurgula
            if param_name.lower() == current_parameter:
                self.display.fill_rectangle(5, y_pos - 2, self.width - 10, 20, color565(0, 100, 0))
            
            # Parametre ve değeri
            text = f"{param_name}: {value} {unit}"
            self.display.draw_text8x8(10, y_pos, text, self.COLOR_WHITE)
            
    def update(self):
        """Ekranı güncelle - boş metod, her çağrı günceller"""
        pass