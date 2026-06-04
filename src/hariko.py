#    _   _            _ _         
#   | | | |          (_) |        
#   | |_| | __ _ _ __ _| | _____  
#   |  _  |/ _` | '__| | |/ / _ \ 
#   | | | | (_| | |  | |   < (_) |
#   \_| |_/\__,_|_|  |_|_|\_\___/ 
#
# Author: Saka1r
# License: MIT
# Description: Hariko — локальный пайплайн медиа → Whisper → LLM → конспект

# KivyMD
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogButtonContainer,
)
from kivymd.uix.button import MDButton, MDButtonText

# Kivy Core
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.widget import Widget

# Standard Lib
import json
from threading import Thread

# Local Modules
import stt
import tools

Window.size = (500, 700)


class Hariko(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Window & Events 
        Window.bind(on_keyboard=self.events)

        # File Manager
        self.manager_open: bool = False
        self.path: str | None = None  # ← инициализируем до select_path
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

        # Processing Thread
        self.process_thread: Thread | None = None
        self._check_interval = None  # ← для Clock.unschedule()
        self._task_path: str | None = None

        # Dialog State 
        self.dialog: MDDialog | None = None  # ← None, а не False

        # Config Defaults (переопределяются в upload_config)
        self.gguf_path: str = ""
        self.wp_lang: str = "auto"
        self.wp_model: str = "large-v3"
        self.wp_cd: str = "cpu"

    # ─────────────────────────────────────────────────────────
    # File Manager Logic
    def file_manager_open(self) -> None:
        """Открыть файловый менеджер"""
        self.file_manager.show_disks()
        self.manager_open = True

    def select_path(self, path: str) -> None:
        """Обработать выбор пути"""
        self.exit_manager()
        self.path = path

        # Показать путь в сниппете
        MDSnackbar(
            MDSnackbarText(text=path),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        ).open()

    def exit_manager(self, *args) -> None:
        """Закрыть файловый менеджер"""
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers) -> bool:
        """Обработчик системных клавиш (Back / Esc)"""
        if keyboard in (1001, 27):  # 1001 = Android Back, 27 = Esc
            if self.manager_open:
                self.file_manager.back()
        return True

    # ─────────────────────────────────────────────────────────
    # Config
    def config_to_settings(self) -> None:
        """Применить загруженные настройки к виджетам"""
        # Тема
        if self.theme_cls.theme_style == "Light":
            self.root.ids.theme_checkbox_widget.active = True
        else:
            self.root.ids.theme_checkbox_widget.active = False

        # Поля настроек
        self.root.ids.gguf_path_widget.text = self.gguf_path
        self.root.ids.wp_lang_widget.text = self.wp_lang
        self.root.ids.wp_model_widget.text = self.wp_model
        self.root.ids.wp_cd_widget.text = self.wp_cd

    def upload_config(self) -> None:
        """Загрузить настройки из config.json"""
        with open("config/config.json", "r", encoding="utf-8") as f:
            CONFIG = json.load(f)

        self.theme_cls.theme_style = CONFIG["theme"]
        self.gguf_path = CONFIG["gguf_path"]
        self.wp_lang = CONFIG["whisper_lang"]
        self.wp_model = CONFIG["whisper_model"]
        self.wp_cd = CONFIG["whisper_computing_device"]

        self.config_to_settings()

    def update_config(self) -> None:
        """Сохранить текущие настройки из UI в config.json"""
        self.gguf_path = self.root.ids.gguf_path_widget.text
        self.wp_lang = self.root.ids.wp_lang_widget.text
        self.wp_model = self.root.ids.wp_model_widget.text
        self.wp_cd = self.root.ids.wp_cd_widget.text

        CONFIG = {
            "theme": self.theme_cls.theme_style,
            "gguf_path": self.gguf_path,
            "whisper_lang": self.wp_lang,
            "whisper_model": self.wp_model,
            "whisper_computing_device": self.wp_cd,
        }

        with open("config/config.json", "w", encoding="utf-8") as f:
            json.dump(CONFIG, f, indent=4, ensure_ascii=False)

    # ─────────────────────────────────────────────────────────
    #UI & Navigation
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ) -> None:
        """Переключение вкладок навигации"""
        self.root.ids.screen_manager.current = item_text

    def switch_theme(self, active: bool) -> None:
        """Переключатель светлой/тёмной темы"""
        self.theme_cls.theme_style = "Light" if active else "Dark"

    def screen(self, name) -> None:
        self.root.ids.screen_manager.current = name

    def go_to_output(self) -> None:
        out = tools.get_output()
        self.root.ids.output_text_widget.text = out
        self.screen("output")

    # ─────────────────────────────────────────────────────────
    # ⚡ Core Processing Pipeline (Thread-Safe)
    def start_core(self) -> None:
        """Запустить обработку в фоне"""
        # Защита от повторного запуска
        if self.process_thread and self.process_thread.is_alive():
            return

        # Блокируем UI
        self.root.ids.run_widget.disabled = True
        self._task_path = self.path

        # Запуск потока (args — кортеж!)
        self.process_thread = Thread(
            target=stt.stt_run,
            args=(self._task_path,),
            daemon=True,
        )
        self.process_thread.start()

        self._check_interval = Clock.schedule_interval(self.check_thread, 0.1)

    def check_thread(self, dt) -> bool | None:
        """Проверка статуса фонового потока (вызывается из Clock)"""
        if not self.process_thread.is_alive():
            Clock.unschedule(self._check_interval)
            self._check_interval = None

            self.root.ids.run_widget.disabled = False
            self.show_success_dialog()
            return False  # Остановить интервал
        return None

    def show_success_dialog(self) -> None:
        """Показать диалог завершения"""
        if self.dialog:
            self.dialog.dismiss()

        button = MDButton(
            MDButtonText(text="Go"),
            style="text",
        )

        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text="Ready, check output.txt",
                halign="left",
            ),
            MDDialogButtonContainer(
                Widget(),  # spacer
                button,
                spacing="8dp",
            ),
        )

        button.bind(on_release=lambda x: (self.dialog.dismiss(), self.go_to_output()))
        self.dialog.open()

    # ─────────────────────────────────────────────────────────
    #App Lifecycle
    def on_start(self) -> None:
        """Вызывается после build(), когда дерево виджетов готово"""
        self.upload_config()
        self.show_success_dialog()

    def build(self) -> Widget:
        """Инициализация приложения"""
        self.icon = "config/anime.png"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("hariko.kv")


# ─────────────────────────────────────────────────────────────
# 🏁 Entry Point
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    Hariko().run()