import json
import os
from pathlib import Path

class PortfolioStorage:
    def __init__(self):
        self.storage_dir = Path("portfolios")
        self.storage_dir.mkdir(exist_ok=True)
        
    def save_portfolio(self, slug: str, portfolio_data: dict) -> None:
        """Save portfolio data to a file"""
        file_path = self.storage_dir / f"{slug}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(portfolio_data["html_content"])
            
    def get_portfolio(self, slug: str) -> str:
        """Get portfolio HTML content by slug"""
        file_path = self.storage_dir / f"{slug}.html"
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read() 