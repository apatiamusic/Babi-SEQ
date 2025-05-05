from machine import Pin, SPI
import time
import config
from lib.ili9341 import Display, color565
from lib.xglcd_font import XglcdFont

class DisplayTester:
    def __init__(self):
        self.spi = SPI(0, baudrate=40000000, sck=Pin(config.tftSck), mosi=Pin(config.tftMosi))
        self.display = Display(self.spi,
                             dc=Pin(config.tftDc),
                             cs=Pin(config.tftCs),
                             rst=Pin(config.tftRst),
                             rotation=90)
        
        # Fontları yükle
        try:
            self.unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
            print("Unispace font yüklendi")
        except Exception as e:
            print(f"Unispace font yüklenemedi: {e}")
            self.unispace = None
        
        self.current_test = 0
        self.test_options = [
            self.test_borders,
            self.test_colors,
            self.test_text,
            self.test_fonts,
            self.test_redraw
        ]
    
    def clear_screen(self):
        """Ekranı siyah yap"""
        self.display.fill_rectangle(0, 0, self.display.width, self.display.height, color565(0, 0, 0))
    
    def show_menu(self):
        """Test menüsünü göster"""
        self.clear_screen()
        if self.unispace:
            self.display.draw_text(10, 10, "DISPLAY TEST MENU", self.unispace, color565(255, 255, 0))
            y_pos = 50
            options = [
                "1. Sınır Testi (E)",
                "2. Renk Testi (H)",
                "3. Metin Testi (A)",
                "4. Font Testi (B)",
                "5. Yenileme Testi (C)"
            ]
            for option in options:
                self.display.draw_text(20, y_pos, option, self.unispace, color565(255, 255, 255))
                y_pos += 30
        else:
            self.display.draw_text8x8(10, 10, "TEST MENU (E/H/A/B/C)", color565(255, 255, 255))
    
    def test_borders(self):
        """Ekran sınırlarını test et"""
        self.clear_screen()
        self.display.draw_rectangle(0, 0, self.display.width-1, self.display.height-1, color565(255, 0, 0))
        self.display.draw_rectangle(10, 10, self.display.width-20, self.display.height-20, color565(0, 255, 0))
        self.display.draw_text8x8(20, 20, "SINIR TESTI", color565(255, 255, 255))
        print("Sınır testi aktif - Menüye dönmek için herhangi bir tuşa basın")
    
    def test_colors(self):
        """Renk testi"""
        self.clear_screen()
        colors = [
            (255, 0, 0, "KIRMIZI"),
            (0, 255, 0, "YESIL"),
            (0, 0, 255, "MAVI"),
            (255, 255, 0, "SARI"),
            (255, 0, 255, "PEMBE")
        ]
        
        block_height = self.display.height // len(colors)
        for i, (r, g, b, name) in enumerate(colors):
            y = i * block_height
            self.display.fill_rectangle(0, y, self.display.width, block_height, color565(r, g, b))
            if self.unispace:
                self.display.draw_text(10, y + 10, name, self.unispace, color565(255, 255, 255))
        
        print("Renk testi aktif - Menüye dönmek için herhangi bir tuşa basın")
    
    def test_text(self):
        """Metin testi"""
        self.clear_screen()
        lorem = [
            "Lorem ipsum dolor sit amet,",
            "consectetur adipiscing elit.",
            "Sed do eiusmod tempor",
            "incididunt ut labore et",
            "dolore magna aliqua."
        ]
        
        y_pos = 20
        for line in lorem:
            if self.unispace:
                self.display.draw_text(10, y_pos, line, self.unispace, color565(255, 255, 255))
                y_pos += 30
            else:
                self.display.draw_text8x8(10, y_pos, line, color565(255, 255, 255))
                y_pos += 10
        
        print("Metin testi aktif - Menüye dönmek için herhangi bir tuşa basın")
    
    def test_fonts(self):
        """Font testi"""
        self.clear_screen()
        if self.unispace:
            self.display.draw_text(10, 10, "Unispace Font Test", self.unispace, color565(0, 255, 255))
            self.display.draw_text(10, 50, "12x24 Piksel", self.unispace, color565(255, 255, 0))
        
        self.display.draw_text8x8(10, 100, "8x8 Sistem Fontu", color565(255, 255, 255))
        print("Font testi aktif - Menüye dönmek için herhangi bir tuşa basın")
    
    def test_redraw(self):
        """Yenileme testi"""
        for i in range(5):
            self.clear_screen()
            msg = f"Yenileme Testi {i+1}/5"
            if self.unispace:
                self.display.draw_text(10, 10, msg, self.unispace, color565(0, 255, 0))
            else:
                self.display.draw_text8x8(10, 10, msg, color565(0, 255, 0))
            time.sleep(0.5)
        
        print("Yenileme testi tamamlandı")
    
    def run(self):
        """Ana test döngüsü"""
        print("\n\n=== TFT Ekran Test Programı ===")
        print("E: Sınır Testi")
        print("H: Renk Testi")
        print("A: Metin Testi")
        print("B: Font Testi")
        print("C: Yenileme Testi")
        print("M: Menüye Dön\n")
        
        self.show_menu()
        
        while True:
            cmd = input("Test seçeneği girin (E/H/A/B/C/M): ").upper()
            
            if cmd == 'E':
                self.test_borders()
            elif cmd == 'H':
                self.test_colors()
            elif cmd == 'A':
                self.test_text()
            elif cmd == 'B':
                self.test_fonts()
            elif cmd == 'C':
                self.test_redraw()
            elif cmd == 'M':
                self.show_menu()
            else:
                print("Geçersiz seçenek!")

# Testi başlat
tester = DisplayTester()
tester.run()