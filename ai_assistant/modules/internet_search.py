import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QLineEdit, QTextEdit, QComboBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor
import json
import os
from datetime import datetime

class SearchWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, query, search_type):
        super().__init__()
        self.query = query
        self.search_type = search_type

    def run(self):
        try:
            if self.search_type == "DuckDuckGo":
                results = self.search_duckduckgo()
            elif self.search_type == "Wikipedia":
                results = self.search_wikipedia()
            else:
                results = self.search_custom()
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

    def search_duckduckgo(self):
        # Using DuckDuckGo's HTML
        url = f"https://html.duckduckgo.com/html/?q={self.query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for result in soup.find_all('div', class_='result'):
            title = result.find('a', class_='result__a')
            snippet = result.find('a', class_='result__snippet')
            if title and snippet:
                results.append({
                    'title': title.text.strip(),
                    'url': title['href'],
                    'snippet': snippet.text.strip()
                })
        return results[:5]  # Return top 5 results

    def search_wikipedia(self):
        url = f"https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": self.query,
            "utf8": 1
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        results = []
        for item in data['query']['search']:
            results.append({
                'title': item['title'],
                'url': f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                'snippet': BeautifulSoup(item['snippet'], 'html.parser').get_text()
            })
        return results[:5]

    def search_custom(self):
        # Add your custom search implementation here
        return []

class InternetSearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.search_history = []
        self.load_history()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Search type selection
        search_type_layout = QHBoxLayout()
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems(["DuckDuckGo", "Wikipedia"])
        search_type_layout.addWidget(QLabel("Search Engine:"))
        search_type_layout.addWidget(self.search_type_combo)
        layout.addLayout(search_type_layout)

        # Search input
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter your search query...")
        self.search_input.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)

        # Search history
        layout.addWidget(QLabel("Search History:"))
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setMaximumHeight(100)
        layout.addWidget(self.history_display)
        self.update_history_display()

    def perform_search(self):
        query = self.search_input.text().strip()
        if not query:
            return

        self.search_button.setEnabled(False)
        self.results_display.clear()
        self.results_display.append(f"Searching for: {query}\n")

        # Add to history
        self.add_to_history(query)

        # Create and start search worker
        self.search_worker = SearchWorker(query, self.search_type_combo.currentText())
        self.search_worker.finished.connect(self.handle_results)
        self.search_worker.error.connect(self.handle_error)
        self.search_worker.start()

    def handle_results(self, results):
        self.results_display.clear()
        if not results:
            self.results_display.append("No results found.")
            return

        for result in results:
            self.results_display.append(f"Title: {result['title']}")
            self.results_display.append(f"URL: {result['url']}")
            self.results_display.append(f"Summary: {result['snippet']}")
            self.results_display.append("\n" + "-"*50 + "\n")

        self.search_button.setEnabled(True)

    def handle_error(self, error_message):
        self.results_display.append(f"\nError: {error_message}")
        self.search_button.setEnabled(True)

    def add_to_history(self, query):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.search_history.append({
            'query': query,
            'timestamp': timestamp,
            'engine': self.search_type_combo.currentText()
        })
        self.save_history()
        self.update_history_display()

    def update_history_display(self):
        self.history_display.clear()
        for item in reversed(self.search_history[-5:]):  # Show last 5 searches
            self.history_display.append(
                f"[{item['timestamp']}] {item['engine']}: {item['query']}"
            )

    def save_history(self):
        history_file = os.path.join(os.path.expanduser("~"), "search_history.json")
        with open(history_file, 'w') as f:
            json.dump(self.search_history[-100:], f)  # Keep last 100 searches

    def load_history(self):
        history_file = os.path.join(os.path.expanduser("~"), "search_history.json")
        try:
            with open(history_file, 'r') as f:
                self.search_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.search_history = []

    def closeEvent(self, event):
        self.save_history()
        super().closeEvent(event)
