import os
import requests
import datetime
from fpdf import FPDF
import numpy as np
import re

# Configuration
class Config:
    NEWS_API_KEY = "96a1389e33864a8189e25e1f70e22661"
    NEWSPAPER_NAME = "EchoNomix"
    COMPANY_NAME = "!FUN STUDIOS"
    OUTPUT_DIR = "output"

# Create output directory
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

class FinancialNewsAgent:
    def __init__(self):
        self.news_api_key = Config.NEWS_API_KEY
        self.articles = []
        
    def fetch_news(self):
        """Fetch financial news from NewsAPI"""
        print("📰 Fetching latest financial news...")
        
        # NewsAPI endpoint
        url = "https://newsapi.org/v2/top-headlines"
        
        # Parameters for financial news
        params = {
            'category': 'business',
            'language': 'en',
            'pageSize': 15,
            'apiKey': self.news_api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok' and data['totalResults'] > 0:
                articles = []
                for article in data['articles']:
                    articles.append({
                        'title': self.clean_text(article['title'] or 'No title available'),
                        'description': self.clean_text(article['description'] or 'No description available'),
                        'source': self.clean_text(article['source']['name']),
                        'url': article['url'],
                        'published_at': article['publishedAt'],
                        'content': self.clean_text(article['content'] or 'No content available')
                    })
                self.articles = articles
                print(f"✅ Successfully fetched {len(articles)} articles")
                return articles
            else:
                print("⚠️ No articles found, using sample data")
                return self.get_sample_data()
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching news: {e}")
            print("⚠️ Using sample data for demonstration")
            return self.get_sample_data()
    
    def clean_text(self, text):
        """Clean text by removing or replacing problematic characters"""
        if not text:
            return ""
        
        # Replace common problematic characters
        replacements = {
            '…': '...',
            '–': '-',
            '—': '-',
            '‘': "'",
            '…': "'",
            '“': '"',
            '”': '"',
            '•': '*',
            '®': '(R)',
            '©': '(C)',
            '™': '(TM)'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Remove any other non-ASCII characters
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        return text
    
    def get_sample_data(self):
        """Return sample data if API fails"""
        sample_articles = [
            {
                'title': 'Federal Reserve Holds Interest Rates Steady',
                'description': 'The Federal Reserve announced it will maintain current interest rates while monitoring inflation trends.',
                'source': 'Financial Times',
                'published_at': datetime.datetime.now().isoformat(),
            },
            {
                'title': 'Stock Markets Rally on Positive Economic Data',
                'description': 'Global markets showed strong gains following better-than-expected employment reports.',
                'source': 'Bloomberg',
                'published_at': datetime.datetime.now().isoformat(),
            },
            {
                'title': 'Tech Stocks Lead Market Recovery',
                'description': 'Technology companies show robust earnings, driving market optimism.',
                'source': 'CNBC',
                'published_at': datetime.datetime.now().isoformat(),
            }
        ]
        
        # Clean sample data too
        for article in sample_articles:
            article['title'] = self.clean_text(article['title'])
            article['description'] = self.clean_text(article['description'])
            article['source'] = self.clean_text(article['source'])
        
        return sample_articles
    
    def analyze_sentiment(self, text):
        """Basic sentiment analysis"""
        if not text:
            return 'Neutral'
            
        text_lower = text.lower()
        
        bullish_words = ['rise', 'gain', 'growth', 'positive', 'bullish', 'profit', 
                        'increase', 'rally', 'strong', 'optimistic', 'recovery', 'up']
        bearish_words = ['fall', 'drop', 'decline', 'negative', 'bearish', 'loss',
                        'decrease', 'crash', 'weak', 'pessimistic', 'recession', 'down']
        
        bullish_count = sum(1 for word in bullish_words if word in text_lower)
        bearish_count = sum(1 for word in bearish_words if word in text_lower)
        
        if bullish_count > bearish_count:
            return 'Bullish'
        elif bearish_count > bullish_count:
            return 'Bearish'
        else:
            return 'Neutral'
    
    def generate_market_summary(self):
        """Generate simulated market data"""
        trends = ['↑', '↓', '→']
        return {
            'dow_jones': f"{np.random.choice(trends)} {np.random.uniform(0.5, 3.0):.2f}%",
            'nasdaq': f"{np.random.choice(trends)} {np.random.uniform(0.5, 4.0):.2f}%",
            's_p_500': f"{np.random.choice(trends)} {np.random.uniform(0.5, 2.5):.2f}%",
            'oil': f"{np.random.choice(trends)} {np.random.uniform(0.1, 2.0):.2f}%",
            'gold': f"{np.random.choice(trends)} {np.random.uniform(0.1, 1.5):.2f}%",
            'usd': f"{np.random.choice(trends)} {np.random.uniform(0.1, 1.2):.2f}%"
        }
    
    def create_newspaper_pdf(self, filename=None):
        """Create PDF newspaper with proper Unicode handling"""
        if filename is None:
            filename = f"{Config.OUTPUT_DIR}/financial_times_daily.pdf"
        
        print("📄 Creating newspaper PDF...")
        
        pdf = FPDF()
        pdf.add_page()
        
        # Add a Unicode-compatible font
        try:
            # Try to use Arial Unicode if available
            pdf.add_font('Arial', '', 'c:/windows/fonts/arial.ttf', uni=True)
            pdf.add_font('Arial', 'B', 'c:/windows/fonts/arialbd.ttf', uni=True)
            pdf.add_font('Arial', 'I', 'c:/windows/fonts/ariali.ttf', uni=True)
            font_name = 'Arial'
        except:
            # Fallback to built-in font
            font_name = 'Helvetica'
            print("⚠️ Using built-in font (limited Unicode support)")
        
        # Header
        pdf.set_font(font_name, 'B', 24)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 15, Config.NEWSPAPER_NAME, new_x="LMARGIN", new_y="NEXT", align='C')
        
        pdf.set_font(font_name, 'I', 12)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 8, f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}", new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(5)
        
        # Market Summary
        market_data = self.generate_market_summary()
        pdf.set_font(font_name, 'B', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "MARKET SNAPSHOT", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font(font_name, '', 10)
        market_text = f"DOW: {market_data['dow_jones']} | NASDAQ: {market_data['nasdaq']} | S&P 500: {market_data['s_p_500']}"
        pdf.multi_cell(0, 6, market_text)
        pdf.ln(2)
        
        # Articles
        pdf.set_font(font_name, 'B', 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 12, "TOP FINANCIAL NEWS", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        
        for i, article in enumerate(self.articles):
            sentiment = self.analyze_sentiment(article['title'] + ' ' + article['description'])
            
            # Article header
            pdf.set_font(font_name, 'B', 12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 8, f"{i+1}. {article['title']}")
            
            # Source and sentiment
            pdf.set_font(font_name, 'I', 10)
            
            if sentiment == 'Bullish':
                pdf.set_text_color(0, 128, 0)  # Green
            elif sentiment == 'Bearish':
                pdf.set_text_color(255, 0, 0)   # Red
            else:
                pdf.set_text_color(100, 100, 100)  # Gray
                
            source_text = f"Source: {article['source']} | Sentiment: {sentiment}"
            pdf.cell(0, 6, source_text, new_x="LMARGIN", new_y="NEXT")
            
            # Article content
            pdf.set_font(font_name, '', 10)
            pdf.set_text_color(0, 0, 0)
            
            # Split long descriptions into manageable chunks
            description = article['description']
            if len(description) > 200:
                description = description[:197] + "..."
                
            pdf.multi_cell(0, 6, description)
            pdf.ln(3)
            
            if i < len(self.articles) - 1:
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(3)
        
        # Footer
        pdf.ln(10)
        pdf.set_font(font_name, 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 5, f"Generated by {Config.COMPANY_NAME} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT", align='C')
        
        pdf.output(filename)
        print(f"✅ Newspaper saved as: {filename}")
        return filename
    
    def create_html_newspaper(self, filename=None):
        """Create HTML version as backup"""
        if filename is None:
            filename = f"{Config.OUTPUT_DIR}/financial_times_daily.html"
        
        print("🌐 Creating HTML version...")
        
        market_data = self.generate_market_summary()
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{Config.NEWSPAPER_NAME}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f9f9f9;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 3px double #003366;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .headline {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #003366;
                }}
                .market-snapshot {{
                    background: #e8f4f8;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .article {{
                    background: white;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .article.bullish {{ border-left: 4px solid #4caf50; }}
                .article.bearish {{ border-left: 4px solid #f44336; }}
                .article.neutral {{ border-left: 4px solid #9e9e9e; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="headline">{Config.NEWSPAPER_NAME}</div>
                <div class="date">{current_date}</div>
            </div>
            
            <div class="market-snapshot">
                <h3>📊 Market Snapshot</h3>
                <p><strong>DOW:</strong> {market_data['dow_jones']} | 
                   <strong>NASDAQ:</strong> {market_data['nasdaq']} | 
                   <strong>S&P 500:</strong> {market_data['s_p_500']}</p>
            </div>
            
            <h2>📰 Top Financial News</h2>
        """
        
        for i, article in enumerate(self.articles):
            sentiment = self.analyze_sentiment(article['title'] + ' ' + article['description']).lower()
            
            html_content += f"""
            <div class="article {sentiment}">
                <h3>{i+1}. {article['title']}</h3>
                <p><em>Source: {article['source']} | Sentiment: <span class="sentiment">{sentiment.upper()}</span></em></p>
                <p>{article['description']}</p>
            </div>
            """
        
        html_content += """
            <footer style="text-align: center; margin-top: 30px; color: #666;">
                Generated by !FUN STUDIOS
            </footer>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML newspaper saved as: {filename}")
        return filename

def main():
    print("🚀 Starting Financial News AI Agent...")
    print("=" * 50)
    
    agent = FinancialNewsAgent()
    articles = agent.fetch_news()
    
    if articles:
        try:
            pdf_file = agent.create_newspaper_pdf()
            print(f"✅ PDF created: {pdf_file}")
        except Exception as e:
            print(f"❌ PDF creation failed: {e}")
            print("🔄 Falling back to HTML...")
            pdf_file = None
        
        # Always create HTML version
        html_file = agent.create_html_newspaper()
        
        print("=" * 50)
        print("🎉 Generation Complete!")
        if pdf_file:
            print(f"📄 PDF Newspaper: {pdf_file}")
        print(f"🌐 HTML Version: {html_file}")
        print(f"📊 Articles Processed: {len(articles)}")
        print("=" * 50)
        
        # Show sample articles
        print("\n📋 Sample Articles:")
        for i, article in enumerate(articles[:3]):
            print(f"{i+1}. {article['title'][:60]}... ({article['source']})")
    else:
        print("❌ Failed to fetch articles")

if __name__ == "__main__":
    main()