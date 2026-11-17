import os
import hashlib
from pathlib import Path
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

try:
    from android.permissions import request_permissions, Permission  # type: ignore
    IS_ANDROID = True
except ImportError:
    IS_ANDROID = False

KEYWORDS = [
    "minecraft", "cheat", "client", "mod", "wurst", "meteor", "matrix", 
    "killaura", "aimbot", "toolbox", "gameguardian", "gg", "hack", "menu",
    "horion", "prax", "lumine", "strike", "zephyr", "solstice", "aetheris", 
    "wexor", "injector", "xposed", "lsposed", "bypass"
]

EXCEPTIONS = ["oderso"]
EXTENSIONS = {".apk", ".zip", ".rar", ".txt", ".json", ".pak"}

class IronMineScannerApp(App):
    def build(self):
        if IS_ANDROID:
            try:
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE, 
                    Permission.WRITE_EXTERNAL_STORAGE
                ])
            except Exception:
                pass

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        self.label = Label(
            text="IronMine Security Scanner\n\nНажмите кнопку для запуска проверки",
            halign='center',
            font_size='16sp'
        )
        
        btn = Button(
            text="Запустить сканирование",
            size_hint=(1, 0.25),
            background_color=(0.1, 0.5, 0.8, 1)
        )
        btn.bind(on_press=self.start_scan)
        
        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def start_scan(self, instance):
        self.label.text = "Выполняется сканирование..."
        try:
            paths = [
                Path("/sdcard/Download"),
                Path("/sdcard/Downloads"),
                Path("/sdcard/games/com.mojang")
            ]
            found = set()
            for base_path in paths:
                if base_path.exists():
                    for root, dirs, files in os.walk(base_path):
                        root_lower = root.lower()
                        if any(kw in root_lower for kw in ["toolbox", "gameguardian", "cheat", "hack", "modmenu"]):
                            if not any(exc in root_lower for exc in EXCEPTIONS):
                                found.add(root)
                        for file in files:
                            p = Path(root) / file
                            name_lower = p.name.lower()
                            if p.suffix.lower() in EXTENSIONS:
                                if any(exc in name_lower for exc in EXCEPTIONS):
                                    continue
                                if any(kw in name_lower for kw in KEYWORDS):
                                    found.add(str(p))

            content = (
                "=== IRONMINE ANDROID SECURITY SCANNER ===\n"
                "Author / Created by: AbsurdEar7658\n"
                "=========================================\n\n"
                "=== FOUND FILES & DIRECTORIES ===\n" + ("\n".join(found) if found else "Ничего не найдено.") + "\n"
            )
            
            file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            
            save_dir = Path("/sdcard/Download")
            if not save_dir.exists():
                save_dir = Path(".")
                
            save_path = save_dir / "scan_results_android.txt"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(content)
                f.write(f"\n--- INTEGRITY HASH: {file_hash} ---")
            
            self.label.text = "Готово!\n\nОтчет сохранен в папку\n'Загрузки' (Download) как\nscan_results_android.txt"
        except Exception as e:
            self.label.text = f"Ошибка: {str(e)}"

if __name__ == '__main__':
    IronMineScannerApp().run()
