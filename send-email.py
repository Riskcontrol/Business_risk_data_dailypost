# import os
# import random
# import time
# import asyncio
# import pandas as pd
# import re
# from datetime import datetime
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from groq import AsyncGroq

# # ================================
# # 🔹 1. Initialize API & Web Scraper
# # ================================

# # Initialize Groq API Client
# client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])

# # User-Agent Rotation
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# ]

# # News Sources for Business Data
# BUSINESS_NEWS_URLS = [
#     "https://www.dailypost.ng",
#     "https://dailypost.ng/category/business/",
#     "https://dailypost.ng/category/economy/",
#     "https://punchng.com/topics/business/",
#     "https://www.vanguardngr.com/category/business/",
#     "https://www.premiumtimesng.com/business/"
# ]

# # ================================
# # 🔹 2. Business Risk Framework
# # ================================

# # Risk Factors and their indicators based on your SOP
# BUSINESS_RISK_FACTORS = {
#     "Economic": ["GDP", "Unemployment Rate", "Inflation rate"],
#     "Political": ["Government stability", "Corruption", "Rule of law"],
#     "Technology": ["Digital Infrastructure", "Cybersecurity", "Technology Adoption"],
#     "Social": ["Poverty Rate", "Social unrest", "Education"],
#     "Environmental": ["Air and water quality", "Natural disaster", "Climate change probability"],
#     "Operational": ["Infrastructure Quality", "Supply chain disruption", "Business Continuity"],
#     "Healthcare": ["Healthcare Access", "Disease prevalence", "Healthcare Infrastructure"],
#     "Regulatory and Legal": ["Burden Of Compliance", "Legal Framework", "Enforcement"]
# }

# # Industry Types and Subtypes
# INDUSTRY_MAPPING = {
#     "Manufacturing": ["Factory", "Warehouse", "Supermarket"],
#     "Healthcare": ["Hospitals", "Pharmaceutical"],
#     "Finance & Banking": ["Banks", "Insurance", "Mortgage", "Microfinance"],
#     "Oil & Gas": ["Upstream", "Downstream"],
#     "Education": ["Primary", "Secondary", "Tertiary"],
#     "Logistics & Transportation": ["Logistics", "Transportation (Land)", "Aviation (Air)", "Maritime (Sea)"],
#     "Travel & Hospitality": ["Hotel", "Nightclub", "Bar", "Restaurant"],
#     "Agro-allied": ["Farm", "Storage", "Livestock"],
#     "Telecommunications": ["Telcomm", "Cloud", "Network"],
#     "Mining": ["Mining", "Processing"],
#     "Real Estate & Construction": ["Construction", "Real estate"]
# }

# # Industry Risk Types
# INDUSTRY_RISK_TYPES = {
#     "Manufacturing": ["Supply Chain Disruption", "Forex/Import Policy", "Labour Unrest", "Insecurity", "Energy Costs"],
#     "Healthcare": ["Drug Supply Shortages", "Regulatory Changes", "Security Risks (Kidnapping/Attacks)", "Workforce Shortage", "Counterfeiting"],
#     "Finance & Banking": ["Cybersecurity Threats", "Regulatory Policy Shifts", "Economic Instability", "Naira Volatility", "Fraud Trends"],
#     "Oil & Gas": ["Pipeline Vandalism", "Community Unrest", "Regulatory Compliance", "Environmental Incidents", "Militant Activity"],
#     "Education": ["Student Protests", "Terrorism/Insecurity", "Infrastructure Vandalism", "Regulatory Shifts", "Tuition Policy Changes"],
#     "Logistics & Transportation": ["Road Infrastructure Quality", "Port Congestion", "Fuel Price Volatility", "Cargo Theft/Banditry", "Regulatory Permits", "Insecurity"],
#     "Travel & Hospitality": ["Insecurity (Kidnapping/Terrorism)", "Health Epidemics", "Currency Volatility", "Regulatory Shifts (Tourism Policies)", "Labour Strikes"],
#     "Agro-allied": ["Climate Risks", "Banditry & Herdsmen Attacks", "Market Price Volatility", "Supply Chain Blockages", "Land Use Policy", "Input Costs"],
#     "Telecommunications": ["Vandalism of Infrastructure", "Regulatory Compliance (NCC)", "Cybersecurity Threats", "Power Supply Disruption", "Taxation Changes"],
#     "Mining": ["Community Unrest", "Illegal Mining Activities", "Environmental Regulations", "Insecurity (Banditry/Terrorism)", "Licensing Delays"],
#     "Real Estate & Construction": ["Policy Shifts (Land Use Act)", "Material Cost Volatility", "Regulatory Approvals Delays", "Insecurity (Site Theft/Kidnap)", "Infrastructure Quality"]
# }

# # Business Keywords for filtering
# BUSINESS_KEYWORDS = [
#     # Economic indicators
#     'gdp', 'inflation', 'unemployment', 'economic', 'economy', 'recession', 'growth', 'naira', 'dollar', 'forex',
#     'interest rate', 'monetary policy', 'fiscal policy', 'budget', 'revenue', 'tax', 'taxation',
    
#     # Business operations
#     'business', 'company', 'industry', 'factory', 'manufacturing', 'production', 'supply chain', 'logistics',
#     'import', 'export', 'trade', 'commerce', 'investment', 'investor', 'market', 'price', 'cost',
    
#     # Infrastructure and operations
#     'infrastructure', 'port', 'airport', 'road', 'railway', 'power', 'electricity', 'fuel', 'energy',
#     'telecommunications', 'banking', 'finance', 'insurance', 'loan', 'credit',
    
#     # Risk-related terms
#     'strike', 'protest', 'unrest', 'violence', 'attack', 'kidnap', 'terrorism', 'bandit', 'herdsmen',
#     'vandalism', 'theft', 'fraud', 'corruption', 'policy', 'regulation', 'compliance', 'enforcement',
#     'shutdown', 'closure', 'disruption', 'delay', 'shortage', 'scarcity',
    
#     # Industry-specific
#     'oil', 'gas', 'petroleum', 'pipeline', 'refinery', 'crude', 'nnpc', 'upstream', 'downstream',
#     'agriculture', 'farming', 'crop', 'livestock', 'food', 'harvest',
#     'mining', 'solid minerals', 'gold', 'coal', 'tin', 'iron ore',
#     'healthcare', 'hospital', 'medical', 'drug', 'pharmaceutical', 'medicine',
#     'education', 'school', 'university', 'student', 'teacher', 'academic',
#     'construction', 'building', 'real estate', 'property', 'housing', 'land'
# ]

# # ================================
# # 🔹 3. Load Neighbourhood Data
# # ================================

# def load_neighborhoods_data(filepath="state_neighbourhoods.csv"):
#     """Load neighborhood data for location mapping."""
#     NIGERIAN_STATES_COORDS = {
#         'Abia': {'lat': 5.4301, 'lon': 7.5248},
#         'Adamawa': {'lat': 9.3328, 'lon': 12.3954},
#         'Akwa Ibom': {'lat': 5.0072, 'lon': 7.9306},
#         'Anambra': {'lat': 6.2209, 'lon': 7.0388},
#         'Bauchi': {'lat': 10.3158, 'lon': 9.8474},
#         'Bayelsa': {'lat': 4.7719, 'lon': 6.0699},
#         'Benue': {'lat': 7.3369, 'lon': 8.7404},
#         'Borno': {'lat': 11.8846, 'lon': 13.1520},
#         'Cross River': {'lat': 5.8702, 'lon': 8.6089},
#         'Delta': {'lat': 5.5322, 'lon': 5.8983},
#         'Ebonyi': {'lat': 6.2649, 'lon': 8.0137},
#         'Edo': {'lat': 6.3350, 'lon': 5.6038},
#         'Ekiti': {'lat': 7.7190, 'lon': 5.3110},
#         'Enugu': {'lat': 6.4584, 'lon': 7.5463},
#         'Federal Capital Territory': {'lat': 9.0764, 'lon': 7.3986},
#         'FCT': {'lat': 9.0764, 'lon': 7.3986},
#         'Abuja': {'lat': 9.0764, 'lon': 7.3986},
#         'Gombe': {'lat': 10.2896, 'lon': 11.1698},
#         'Imo': {'lat': 5.4833, 'lon': 7.0333},
#         'Jigawa': {'lat': 12.2280, 'lon': 9.5615},
#         'Kaduna': {'lat': 10.5166, 'lon': 7.4166},
#         'Kano': {'lat': 11.9964, 'lon': 8.5167},
#         'Katsina': {'lat': 12.9855, 'lon': 7.6184},
#         'Kebbi': {'lat': 12.4539, 'lon': 4.1975},
#         'Kogi': {'lat': 7.8012, 'lon': 6.7374},
#         'Kwara': {'lat': 9.5917, 'lon': 4.5481},
#         'Lagos': {'lat': 6.5244, 'lon': 3.3792},
#         'Nasarawa': {'lat': 8.5399, 'lon': 8.2980},
#         'Nassarawa': {'lat': 8.5399, 'lon': 8.2980},
#         'Niger': {'lat': 9.9309, 'lon': 5.5982},
#         'Ogun': {'lat': 7.1600, 'lon': 3.3500},
#         'Ondo': {'lat': 7.2500, 'lon': 5.2000},
#         'Osun': {'lat': 7.7583, 'lon': 4.5641},
#         'Oyo': {'lat': 7.8500, 'lon': 3.9300},
#         'Plateau': {'lat': 9.2182, 'lon': 9.5179},
#         'Rivers': {'lat': 4.7500, 'lon': 7.0000},
#         'Sokoto': {'lat': 13.0654, 'lon': 5.2379},
#         'Taraba': {'lat': 7.9994, 'lon': 10.7744},
#         'Yobe': {'lat': 12.2939, 'lon': 11.4390},
#         'Zamfara': {'lat': 12.1222, 'lon': 6.2236}
#     }
    
#     try:
#         if not os.path.exists(filepath):
#             print(f"Neighborhood file {filepath} not found. Using default coordinates.")
#             return {
#                 "by_state": {state: [{"name": state, "latitude": coords["lat"], "longitude": coords["lon"]}] 
#                            for state, coords in NIGERIAN_STATES_COORDS.items()},
#                 "all_neighborhoods": [],
#                 "neighborhood_names": set()
#             }
        
#         df = pd.read_csv(filepath)
#         print(f"Loaded {len(df)} neighborhoods from {filepath}")
        
#         neighborhoods_by_state = {}
#         all_neighborhoods = []
#         neighborhood_names = set()
        
#         for _, row in df.iterrows():
#             state = row['state']
#             neighborhood = row['neighbourhood_name']
            
#             try:
#                 lat = float(row['latitude'])
#                 lon = float(row['longitude'])
                
#                 if state not in neighborhoods_by_state:
#                     neighborhoods_by_state[state] = []
                
#                 neighborhoods_by_state[state].append({
#                     "name": neighborhood,
#                     "latitude": lat,
#                     "longitude": lon
#                 })
                
#                 all_neighborhoods.append({
#                     "name": neighborhood,
#                     "state": state,
#                     "latitude": lat,
#                     "longitude": lon
#                 })
                
#                 neighborhood_names.add(neighborhood.lower())
                
#             except (ValueError, TypeError):
#                 continue
        
#         for state, coords in NIGERIAN_STATES_COORDS.items():
#             if state not in neighborhoods_by_state:
#                 neighborhoods_by_state[state] = [{
#                     "name": state,
#                     "latitude": coords["lat"],
#                     "longitude": coords["lon"]
#                 }]
        
#         return {
#             "by_state": neighborhoods_by_state,
#             "all_neighborhoods": all_neighborhoods,
#             "neighborhood_names": neighborhood_names
#         }
        
#     except Exception as e:
#         print(f"Error loading neighborhood data: {e}")
#         return {
#             "by_state": {state: [{"name": state, "latitude": coords["lat"], "longitude": coords["lon"]}] 
#                        for state, coords in NIGERIAN_STATES_COORDS.items()},
#             "all_neighborhoods": [],
#             "neighborhood_names": set()
#         }

# # ================================
# # 🔹 4. WebDriver Setup
# # ================================

# def init_driver():
#     """Initialize and return a WebDriver."""
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-notifications")
#     options.add_argument("--window-size=1920,1080")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     return driver

# # ================================
# # 🔹 5. Web Scraping Functions
# # ================================

# def get_business_article_links(driver):
#     """Extract business-related article links from various news sources."""
#     all_links = []
    
#     for url in BUSINESS_NEWS_URLS:
#         try:
#             print(f"Getting business links from {url}")
#             driver.get(url)
#             WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#             soup = BeautifulSoup(driver.page_source, "html.parser")
            
#             # Get all links from the page with date patterns
#             pattern = re.compile(r"/\d{4}/\d{2}/\d{2}/")
#             for a_tag in soup.find_all("a", href=True):
#                 href = a_tag["href"]
#                 if pattern.search(href):
#                     # Convert relative URLs to absolute
#                     if not href.startswith("http"):
#                         base_domain = re.match(r'https?://[^/]+', url).group(0)
#                         href = base_domain + href
#                     if href not in all_links:
#                         all_links.append(href)
            
#             print(f"Found {len(all_links)} links so far")
#             time.sleep(random.uniform(2, 4))
            
#         except Exception as e:
#             print(f"Error getting links from {url}: {e}")
    
#     print(f"Total unique business links found: {len(all_links)}")
#     return all_links

# def scrape_business_article(driver, url):
#     """Scrape business article content."""
#     try:
#         driver.get(url)
#         WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#         soup = BeautifulSoup(driver.page_source, "html.parser")
        
#         # Extract title and description
#         title = soup.find("title").text.strip() if soup.find("title") else "No title found"
#         meta_desc = soup.find("meta", {"name": "description"})
#         description = meta_desc["content"].strip() if meta_desc and meta_desc.has_attr("content") else "No description found"
        
#         # Extract article content based on site
#         article_text = ""
        
#         # DailyPost
#         if "dailypost.ng" in url:
#             content_container = soup.find("div", id="mvp-content-main")
#             if content_container:
#                 paragraphs = content_container.find_all("p")
#                 article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         # Punch
#         elif "punchng.com" in url:
#             content_container = soup.find("div", class_="post-content")
#             if content_container:
#                 paragraphs = content_container.find_all("p")
#                 article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         # Vanguard
#         elif "vanguardngr.com" in url:
#             content_container = soup.find("div", class_="entry-content")
#             if content_container:
#                 paragraphs = content_container.find_all("p")
#                 article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         # Premium Times
#         elif "premiumtimesng.com" in url:
#             content_container = soup.find("div", class_="content")
#             if content_container:
#                 paragraphs = content_container.find_all("p")
#                 article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         # Generic extraction
#         if not article_text:
#             paragraphs = soup.find_all("p")
#             article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         return {
#             "Title": title,
#             "Description": description,
#             "Content": article_text,
#             "Link": url
#         }
        
#     except Exception as e:
#         print(f"Error scraping business article {url}: {e}")
#         return None

# def is_business_relevant(article):
#     """Check if article is relevant to business risks."""
#     content = (article["Title"] + " " + article["Description"] + " " + article["Content"]).lower()
    
#     # Check for business keywords
#     keyword_count = sum(1 for keyword in BUSINESS_KEYWORDS if keyword in content)
    
#     # Article is relevant if it contains at least 2 business keywords
#     return keyword_count >= 2

# # ================================
# # 🔹 6. AI Analysis Functions
# # ================================

# BUSINESS_ANALYSIS_PROMPT = """
# You are an expert business risk analyst specializing in Nigerian market conditions. 
# Analyze the following news article and extract business risk information with high precision.

# Extract the following information in JSON format:

# 1. **Industry** (Choose the most relevant):
#    - Manufacturing, Healthcare, Finance & Banking, Oil & Gas, Education, 
#    - Logistics & Transportation, Travel & Hospitality, Agro-allied, 
#    - Telecommunications, Mining, Real Estate & Construction

# 2. **Industry Subtype** (Based on industry selected):
#    Manufacturing: Factory, Warehouse, Supermarket
#    Healthcare: Hospitals, Pharmaceutical
#    Finance & Banking: Banks, Insurance, Mortgage, Microfinance
#    Oil & Gas: Upstream, Downstream
#    Education: Primary, Secondary, Tertiary
#    Logistics & Transportation: Logistics, Transportation (Land), Aviation (Air), Maritime (Sea)
#    Travel & Hospitality: Hotel, Nightclub, Bar, Restaurant
#    Agro-allied: Farm, Storage, Livestock
#    Telecommunications: Telcomm, Cloud, Network
#    Mining: Mining, Processing
#    Real Estate & Construction: Construction, Real estate

# 3. **Business Risk Factor** (Choose most relevant):
#    - Economic, Political, Technology, Social, Environmental, 
#    - Operational, Healthcare, Regulatory and Legal

# 4. **Risk Indicator** (Based on Risk Factor):
#    Economic: GDP, Unemployment Rate, Inflation rate
#    Political: Government stability, Corruption, Rule of law
#    Technology: Digital Infrastructure, Cybersecurity, Technology Adoption
#    Social: Poverty Rate, Social unrest, Education
#    Environmental: Air and water quality, Natural disaster, Climate change probability
#    Operational: Infrastructure Quality, Supply chain disruption, Business Continuity
#    Healthcare: Healthcare Access, Disease prevalence, Healthcare Infrastructure
#    Regulatory and Legal: Burden Of Compliance, Legal Framework, Enforcement

# 5. **Impact Type**: Positive or Negative

# 6. **Impact Level** (1-4):
#    1 = Low: No known threat, unverified report, non-violent protest, minor regulatory update
#    2 = Medium: Notification of strike, major delay, policy change, localized violent threat
#    3 = High: Confirmed major disruption, security incident, policy changes, health/environmental disasters
#    4 = Critical: Shutdowns, attacks, policy crisis with national impact

# 7. **Event Headline** (Max 20 words): Brief, clear headline describing the business risk

# 8. **Industry Risktype** (Choose most relevant for the identified industry):
#    Manufacturing: Supply Chain Disruption, Forex/Import Policy, Labour Unrest, Insecurity, Energy Costs
#    Healthcare: Drug Supply Shortages, Regulatory Changes, Security Risks, Workforce Shortage, Counterfeiting
#    Finance & Banking: Cybersecurity Threats, Regulatory Policy Shifts, Economic Instability, Naira Volatility, Fraud Trends
#    Oil & Gas: Pipeline Vandalism, Community Unrest, Regulatory Compliance, Environmental Incidents, Militant Activity
#    Education: Student Protests, Terrorism/Insecurity, Infrastructure Vandalism, Regulatory Shifts, Tuition Policy Changes
#    Logistics & Transportation: Road Infrastructure Quality, Port Congestion, Fuel Price Volatility, Cargo Theft/Banditry, Regulatory Permits, Insecurity
#    Travel & Hospitality: Insecurity, Health Epidemics, Currency Volatility, Regulatory Shifts, Labour Strikes
#    Agro-allied: Climate Risks, Banditry & Herdsmen Attacks, Market Price Volatility, Supply Chain Blockages, Land Use Policy, Input Costs
#    Telecommunications: Vandalism of Infrastructure, Regulatory Compliance, Cybersecurity Threats, Power Supply Disruption, Taxation Changes
#    Mining: Community Unrest, Illegal Mining Activities, Environmental Regulations, Insecurity, Licensing Delays
#    Real Estate & Construction: Policy Shifts, Material Cost Volatility, Regulatory Approvals Delays, Insecurity, Infrastructure Quality

# 9. **State**: Nigerian state mentioned in the article
# 10. **City**: Specific city or location mentioned

# IMPORTANT RULES:
# - If Impact Type is Positive, Impact Level must be 1 (Low)
# - Only extract information explicitly mentioned in the article
# - Use null for fields where information is not available
# - Return response in clean JSON format only

# Return your analysis in JSON format without explanations.
# """

# async def analyze_business_article(article):
#     """Use AI to analyze business article and extract risk information."""
#     try:
#         response = await client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": BUSINESS_ANALYSIS_PROMPT},
#                 {"role": "user", "content": f"Title: {article['Title']}\n\nDescription: {article['Description']}\n\nContent: {article['Content']}"}
#             ],
#             model="llama3-8b-8192",
#             temperature=0.2,
#             max_tokens=2000
#         )
        
#         extracted_text = response.choices[0].message.content
        
#         # Find JSON content
#         json_match = re.search(r'```(?:json)?(.*?)```', extracted_text, re.DOTALL)
#         if json_match:
#             extracted_text = json_match.group(1).strip()
        
#         # Try to parse JSON
#         try:
#             import json
#             extracted_data = json.loads(extracted_text)
#         except json.JSONDecodeError:
#             json_start = extracted_text.find('{')
#             json_end = extracted_text.rfind('}') + 1
#             if json_start >= 0 and json_end > json_start:
#                 cleaned_json = extracted_text[json_start:json_end]
#                 try:
#                     extracted_data = json.loads(cleaned_json)
#                 except:
#                     print(f"Failed to parse JSON: {extracted_text}")
#                     extracted_data = {}
#             else:
#                 print(f"Could not find JSON object: {extracted_text}")
#                 extracted_data = {}
        
#         return extracted_data
    
#     except Exception as e:
#         print(f"Error analyzing business article: {e}")
#         return {}

# # ================================
# # 🔹 7. Location and Data Processing
# # ================================

# def extract_location_info(article, neighborhoods_data):
#     """Extract state and city information from article."""
#     content = article["Title"] + " " + article["Description"] + " " + article["Content"]
    
#     # Nigerian states
#     nigerian_states = [
#         'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
#         'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
#         'Federal Capital Territory', 'FCT', 'Abuja', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 
#         'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 
#         'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 
#         'Yobe', 'Zamfara'
#     ]
    
#     # Extract state
#     state = "Unknown"
#     for state_name in nigerian_states:
#         if re.search(r'\b' + re.escape(state_name) + r'\b', content, re.IGNORECASE):
#             if state_name.lower() in ["abuja", "fct"]:
#                 state = "Federal Capital Territory"
#             else:
#                 state = state_name
#             break
    
#     # Extract city
#     city = "Unknown"
#     if state != "Unknown" and state in neighborhoods_data["by_state"]:
#         for neighborhood in neighborhoods_data["by_state"][state]:
#             if re.search(r'\b' + re.escape(neighborhood["name"]) + r'\b', content, re.IGNORECASE):
#                 city = neighborhood["name"]
#                 break
        
#         # If no specific city found, use state as city
#         if city == "Unknown":
#             city = state
    
#     return state, city

# def create_business_risk_record(article, analysis, neighborhoods_data):
#     """Create a business risk record in the required format."""
#     # Get current date
#     today = datetime.now()
    
#     # Extract location
#     state, city = extract_location_info(article, neighborhoods_data)
    
#     # Override with AI analysis if available
#     if analysis.get("State"):
#         state = analysis["State"]
#     if analysis.get("City"):
#         city = analysis["City"]
    
#     # Ensure positive impact is always low level
#     impact_type = analysis.get("Impact Type", "Negative")
#     impact_level = analysis.get("Impact Level", 2)
    
#     if impact_type == "Positive" and impact_level != 1:
#         impact_level = 1
    
#     record = {
#         "Day": today.day,
#         "Month": today.strftime("%b"),
#         "Year": today.year,
#         "Date": today.strftime("%d/%m/%Y"),
#         "State": state,
#         "City": city,
#         "Industry": analysis.get("Industry", ""),
#         "Industry Subtype": analysis.get("Industry Subtype", ""),
#         "Business Risk Factor": analysis.get("Business Risk Factor", ""),
#         "Risk Indicator": analysis.get("Risk Indicator", ""),
#         "Impact Type": impact_type,
#         "Impact Level": impact_level,
#         "Event Headline": analysis.get("Event Headline", article["Title"][:100]),
#         "Evidence Source Link": article["Link"],
#         "Analyst Comments": "",
#         "Industry Risktype": analysis.get("Industry Risktype", "")
#     }
    
#     return record

# # ================================
# # 🔹 8. Email Function
# # ================================

# def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
#     """Send email with business risk data attached."""
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         with open(attachment_path, 'rb') as attachment:
#             part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
#         part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#         msg.attach(part)

#         server = smtplib.SMTP_SSL(smtp_server, smtp_port)
#         server.login(sender_email, smtp_password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())
#         server.quit()
        
#         print(f"Email sent successfully to {receiver_email}")
#     except Exception as e:
#         print(f"Error sending email: {e}")

# # ================================
# # 🔹 9. Main Function
# # ================================

# async def main():
#     """Main function to run the business risk scraper."""
#     print("Starting Business Risk Data Scraper...")
    
#     # Load neighborhood data
#     neighborhoods_data = load_neighborhoods_data()
#     print(f"Loaded neighborhood data with {len(neighborhoods_data['all_neighborhoods'])} locations")
    
#     # Initialize WebDriver
#     driver = init_driver()
    
#     try:
#         # Get business article links
#         article_links = get_business_article_links(driver)
#         print(f"Found {len(article_links)} business article links")
        
#         # Scrape articles
#         articles = []
#         for url in article_links:
#             article = scrape_business_article(driver, url)
#             if article and is_business_relevant(article):
#                 articles.append(article)
#                 print(f"Found relevant business article: {article['Title'][:80]}...")
            
#             time.sleep(random.uniform(2, 4))  # Random delay between requests
        
#         print(f"Successfully scraped {len(articles)} relevant business articles")
        
#         if not articles:
#             print("No relevant business articles found. Exiting.")
#             return
        
#         # Analyze articles and create business risk records
#         business_risk_records = []
        
#         for article in articles:
#             try:
#                 # Analyze article with AI
#                 analysis = await analyze_business_article(article)
                
#                 # Create business risk record
#                 if analysis:  # Only create record if analysis was successful
#                     record = create_business_risk_record(article, analysis, neighborhoods_data)
#                     business_risk_records.append(record)
#                     print(f"Created business risk record: {record['Event Headline'][:60]}...")
                
#             except Exception as e:
#                 print(f"Error processing article: {e}")
#                 continue
        
#         print(f"Created {len(business_risk_records)} business risk records")
        
#         # Save data to CSV
#         if business_risk_records:
#             df = pd.DataFrame(business_risk_records)
            
#             # Sort by date (most recent first)
#             df = df.sort_values(['Year', 'Month', 'Day'], ascending=[False, False, False])
            
#             # Save to CSV
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             filename = f'business_risk_data_{timestamp}.csv'
#             df.to_csv(filename, index=False)
#             print(f"Business risk data saved to {filename}")
            
#             # Display summary statistics
#             print("\n📊 Business Risk Data Summary:")
#             print(f"Total Records: {len(df)}")
#             print(f"Industries Covered: {df['Industry'].nunique()}")
#             print(f"States Covered: {df['State'].nunique()}")
#             print(f"Risk Factors: {df['Business Risk Factor'].nunique()}")
            
#             print("\n🏭 Top Industries by Risk Events:")
#             industry_counts = df['Industry'].value_counts().head(5)
#             for industry, count in industry_counts.items():
#                 print(f"  {industry}: {count} events")
            
#             print("\n🌍 Top States by Risk Events:")
#             state_counts = df['State'].value_counts().head(5)
#             for state, count in state_counts.items():
#                 print(f"  {state}: {count} events")
            
#             print("\n⚠️ Risk Factor Distribution:")
#             risk_factor_counts = df['Business Risk Factor'].value_counts()
#             for factor, count in risk_factor_counts.items():
#                 print(f"  {factor}: {count} events")
            
#             print("\n📈 Impact Level Distribution:")
#             impact_counts = df['Impact Level'].value_counts().sort_index()
#             impact_labels = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}
#             for level, count in impact_counts.items():
#                 print(f"  Level {level} ({impact_labels.get(level, 'Unknown')}): {count} events")
            
#             # Send email with the business risk data
#             send_email(
#                 sender_email=os.environ.get('USER_EMAIL'),
#                 receiver_email="riskcontrolservicesnig@gmail.com",
#                 subject="Daily Business Risk Data Update",
#                 body=f"""Daily Business Risk Intelligence Report

# 📊 Summary:
# - Total Risk Events: {len(df)}
# - Industries Monitored: {df['Industry'].nunique()}
# - States Covered: {df['State'].nunique()}
# - High/Critical Events: {len(df[df['Impact Level'] >= 3])}

# 🔍 Top Risk Areas:
# - Primary Industry: {df['Industry'].value_counts().index[0] if len(df) > 0 else 'N/A'}
# - Primary Risk Factor: {df['Business Risk Factor'].value_counts().index[0] if len(df) > 0 else 'N/A'}
# - Most Affected State: {df['State'].value_counts().index[0] if len(df) > 0 else 'N/A'}

# Please find the detailed business risk data attached.

# This report was generated automatically from Nigerian business news sources.
# """,
#                 attachment_path=filename,
#                 smtp_server="smtp.gmail.com",
#                 smtp_port=465,
#                 smtp_password=os.environ.get('USER_PASSWORD')
#             )
            
#             print("✅ Business risk data processing and email sent successfully")
#         else:
#             print("No business risk records created.")
    
#     except Exception as e:
#         print(f"Error in main processing: {e}")
    
#     finally:
#         # Clean up
#         driver.quit()

# # ================================
# # 🔹 10. Additional Utility Functions
# # ================================

# def validate_business_record(record):
#     """Validate business risk record for completeness and accuracy."""
#     required_fields = ['Industry', 'Business Risk Factor', 'Risk Indicator', 'Impact Type', 'Impact Level']
    
#     for field in required_fields:
#         if not record.get(field) or record[field] == "":
#             return False, f"Missing required field: {field}"
    
#     # Validate Impact Type and Level relationship
#     if record['Impact Type'] == 'Positive' and record['Impact Level'] != 1:
#         return False, "Positive impact must have Low (1) impact level"
    
#     # Validate Impact Level range
#     if record['Impact Level'] not in [1, 2, 3, 4]:
#         return False, "Impact Level must be between 1-4"
    
#     # Validate Industry and Industry Subtype relationship
#     industry = record.get('Industry', '')
#     subtype = record.get('Industry Subtype', '')
    
#     if industry in INDUSTRY_MAPPING and subtype:
#         if subtype not in INDUSTRY_MAPPING[industry]:
#             return False, f"Invalid subtype {subtype} for industry {industry}"
    
#     return True, "Valid record"

# def enhance_location_data(record, neighborhoods_data):
#     """Enhance location data with coordinates if available."""
#     state = record.get('State', '')
#     city = record.get('City', '')
    
#     if state in neighborhoods_data["by_state"]:
#         for neighborhood in neighborhoods_data["by_state"][state]:
#             if neighborhood["name"].lower() == city.lower():
#                 record['Latitude'] = neighborhood["latitude"]
#                 record['Longitude'] = neighborhood["longitude"]
#                 break
        
#         # If no exact match, use state coordinates
#         if 'Latitude' not in record and neighborhoods_data["by_state"][state]:
#             record['Latitude'] = neighborhoods_data["by_state"][state][0]["latitude"]
#             record['Longitude'] = neighborhoods_data["by_state"][state][0]["longitude"]
    
#     return record

# def generate_risk_insights(df):
#     """Generate insights from the business risk data."""
#     insights = []
    
#     if len(df) == 0:
#         return ["No data available for analysis"]
    
#     # Critical events insight
#     critical_events = len(df[df['Impact Level'] == 4])
#     if critical_events > 0:
#         insights.append(f"🚨 {critical_events} critical business risk events detected requiring immediate attention")
    
#     # High-risk industry insight
#     top_industry = df['Industry'].value_counts().index[0]
#     top_industry_count = df['Industry'].value_counts().iloc[0]
#     insights.append(f"📊 {top_industry} sector shows highest risk activity with {top_industry_count} events")
    
#     # Geographic concentration
#     top_state = df['State'].value_counts().index[0]
#     top_state_count = df['State'].value_counts().iloc[0]
#     insights.append(f"🌍 {top_state} state has highest concentration of business risks with {top_state_count} events")
    
#     # Risk factor analysis
#     top_risk_factor = df['Business Risk Factor'].value_counts().index[0]
#     top_risk_count = df['Business Risk Factor'].value_counts().iloc[0]
#     insights.append(f"⚠️ {top_risk_factor} risks dominate with {top_risk_count} events")
    
#     # Positive vs Negative impact ratio
#     positive_count = len(df[df['Impact Type'] == 'Positive'])
#     negative_count = len(df[df['Impact Type'] == 'Negative'])
#     ratio = round(negative_count / positive_count, 2) if positive_count > 0 else "∞"
#     insights.append(f"📈 Negative to positive event ratio: {ratio}:1")
    
#     return insights

# # ================================
# # 🔹 11. Script Execution
# # ================================

# if __name__ == "__main__":
#     asyncio.run(main())



# import os
# import random
# import time
# import asyncio
# import pandas as pd
# import re
# from datetime import datetime
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from groq import AsyncGroq
# import google.generativeai as genai
# import json

# # ================================
# # 🔹 1. Initialize APIs & Web Scraper
# # ================================

# # Initialize Groq API Client
# client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])

# # Initialize Gemini API Client
# #GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual Gemini API key
# #genai.configure(api_key=GEMINI_API_KEY)
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# gemini_model = genai.GenerativeModel('gemini-2.0-flash')

# # User-Agent Rotation
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# ]

# # News Sources for Business Data
# BUSINESS_NEWS_URLS = [
#     "https://www.dailypost.ng",
#     "https://dailypost.ng/category/business/",
#     "https://dailypost.ng/category/economy/",
#     "https://punchng.com/topics/business/",
#     "https://www.vanguardngr.com/category/business/",
#     "https://www.premiumtimesng.com/business/"
# ]

# # ================================
# # 🔹 2. Business Risk Framework
# # ================================

# # Risk Factors and their indicators based on your SOP
# BUSINESS_RISK_FACTORS = {
#     "Economic": ["GDP", "Unemployment Rate", "Inflation rate"],
#     "Political": ["Government stability", "Corruption", "Rule of law"],
#     "Technology": ["Digital Infrastructure", "Cybersecurity", "Technology Adoption"],
#     "Social": ["Poverty Rate", "Social unrest", "Education"],
#     "Environmental": ["Air and water quality", "Natural disaster", "Climate change probability"],
#     "Operational": ["Infrastructure Quality", "Supply chain disruption", "Business Continuity"],
#     "Healthcare": ["Healthcare Access", "Disease prevalence", "Healthcare Infrastructure"],
#     "Regulatory and Legal": ["Burden Of Compliance", "Legal Framework", "Enforcement"]
# }

# # Industry Types and Subtypes
# INDUSTRY_MAPPING = {
#     "Manufacturing": ["Factory", "Warehouse", "Supermarket"],
#     "Healthcare": ["Hospitals", "Pharmaceutical"],
#     "Finance & Banking": ["Banks", "Insurance", "Mortgage", "Microfinance"],
#     "Oil & Gas": ["Upstream", "Downstream"],
#     "Education": ["Primary", "Secondary", "Tertiary"],
#     "Logistics & Transportation": ["Logistics", "Transportation (Land)", "Aviation (Air)", "Maritime (Sea)"],
#     "Travel & Hospitality": ["Hotel", "Nightclub", "Bar", "Restaurant"],
#     "Agro-allied": ["Farm", "Storage", "Livestock"],
#     "Telecommunications": ["Telcomm", "Cloud", "Network"],
#     "Mining": ["Mining", "Processing"],
#     "Real Estate & Construction": ["Construction", "Real estate"]
# }

# # Industry Risk Types
# INDUSTRY_RISK_TYPES = {
#     "Manufacturing": ["Supply Chain Disruption", "Forex/Import Policy", "Labour Unrest", "Insecurity", "Energy Costs"],
#     "Healthcare": ["Drug Supply Shortages", "Regulatory Changes", "Security Risks (Kidnapping/Attacks)", "Workforce Shortage", "Counterfeiting"],
#     "Finance & Banking": ["Cybersecurity Threats", "Regulatory Policy Shifts", "Economic Instability", "Naira Volatility", "Fraud Trends"],
#     "Oil & Gas": ["Pipeline Vandalism", "Community Unrest", "Regulatory Compliance", "Environmental Incidents", "Militant Activity"],
#     "Education": ["Student Protests", "Terrorism/Insecurity", "Infrastructure Vandalism", "Regulatory Shifts", "Tuition Policy Changes"],
#     "Logistics & Transportation": ["Road Infrastructure Quality", "Port Congestion", "Fuel Price Volatility", "Cargo Theft/Banditry", "Regulatory Permits", "Insecurity"],
#     "Travel & Hospitality": ["Insecurity (Kidnapping/Terrorism)", "Health Epidemics", "Currency Volatility", "Regulatory Shifts (Tourism Policies)", "Labour Strikes"],
#     "Agro-allied": ["Climate Risks", "Banditry & Herdsmen Attacks", "Market Price Volatility", "Supply Chain Blockages", "Land Use Policy", "Input Costs"],
#     "Telecommunications": ["Vandalism of Infrastructure", "Regulatory Compliance (NCC)", "Cybersecurity Threats", "Power Supply Disruption", "Taxation Changes"],
#     "Mining": ["Community Unrest", "Illegal Mining Activities", "Environmental Regulations", "Insecurity (Banditry/Terrorism)", "Licensing Delays"],
#     "Real Estate & Construction": ["Policy Shifts (Land Use Act)", "Material Cost Volatility", "Regulatory Approvals Delays", "Insecurity (Site Theft/Kidnap)", "Infrastructure Quality"]
# }

# # Business Keywords for filtering
# BUSINESS_KEYWORDS = [
#     # Economic indicators
#     'gdp', 'inflation', 'unemployment', 'economic', 'economy', 'recession', 'growth', 'naira', 'dollar', 'forex',
#     'interest rate', 'monetary policy', 'fiscal policy', 'budget', 'revenue', 'tax', 'taxation',
    
#     # Business operations
#     'business', 'company', 'industry', 'factory', 'manufacturing', 'production', 'supply chain', 'logistics',
#     'import', 'export', 'trade', 'commerce', 'investment', 'investor', 'market', 'price', 'cost',
    
#     # Infrastructure and operations
#     'infrastructure', 'port', 'airport', 'road', 'railway', 'power', 'electricity', 'fuel', 'energy',
#     'telecommunications', 'banking', 'finance', 'insurance', 'loan', 'credit',
    
#     # Risk-related terms
#     'strike', 'protest', 'unrest', 'violence', 'attack', 'kidnap', 'terrorism', 'bandit', 'herdsmen',
#     'vandalism', 'theft', 'fraud', 'corruption', 'policy', 'regulation', 'compliance', 'enforcement',
#     'shutdown', 'closure', 'disruption', 'delay', 'shortage', 'scarcity',
    
#     # Industry-specific
#     'oil', 'gas', 'petroleum', 'pipeline', 'refinery', 'crude', 'nnpc', 'upstream', 'downstream',
#     'agriculture', 'farming', 'crop', 'livestock', 'food', 'harvest',
#     'mining', 'solid minerals', 'gold', 'coal', 'tin', 'iron ore',
#     'healthcare', 'hospital', 'medical', 'drug', 'pharmaceutical', 'medicine',
#     'education', 'school', 'university', 'student', 'teacher', 'academic',
#     'construction', 'building', 'real estate', 'property', 'housing', 'land'
# ]

# # Nigerian states for validation
# NIGERIAN_STATES = [
#     'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
#     'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
#     'Federal Capital Territory', 'FCT', 'Abuja', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 
#     'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 
#     'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 
#     'Yobe', 'Zamfara'
# ]

# # ================================
# # 🔹 3. Load Neighbourhood Data
# # ================================

# def load_neighborhoods_data(filepath="state_neighbourhoods.csv"):
#     """Load neighborhood data for location mapping."""
#     NIGERIAN_STATES_COORDS = {
#         'Abia': {'lat': 5.4301, 'lon': 7.5248},
#         'Adamawa': {'lat': 9.3328, 'lon': 12.3954},
#         'Akwa Ibom': {'lat': 5.0072, 'lon': 7.9306},
#         'Anambra': {'lat': 6.2209, 'lon': 7.0388},
#         'Bauchi': {'lat': 10.3158, 'lon': 9.8474},
#         'Bayelsa': {'lat': 4.7719, 'lon': 6.0699},
#         'Benue': {'lat': 7.3369, 'lon': 8.7404},
#         'Borno': {'lat': 11.8846, 'lon': 13.1520},
#         'Cross River': {'lat': 5.8702, 'lon': 8.6089},
#         'Delta': {'lat': 5.5322, 'lon': 5.8983},
#         'Ebonyi': {'lat': 6.2649, 'lon': 8.0137},
#         'Edo': {'lat': 6.3350, 'lon': 5.6038},
#         'Ekiti': {'lat': 7.7190, 'lon': 5.3110},
#         'Enugu': {'lat': 6.4584, 'lon': 7.5463},
#         'Federal Capital Territory': {'lat': 9.0764, 'lon': 7.3986},
#         'FCT': {'lat': 9.0764, 'lon': 7.3986},
#         'Abuja': {'lat': 9.0764, 'lon': 7.3986},
#         'Gombe': {'lat': 10.2896, 'lon': 11.1698},
#         'Imo': {'lat': 5.4833, 'lon': 7.0333},
#         'Jigawa': {'lat': 12.2280, 'lon': 9.5615},
#         'Kaduna': {'lat': 10.5166, 'lon': 7.4166},
#         'Kano': {'lat': 11.9964, 'lon': 8.5167},
#         'Katsina': {'lat': 12.9855, 'lon': 7.6184},
#         'Kebbi': {'lat': 12.4539, 'lon': 4.1975},
#         'Kogi': {'lat': 7.8012, 'lon': 6.7374},
#         'Kwara': {'lat': 9.5917, 'lon': 4.5481},
#         'Lagos': {'lat': 6.5244, 'lon': 3.3792},
#         'Nasarawa': {'lat': 8.5399, 'lon': 8.2980},
#         'Niger': {'lat': 9.9309, 'lon': 5.5982},
#         'Ogun': {'lat': 7.1600, 'lon': 3.3500},
#         'Ondo': {'lat': 7.2500, 'lon': 5.2000},
#         'Osun': {'lat': 7.7583, 'lon': 4.5641},
#         'Oyo': {'lat': 7.8500, 'lon': 3.9300},
#         'Plateau': {'lat': 9.2182, 'lon': 9.5179},
#         'Rivers': {'lat': 4.7500, 'lon': 7.0000},
#         'Sokoto': {'lat': 13.0654, 'lon': 5.2379},
#         'Taraba': {'lat': 7.9994, 'lon': 10.7744},
#         'Yobe': {'lat': 12.2939, 'lon': 11.4390},
#         'Zamfara': {'lat': 12.1222, 'lon': 6.2236}
#     }
    
#     try:
#         if not os.path.exists(filepath):
#             print(f"Neighborhood file {filepath} not found. Using default coordinates.")
#             return {
#                 "by_state": {state: [{"name": state, "latitude": coords["lat"], "longitude": coords["lon"]}] 
#                            for state, coords in NIGERIAN_STATES_COORDS.items()},
#                 "all_neighborhoods": [],
#                 "neighborhood_names": set()
#             }
        
#         df = pd.read_csv(filepath)
#         print(f"Loaded {len(df)} neighborhoods from {filepath}")
        
#         neighborhoods_by_state = {}
#         all_neighborhoods = []
#         neighborhood_names = set()
        
#         for _, row in df.iterrows():
#             state = row['state']
#             neighborhood = row['neighbourhood_name']
            
#             try:
#                 lat = float(row['latitude'])
#                 lon = float(row['longitude'])
                
#                 if state not in neighborhoods_by_state:
#                     neighborhoods_by_state[state] = []
                
#                 neighborhoods_by_state[state].append({
#                     "name": neighborhood,
#                     "latitude": lat,
#                     "longitude": lon
#                 })
                
#                 all_neighborhoods.append({
#                     "name": neighborhood,
#                     "state": state,
#                     "latitude": lat,
#                     "longitude": lon
#                 })
                
#                 neighborhood_names.add(neighborhood.lower())
                
#             except (ValueError, TypeError):
#                 continue
        
#         for state, coords in NIGERIAN_STATES_COORDS.items():
#             if state not in neighborhoods_by_state:
#                 neighborhoods_by_state[state] = [{
#                     "name": state,
#                     "latitude": coords["lat"],
#                     "longitude": coords["lon"]
#                 }]
        
#         return {
#             "by_state": neighborhoods_by_state,
#             "all_neighborhoods": all_neighborhoods,
#             "neighborhood_names": neighborhood_names
#         }
        
#     except Exception as e:
#         print(f"Error loading neighborhood data: {e}")
#         return {
#             "by_state": {state: [{"name": state, "latitude": coords["lat"], "longitude": coords["lon"]}] 
#                        for state, coords in NIGERIAN_STATES_COORDS.items()},
#             "all_neighborhoods": [],
#             "neighborhood_names": set()
#         }

# # ================================
# # 🔹 4. WebDriver Setup
# # ================================

# def init_driver():
#     """Initialize and return a WebDriver."""
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-notifications")
#     options.add_argument("--window-size=1920,1080")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     return driver

# # ================================
# # 🔹 5. Web Scraping Functions
# # ================================

# def get_business_article_links(driver):
#     """Extract business-related article links from various news sources."""
#     all_links = []
    
#     for url in BUSINESS_NEWS_URLS:
#         try:
#             print(f"Getting business links from {url}")
#             driver.get(url)
#             WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#             soup = BeautifulSoup(driver.page_source, "html.parser")
            
#             # Get all links from the page with date patterns
#             pattern = re.compile(r"/\d{4}/\d{2}/\d{2}/")
#             for a_tag in soup.find_all("a", href=True):
#                 href = a_tag["href"]
#                 if pattern.search(href):
#                     # Convert relative URLs to absolute
#                     if not href.startswith("http"):
#                         base_domain = re.match(r'https?://[^/]+', url).group(0)
#                         href = base_domain + href
#                     if href not in all_links:
#                         all_links.append(href)
            
#             print(f"Found {len(all_links)} links so far")
#             time.sleep(random.uniform(2, 4))
            
#         except Exception as e:
#             print(f"Error getting links from {url}: {e}")
    
#     print(f"Total unique business links found: {len(all_links)}")
#     return all_links

# def scrape_business_article(driver, url):
#     """Scrape business article content."""
#     try:
#         driver.get(url)
#         WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#         soup = BeautifulSoup(driver.page_source, "html.parser")
        
#         # Extract title and description
#         title = soup.find("title").text.strip() if soup.find("title") else "No title found"
#         meta_desc = soup.find("meta", {"name": "description"})
#         description = meta_desc["content"].strip() if meta_desc and meta_desc.has_attr("content") else "No description found"
        
#         # Extract article content based on site
#         article_text = ""
        
#         # DailyPost
#         if "dailypost.ng" in url:
#             content_container = soup.find("div", id="mvp-content-main")
#             if content_container:
#                 paragraphs = content_container.find_all("p")
#                 article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         # Punch
#         elif "punchng.com" in url:
#             content_container = soup.find("div", class_="post-content")
#             if content_container:
#                 paragraphs = content_container.find_all("p")
#                 article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         # Vanguard
#         elif "vanguardngr.com" in url:
#             content_container = soup.find("div", class_="entry-content")
#             if content_container:
#                 paragraphs = content_container.find_all("p")
#                 article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         # Premium Times
#         elif "premiumtimesng.com" in url:
#             content_container = soup.find("div", class_="content")
#             if content_container:
#                 paragraphs = content_container.find_all("p")
#                 article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         # Generic extraction
#         if not article_text:
#             paragraphs = soup.find_all("p")
#             article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
#         return {
#             "Title": title,
#             "Description": description,
#             "Content": article_text,
#             "Link": url
#         }
        
#     except Exception as e:
#         print(f"Error scraping business article {url}: {e}")
#         return None

# def is_business_relevant(article):
#     """Check if article is relevant to business risks."""
#     content = (article["Title"] + " " + article["Description"] + " " + article["Content"]).lower()
    
#     # Check for business keywords
#     keyword_count = sum(1 for keyword in BUSINESS_KEYWORDS if keyword in content)
    
#     # Article is relevant if it contains at least 2 business keywords
#     return keyword_count >= 2

# # ================================
# # 🔹 6. AI Analysis Functions
# # ================================

# BUSINESS_ANALYSIS_PROMPT = """
# You are an expert business risk analyst specializing in Nigerian market conditions. 
# Analyze the following news article and extract business risk information with high precision.

# Extract the following information in JSON format:

# 1. **Industry** (Choose the most relevant):
#    - Manufacturing, Healthcare, Finance & Banking, Oil & Gas, Education, 
#    - Logistics & Transportation, Travel & Hospitality, Agro-allied, 
#    - Telecommunications, Mining, Real Estate & Construction

# 2. **Industry Subtype** (Based on industry selected):
#    Manufacturing: Factory, Warehouse, Supermarket
#    Healthcare: Hospitals, Pharmaceutical
#    Finance & Banking: Banks, Insurance, Mortgage, Microfinance
#    Oil & Gas: Upstream, Downstream
#    Education: Primary, Secondary, Tertiary
#    Logistics & Transportation: Logistics, Transportation (Land), Aviation (Air), Maritime (Sea)
#    Travel & Hospitality: Hotel, Nightclub, Bar, Restaurant
#    Agro-allied: Farm, Storage, Livestock
#    Telecommunications: Telcomm, Cloud, Network
#    Mining: Mining, Processing
#    Real Estate & Construction: Construction, Real estate

# 3. **Business Risk Factor** (Choose most relevant):
#    - Economic, Political, Technology, Social, Environmental, 
#    - Operational, Healthcare, Regulatory and Legal

# 4. **Risk Indicator** (Based on Risk Factor):
#    Economic: GDP, Unemployment Rate, Inflation rate
#    Political: Government stability, Corruption, Rule of law
#    Technology: Digital Infrastructure, Cybersecurity, Technology Adoption
#    Social: Poverty Rate, Social unrest, Education
#    Environmental: Air and water quality, Natural disaster, Climate change probability
#    Operational: Infrastructure Quality, Supply chain disruption, Business Continuity
#    Healthcare: Healthcare Access, Disease prevalence, Healthcare Infrastructure
#    Regulatory and Legal: Burden Of Compliance, Legal Framework, Enforcement

# 5. **Impact Type**: Positive or Negative

# 6. **Impact Level** (1-4):
#    1 = Low: No known threat, unverified report, non-violent protest, minor regulatory update
#    2 = Medium: Notification of strike, major delay, policy change, localized violent threat
#    3 = High: Confirmed major disruption, security incident, policy changes, health/environmental disasters
#    4 = Critical: Shutdowns, attacks, policy crisis with national impact

# 7. **Event Headline** (Max 20 words): Brief, clear headline describing the business risk

# 8. **Industry Risktype** (Choose most relevant for the identified industry):
#    Manufacturing: Supply Chain Disruption, Forex/Import Policy, Labour Unrest, Insecurity, Energy Costs
#    Healthcare: Drug Supply Shortages, Regulatory Changes, Security Risks, Workforce Shortage, Counterfeiting
#    Finance & Banking: Cybersecurity Threats, Regulatory Policy Shifts, Economic Instability, Naira Volatility, Fraud Trends
#    Oil & Gas: Pipeline Vandalism, Community Unrest, Regulatory Compliance, Environmental Incidents, Militant Activity
#    Education: Student Protests, Terrorism/Insecurity, Infrastructure Vandalism, Regulatory Shifts, Tuition Policy Changes
#    Logistics & Transportation: Road Infrastructure Quality, Port Congestion, Fuel Price Volatility, Cargo Theft/Banditry, Regulatory Permits, Insecurity
#    Travel & Hospitality: Insecurity, Health Epidemics, Currency Volatility, Regulatory Shifts, Labour Strikes
#    Agro-allied: Climate Risks, Banditry & Herdsmen Attacks, Market Price Volatility, Supply Chain Blockages, Land Use Policy, Input Costs
#    Telecommunications: Vandalism of Infrastructure, Regulatory Compliance, Cybersecurity Threats, Power Supply Disruption, Taxation Changes
#    Mining: Community Unrest, Illegal Mining Activities, Environmental Regulations, Insecurity, Licensing Delays
#    Real Estate & Construction: Policy Shifts, Material Cost Volatility, Regulatory Approvals Delays, Insecurity, Infrastructure Quality

# 9. **State**: Nigerian state mentioned in the article
# 10. **City**: Specific city or location mentioned

# IMPORTANT RULES:
# - If Impact Type is Positive, Impact Level must be 1 (Low)
# - Only extract information explicitly mentioned in the article
# - Use null for fields where information is not available
# - Return response in clean JSON format only

# Return your analysis in JSON format without explanations.
# """

# async def analyze_business_article(article):
#     """Use AI to analyze business article and extract risk information."""
#     try:
#         response = await client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": BUSINESS_ANALYSIS_PROMPT},
#                 {"role": "user", "content": f"Title: {article['Title']}\n\nDescription: {article['Description']}\n\nContent: {article['Content']}"}
#             ],
#             model="llama3-8b-8192",
#             temperature=0.2,
#             max_tokens=2000
#         )
        
#         extracted_text = response.choices[0].message.content
        
#         # Find JSON content
#         json_match = re.search(r'```(?:json)?(.*?)```', extracted_text, re.DOTALL)
#         if json_match:
#             extracted_text = json_match.group(1).strip()
        
#         # Try to parse JSON
#         try:
#             extracted_data = json.loads(extracted_text)
#         except json.JSONDecodeError:
#             json_start = extracted_text.find('{')
#             json_end = extracted_text.rfind('}') + 1
#             if json_start >= 0 and json_end > json_start:
#                 cleaned_json = extracted_text[json_start:json_end]
#                 try:
#                     extracted_data = json.loads(cleaned_json)
#                 except:
#                     print(f"Failed to parse JSON: {extracted_text}")
#                     extracted_data = {}
#             else:
#                 print(f"Could not find JSON object: {extracted_text}")
#                 extracted_data = {}
        
#         return extracted_data
    
#     except Exception as e:
#         print(f"Error analyzing business article: {e}")
#         return {}

# # ================================
# # 🔹 7. Gemini Verification Functions
# # ================================

# GEMINI_VERIFICATION_PROMPT = """
# You are a senior quality assurance analyst tasked with verifying the accuracy of business risk data extraction.

# Review the following:

# 1. **Original News Article:**
# Title: {title}
# Content: {content}

# 2. **Extracted Business Risk Data:**
# {extracted_data}

# **Verification Tasks:**

# 1. **Content Intent Verification**: Does the extracted data accurately reflect the main business risk discussed in the article? (Yes/No)

# 2. **State/Location Accuracy**: Is the state mentioned in the extracted data actually referenced in the article? (Yes/No)

# 3. **Industry Classification**: Is the industry classification appropriate based on the article content? (Yes/No)

# 4. **Risk Factor Mapping**: Does the risk factor correctly categorize the type of business risk described? (Yes/No)

# 5. **Impact Assessment**: Is the impact level (1-4) and type (Positive/Negative) appropriate for the event described? (Yes/No)

# 6. **Overall Accuracy Score**: Rate the overall accuracy from 1-10 (where 10 is perfect accuracy)

# 7. **Recommendations**: If accuracy score is below 7, provide specific corrections needed.

# 8. **Final Decision**: Should this record be INCLUDED or EXCLUDED from the final dataset?

# Respond in the following JSON format:
# {
#   "content_intent_accurate": true/false,
#   "location_accurate": true/false,
#   "industry_classification_accurate": true/false,
#   "risk_factor_accurate": true/false,
#   "impact_assessment_accurate": true/false,
#   "accuracy_score": 1-10,
#   "recommendations": "specific corrections needed",
#   "final_decision": "INCLUDE/EXCLUDE",
#   "verification_summary": "brief explanation of decision"
# }
# """

# async def verify_with_gemini(article, extracted_data):
#     """Use Gemini to verify the accuracy of extracted business risk data."""
#     try:
#         # Prepare the verification prompt
#         prompt = GEMINI_VERIFICATION_PROMPT.format(
#             title=article["Title"],
#             content=article["Content"][:3000],  # Limit content length for API
#             extracted_data=json.dumps(extracted_data, indent=2)
#         )
        
#         # Call Gemini API
#         response = gemini_model.generate_content(prompt)
#         verification_text = response.text
        
#         # Extract JSON from response
#         json_match = re.search(r'```(?:json)?(.*?)```', verification_text, re.DOTALL)
#         if json_match:
#             verification_text = json_match.group(1).strip()
        
#         # Parse verification JSON
#         try:
#             verification_data = json.loads(verification_text)
#         except json.JSONDecodeError:
#             json_start = verification_text.find('{')
#             json_end = verification_text.rfind('}') + 1
#             if json_start >= 0 and json_end > json_start:
#                 cleaned_json = verification_text[json_start:json_end]
#                 try:
#                     verification_data = json.loads(cleaned_json)
#                 except:
#                     print(f"Failed to parse Gemini verification JSON: {verification_text}")
#                     verification_data = {"final_decision": "EXCLUDE", "accuracy_score": 0}
#             else:
#                 print(f"Could not find JSON in Gemini response: {verification_text}")
#                 verification_data = {"final_decision": "EXCLUDE", "accuracy_score": 0}
        
#         return verification_data
    
#     except Exception as e:
#         print(f"Error with Gemini verification: {e}")
#         return {"final_decision": "EXCLUDE", "accuracy_score": 0, "verification_summary": f"Verification failed: {e}"}

# # ================================
# # 🔹 8. Location and Data Processing
# # ================================

# def extract_location_info(article, neighborhoods_data):
#     """Extract state and city information from article."""
#     content = article["Title"] + " " + article["Description"] + " " + article["Content"]
    
#     # Extract state
#     state = "Unknown"
#     for state_name in NIGERIAN_STATES:
#         if re.search(r'\b' + re.escape(state_name) + r'\b', content, re.IGNORECASE):
#             if state_name.lower() in ["abuja", "fct"]:
#                 state = "Federal Capital Territory"
#             else:
#                 state = state_name
#             break
    
#     # Extract city
#     city = "Unknown"
#     if state != "Unknown" and state in neighborhoods_data["by_state"]:
#         for neighborhood in neighborhoods_data["by_state"][state]:
#             if re.search(r'\b' + re.escape(neighborhood["name"]) + r'\b', content, re.IGNORECASE):
#                 city = neighborhood
#                 break
        
#         # If no specific city found, use state as city
#         if city == "Unknown":
#             city = state
    
#     return state, city

# def validate_state(state):
#     """Validate if the extracted state is a valid Nigerian state."""
#     if state == "Unknown":
#         return False
    
#     # Normalize state name
#     if state.lower() in ["abuja", "fct"]:
#         state = "Federal Capital Territory"
    
#     return state in NIGERIAN_STATES

# def create_business_risk_record(article, analysis, neighborhoods_data):
#     """Create a business risk record in the required format."""
#     # Get current date
#     today = datetime.now()
    
#     # Extract location
#     state, city = extract_location_info(article, neighborhoods_data)
    
#     # Override with AI analysis if available
#     if analysis.get("State"):
#         state = analysis["State"]
#     if analysis.get("City"):
#         city = analysis["City"]
    
#     # Validate state - if unknown, return None to exclude this record
#     if not validate_state(state):
#         print(f"Invalid or unknown state '{state}' - excluding record")
#         return None
    
#     # Ensure positive impact is always low level
#     impact_type = analysis.get("Impact Type", "Negative")
#     impact_level = analysis.get("Impact Level", 2)
    
#     if impact_type == "Positive" and impact_level != 1:
#         impact_level = 1
    
#     record = {
#         "Day": today.day,
#         "Month": today.strftime("%b"),
#         "Year": today.year,
#         "Date": today.strftime("%d/%m/%Y"),
#         "State": state,
#         "City": city,
#         "Industry": analysis.get("Industry", ""),
#         "Industry Subtype": analysis.get("Industry Subtype", ""),
#         "Business Risk Factor": analysis.get("Business Risk Factor", ""),
#         "Risk Indicator": analysis.get("Risk Indicator", ""),
#         "Impact Type": impact_type,
#         "Impact Level": impact_level,
#         "Event Headline": analysis.get("Event Headline", article["Title"][:100]),
#         "Evidence Source Link": article["Link"],
#         "Analyst Comments": "",
#         "Industry Risktype": analysis.get("Industry Risktype", "")
#     }
    
#     return record

# # ================================
# # 🔹 9. Enhanced Validation Functions
# # ================================

# def validate_business_record(record):
#     """Validate business risk record for completeness and accuracy."""
#     required_fields = ['Industry', 'Business Risk Factor', 'Risk Indicator', 'Impact Type', 'Impact Level']
    
#     for field in required_fields:
#         if not record.get(field) or record[field] == "":
#             return False, f"Missing required field: {field}"
    
#     # Validate Impact Type and Level relationship
#     if record['Impact Type'] == 'Positive' and record['Impact Level'] != 1:
#         return False, "Positive impact must have Low (1) impact level"
    
#     # Validate Impact Level range
#     if record['Impact Level'] not in [1, 2, 3, 4]:
#         return False, "Impact Level must be between 1-4"
    
#     # Validate Industry and Industry Subtype relationship
#     industry = record.get('Industry', '')
#     subtype = record.get('Industry Subtype', '')
    
#     if industry in INDUSTRY_MAPPING and subtype:
#         if subtype not in INDUSTRY_MAPPING[industry]:
#             return False, f"Invalid subtype {subtype} for industry {industry}"
    
#     # Validate state
#     if not validate_state(record.get('State', '')):
#         return False, "Invalid or unknown state"
    
#     return True, "Valid record"

# def cross_validate_with_content(record, article):
#     """Cross-validate extracted data with original article content."""
#     content = (article["Title"] + " " + article["Description"] + " " + article["Content"]).lower()
    
#     validation_score = 0
#     max_score = 5
    
#     # Check if industry is mentioned in content
#     industry = record.get('Industry', '').lower()
#     if industry and industry in content:
#         validation_score += 1
    
#     # Check if state is mentioned in content
#     state = record.get('State', '').lower()
#     if state and (state in content or state.replace(' ', '') in content):
#         validation_score += 1
    
#     # Check if risk factor keywords are present
#     risk_factor = record.get('Business Risk Factor', '').lower()
#     risk_keywords_map = {
#         'economic': ['economic', 'economy', 'inflation', 'gdp', 'unemployment', 'naira', 'dollar'],
#         'political': ['political', 'government', 'policy', 'corruption', 'stability'],
#         'operational': ['supply chain', 'infrastructure', 'disruption', 'operations'],
#         'social': ['social', 'unrest', 'protest', 'education', 'poverty'],
#         'regulatory and legal': ['regulation', 'compliance', 'legal', 'enforcement', 'law']
#     }
    
#     if risk_factor in risk_keywords_map:
#         if any(keyword in content for keyword in risk_keywords_map[risk_factor]):
#             validation_score += 1
    
#     # Check impact type alignment
#     impact_type = record.get('Impact Type', '').lower()
#     if impact_type == 'negative':
#         negative_words = ['crisis', 'attack', 'disruption', 'shortage', 'loss', 'damage', 'threat']
#         if any(word in content for word in negative_words):
#             validation_score += 1
#     elif impact_type == 'positive':
#         positive_words = ['growth', 'improvement', 'increase', 'boost', 'recovery', 'success']
#         if any(word in content for word in positive_words):
#             validation_score += 1
    
#     # Check headline relevance
#     headline = record.get('Event Headline', '').lower()
#     title = article["Title"].lower()
#     if headline and any(word in title for word in headline.split() if len(word) > 3):
#         validation_score += 1
    
#     return validation_score / max_score

# # ================================
# # 🔹 10. Email Function
# # ================================

# def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
#     """Send email with business risk data attached."""
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         with open(attachment_path, 'rb') as attachment:
#             part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
#         part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#         msg.attach(part)

#         server = smtplib.SMTP_SSL(smtp_server, smtp_port)
#         server.login(sender_email, smtp_password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())
#         server.quit()
        
#         print(f"Email sent successfully to {receiver_email}")
#     except Exception as e:
#         print(f"Error sending email: {e}")

# # ================================
# # 🔹 11. Main Function with Enhanced Verification
# # ================================

# async def main():
#     """Main function to run the business risk scraper with enhanced verification."""
#     print("Starting Enhanced Business Risk Data Scraper with Gemini Verification...")
    
#     # Load neighborhood data
#     neighborhoods_data = load_neighborhoods_data()
#     print(f"Loaded neighborhood data with {len(neighborhoods_data['all_neighborhoods'])} locations")
    
#     # Initialize WebDriver
#     driver = init_driver()
    
#     try:
#         # Get business article links
#         article_links = get_business_article_links(driver)
#         print(f"Found {len(article_links)} business article links")
        
#         # Scrape articles
#         articles = []
#         for url in article_links:
#             article = scrape_business_article(driver, url)
#             if article and is_business_relevant(article):
#                 articles.append(article)
#                 print(f"Found relevant business article: {article['Title'][:80]}...")
            
#             time.sleep(random.uniform(2, 4))  # Random delay between requests
        
#         print(f"Successfully scraped {len(articles)} relevant business articles")
        
#         if not articles:
#             print("No relevant business articles found. Exiting.")
#             return
        
#         # Analyze articles and create business risk records with enhanced verification
#         business_risk_records = []
#         verification_results = []
        
#         for i, article in enumerate(articles):
#             try:
#                 print(f"Processing article {i+1}/{len(articles)}: {article['Title'][:60]}...")
                
#                 # Step 1: Initial AI analysis
#                 analysis = await analyze_business_article(article)
                
#                 if not analysis:
#                     print("  ❌ Initial analysis failed - skipping")
#                     continue
                
#                 # Step 2: Create preliminary record
#                 preliminary_record = create_business_risk_record(article, analysis, neighborhoods_data)
                
#                 if not preliminary_record:
#                     print("  ❌ Record creation failed (likely unknown state) - skipping")
#                     continue
                
#                 # Step 3: Basic validation
#                 is_valid, validation_message = validate_business_record(preliminary_record)
#                 if not is_valid:
#                     print(f"  ❌ Basic validation failed: {validation_message} - skipping")
#                     continue
                
#                 # Step 4: Cross-validation with content
#                 content_score = cross_validate_with_content(preliminary_record, article)
#                 print(f"  📊 Content validation score: {content_score:.2f}")
                
#                 # Step 5: Gemini verification (second-level verification)
#                 print("  🔍 Performing Gemini verification...")
#                 gemini_verification = await verify_with_gemini(article, analysis)
                
#                 # Step 6: Decision based on verifications
#                 accuracy_score = gemini_verification.get('accuracy_score', 0)
#                 final_decision = gemini_verification.get('final_decision', 'EXCLUDE')
                
#                 print(f"  🎯 Gemini accuracy score: {accuracy_score}/10")
#                 print(f"  🎯 Gemini decision: {final_decision}")
                
#                 # Store verification results for reporting
#                 verification_results.append({
#                     'title': article['Title'][:100],
#                     'content_score': content_score,
#                     'gemini_score': accuracy_score,
#                     'gemini_decision': final_decision,
#                     'verification_summary': gemini_verification.get('verification_summary', ''),
#                     'included': False
#                 })
                
#                 # Include record only if it passes all verifications
#                 if final_decision == 'INCLUDE' and accuracy_score >= 7 and content_score >= 0.6:
#                     business_risk_records.append(preliminary_record)
#                     verification_results[-1]['included'] = True
#                     print("  ✅ Record INCLUDED after verification")
#                 else:
#                     print(f"  ❌ Record EXCLUDED - Decision: {final_decision}, Score: {accuracy_score}, Content: {content_score:.2f}")
                
#                 # Add small delay between Gemini API calls
#                 time.sleep(2)
                
#             except Exception as e:
#                 print(f"  ❌ Error processing article: {e}")
#                 continue
        
#         print(f"\n📊 Verification Summary:")
#         print(f"Total articles processed: {len(articles)}")
#         print(f"Records created after verification: {len(business_risk_records)}")
#         print(f"Exclusion rate: {((len(articles) - len(business_risk_records)) / len(articles) * 100):.1f}%")
        
#         # Save verification report
#         if verification_results:
#             verification_df = pd.DataFrame(verification_results)
#             verification_filename = f'verification_report_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
#             verification_df.to_csv(verification_filename, index=False)
#             print(f"Verification report saved to {verification_filename}")
        
#         # Save business risk data
#         if business_risk_records:
#             df = pd.DataFrame(business_risk_records)
            
#             # Sort by date and impact level (most recent and critical first)
#             df = df.sort_values(['Year', 'Month', 'Day', 'Impact Level'], 
#                               ascending=[False, False, False, False])
            
#             # Save to CSV
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             filename = f'business_risk_data_verified_{timestamp}.csv'
#             df.to_csv(filename, index=False)
#             print(f"Verified business risk data saved to {filename}")
            
#             # Display summary statistics
#             print("\n📊 Business Risk Data Summary:")
#             print(f"Total Verified Records: {len(df)}")
#             print(f"Industries Covered: {df['Industry'].nunique()}")
#             print(f"States Covered: {df['State'].nunique()}")
#             print(f"Risk Factors: {df['Business Risk Factor'].nunique()}")
            
#             print("\n🏭 Top Industries by Risk Events:")
#             industry_counts = df['Industry'].value_counts().head(5)
#             for industry, count in industry_counts.items():
#                 print(f"  {industry}: {count} events")
            
#             print("\n🌍 Top States by Risk Events:")
#             state_counts = df['State'].value_counts().head(5)
#             for state, count in state_counts.items():
#                 print(f"  {state}: {count} events")
            
#             print("\n⚠️ Risk Factor Distribution:")
#             risk_factor_counts = df['Business Risk Factor'].value_counts()
#             for factor, count in risk_factor_counts.items():
#                 print(f"  {factor}: {count} events")
            
#             print("\n📈 Impact Level Distribution:")
#             impact_counts = df['Impact Level'].value_counts().sort_index()
#             impact_labels = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}
#             for level, count in impact_counts.items():
#                 print(f"  Level {level} ({impact_labels.get(level, 'Unknown')}): {count} events")
            
#             # Generate insights based on verification results
#             included_count = sum(1 for vr in verification_results if vr['included'])
#             avg_gemini_score = sum(vr['gemini_score'] for vr in verification_results) / len(verification_results)
#             avg_content_score = sum(vr['content_score'] for vr in verification_results) / len(verification_results)
            
#             # Send email with the verified business risk data
#             send_email(
#                 sender_email=os.environ.get('USER_EMAIL'),
#                 receiver_email="riskcontrolservicesnig@gmail.com",
#                 subject="Verified Daily Business Risk Data Update",
#                 body=f"""Enhanced Business Risk Intelligence Report with Gemini Verification

# 🔍 VERIFICATION METRICS:
# - Articles Processed: {len(articles)}
# - Records After Verification: {len(df)}
# - Quality Acceptance Rate: {(included_count / len(verification_results) * 100):.1f}%
# - Average Gemini Accuracy Score: {avg_gemini_score:.1f}/10
# - Average Content Validation Score: {avg_content_score:.2f}

# 📊 BUSINESS INTELLIGENCE SUMMARY:
# - Total Verified Risk Events: {len(df)}
# - Industries Monitored: {df['Industry'].nunique()}
# - States with Business Risks: {df['State'].nunique()}
# - High/Critical Events: {len(df[df['Impact Level'] >= 3])}

# 🔍 TOP RISK AREAS:
# - Primary Industry at Risk: {df['Industry'].value_counts().index[0] if len(df) > 0 else 'N/A'}
# - Primary Risk Factor: {df['Business Risk Factor'].value_counts().index[0] if len(df) > 0 else 'N/A'}
# - Most Affected State: {df['State'].value_counts().index[0] if len(df) > 0 else 'N/A'}

# 🎯 QUALITY ASSURANCE:
# - All records have been verified using Gemini AI for accuracy
# - Only records with 70%+ accuracy scores are included
# - Unknown states and invalid data have been filtered out
# - Cross-validation performed against original news content

# 📋 ATTACHED FILES:
# 1. {filename} - Verified business risk data
# 2. {verification_filename} - Detailed verification report

# This enhanced report ensures maximum data quality and reliability for strategic business risk analysis.

# Generated automatically with AI-powered verification from Nigerian business news sources.
# """,
#                 attachment_path=filename,
#                 smtp_server="smtp.gmail.com",
#                 smtp_port=465,
#                 smtp_password=os.environ.get('USER_PASSWORD')
#             )
            
#             print("✅ Enhanced business risk data processing with verification completed successfully")
#         else:
#             print("❌ No business risk records passed verification.")
    
#     except Exception as e:
#         print(f"❌ Error in main processing: {e}")
    
#     finally:
#         # Clean up
#         driver.quit()

# # ================================
# # 🔹 12. Script Execution
# # ================================

# if __name__ == "__main__":
#     print("🚀 Starting Enhanced Business Risk Scraper with Gemini Verification...")
#     print("⚠️  Remember to replace 'YOUR_GEMINI_API_KEY_HERE' with your actual Gemini API key!")
#     asyncio.run(main())



# import os
# import random
# import time
# import asyncio
# import pandas as pd
# import re
# from datetime import datetime
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# import requests
# from bs4 import BeautifulSoup
# from groq import AsyncGroq
# import google.generativeai as genai
# import json
# from urllib.parse import urljoin, urlparse
# import logging

# # ================================
# # 🔹 1. Setup Logging
# # ================================

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # ================================
# # 🔹 2. Initialize APIs
# # ================================

# # Initialize Groq API Client
# client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY", "your_groq_api_key_here"))

# # Initialize Gemini API Client
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual Gemini API key
# genai.configure(api_key=GEMINI_API_KEY)
# gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# # ================================
# # 🔹 3. Constants and Configuration
# # ================================

# # User-Agent Rotation
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
# ]

# # DailyPost specific URLs
# DAILYPOST_URLS = [
#     "https://dailypost.ng/category/business/",
#     "https://dailypost.ng/category/economy/",
#     "https://dailypost.ng/"
# ]

# # Strict Business Keywords for filtering
# BUSINESS_KEYWORDS = [
#     'gdp', 'inflation', 'unemployment', 'economic growth', 'recession', 'naira', 'dollar', 'forex',
#     'interest rate', 'monetary policy', 'fiscal policy', 'budget', 'revenue', 'tax', 'taxation',
#     'business', 'company', 'industry', 'factory', 'manufacturing', 'production', 'supply chain', 'logistics',
#     'import', 'export', 'trade', 'commerce', 'investment', 'investor', 'market', 'price', 'cost',
#     'infrastructure', 'port', 'airport', 'road', 'railway', 'power', 'electricity', 'fuel', 'energy',
#     'telecommunications', 'banking', 'finance', 'insurance', 'loan', 'credit',
#     'oil', 'gas', 'petroleum', 'pipeline', 'refinery', 'crude', 'nnpc', 'upstream', 'downstream',
#     'agriculture', 'farming', 'crop', 'livestock', 'food', 'harvest',
#     'mining', 'solid minerals', 'healthcare', 'hospital', 'medical', 'drug', 'pharmaceutical',
#     'construction', 'building', 'real estate', 'property', 'housing',
#     'strike affecting business', 'factory closure', 'plant shutdown', 'supply disruption',
#     'regulatory compliance', 'business license', 'operations', 'productivity', 'profitability'
# ]

# # Political Keywords to EXCLUDE (unless they have direct business impact)
# POLITICAL_KEYWORDS_TO_EXCLUDE = [
#     'election', 'campaign', 'political party', 'pdp', 'apc', 'labour party', 'candidate',
#     'governor race', 'senate race', 'political crisis', 'coalition', 'political alliance',
#     'political defection', 'party leadership', 'political rally', 'political meeting'
# ]

# # Nigerian states
# NIGERIAN_STATES = [
#     'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
#     'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
#     'Federal Capital Territory', 'FCT', 'Abuja', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 
#     'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 
#     'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 
#     'Yobe', 'Zamfara'
# ]

# # Business Risk Framework
# BUSINESS_RISK_FACTORS = {
#     "Economic": ["GDP", "Unemployment Rate", "Inflation rate"],
#     "Political": ["Government stability", "Corruption", "Rule of law"],
#     "Technology": ["Digital Infrastructure", "Cybersecurity", "Technology Adoption"],
#     "Social": ["Poverty Rate", "Social unrest", "Education"],
#     "Environmental": ["Air and water quality", "Natural disaster", "Climate change probability"],
#     "Operational": ["Infrastructure Quality", "Supply chain disruption", "Business Continuity"],
#     "Healthcare": ["Healthcare Access", "Disease prevalence", "Healthcare Infrastructure"],
#     "Regulatory and Legal": ["Burden Of Compliance", "Legal Framework", "Enforcement"]
# }

# # Strict Industry Mapping with Keywords
# INDUSTRY_MAPPING = {
#     "Manufacturing": {
#         "subtypes": ["Factory", "Warehouse", "Processing Plant"],
#         "keywords": ["factory", "manufacturing", "production", "plant", "assembly", "industrial", "processing", "warehouse"]
#     },
#     "Healthcare": {
#         "subtypes": ["Hospitals", "Pharmaceutical"],
#         "keywords": ["hospital", "medical", "healthcare", "pharmaceutical", "drug", "medicine", "clinic", "health"]
#     },
#     "Finance & Banking": {
#         "subtypes": ["Banks", "Insurance", "Mortgage", "Microfinance"],
#         "keywords": ["bank", "banking", "finance", "financial", "insurance", "loan", "credit", "mortgage", "microfinance"]
#     },
#     "Oil & Gas": {
#         "subtypes": ["Upstream", "Downstream"],
#         "keywords": ["oil", "gas", "petroleum", "crude", "refinery", "pipeline", "nnpc", "upstream", "downstream", "fuel"]
#     },
#     "Education": {
#         "subtypes": ["Primary", "Secondary", "Tertiary"],
#         "keywords": ["school", "education", "university", "college", "student", "teacher", "academic", "classroom"]
#     },
#     "Logistics & Transportation": {
#         "subtypes": ["Logistics", "Transportation (Land)", "Aviation (Air)", "Maritime (Sea)"],
#         "keywords": ["transport", "logistics", "shipping", "cargo", "freight", "port", "airport", "railway", "aviation", "maritime"]
#     },
#     "Travel & Hospitality": {
#         "subtypes": ["Hotel", "Restaurant", "Tourism"],
#         "keywords": ["hotel", "tourism", "restaurant", "hospitality", "travel", "tourist", "accommodation"]
#     },
#     "Agro-allied": {
#         "subtypes": ["Farm", "Storage", "Livestock"],
#         "keywords": ["agriculture", "farming", "farm", "crop", "livestock", "agricultural", "harvest", "food production"]
#     },
#     "Telecommunications": {
#         "subtypes": ["Telcomm", "Cloud", "Network"],
#         "keywords": ["telecommunications", "telecom", "network", "internet", "communication", "mobile", "broadband"]
#     },
#     "Mining": {
#         "subtypes": ["Mining", "Processing"],
#         "keywords": ["mining", "mineral", "gold", "coal", "tin", "iron ore", "solid minerals", "extraction"]
#     },
#     "Real Estate & Construction": {
#         "subtypes": ["Construction", "Real estate"],
#         "keywords": ["construction", "building", "real estate", "property", "housing", "infrastructure", "contractor"]
#     }
# }

# # Impact Level Mapping
# IMPACT_LEVEL_MAPPING = {
#     1: "Low",
#     2: "Medium", 
#     3: "High",
#     4: "Critical",
#     "Low": 1,
#     "Medium": 2,
#     "High": 3,
#     "Critical": 4
# }

# # ================================
# # 🔹 4. Request Session Setup
# # ================================

# def create_session():
#     """Create a requests session with proper headers and configuration."""
#     session = requests.Session()
#     session.headers.update({
#         'User-Agent': random.choice(USER_AGENTS),
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Accept-Encoding': 'gzip, deflate',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1'
#     })
#     return session

# def make_request_with_retry(session, url, max_retries=3, delay=2):
#     """Make HTTP request with retry mechanism."""
#     for attempt in range(max_retries):
#         try:
#             response = session.get(url, timeout=30)
#             response.raise_for_status()
#             return response
#         except requests.exceptions.RequestException as e:
#             logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
#             if attempt < max_retries - 1:
#                 time.sleep(delay * (attempt + 1))
#             else:
#                 logger.error(f"All retry attempts failed for {url}")
#                 return None
#     return None

# # ================================
# # 🔹 5. Web Scraping Functions
# # ================================

# def get_dailypost_article_links(session, limit=50):
#     """Extract article links from DailyPost pages."""
#     all_links = set()
    
#     for url in DAILYPOST_URLS:
#         try:
#             logger.info(f"Scraping links from: {url}")
#             response = make_request_with_retry(session, url)
            
#             if not response:
#                 continue
                
#             soup = BeautifulSoup(response.content, 'html.parser')
            
#             # DailyPost specific selectors
#             article_links = soup.find_all('a', href=True)
            
#             for link in article_links:
#                 href = link.get('href')
#                 if href:
#                     # Convert relative URLs to absolute
#                     full_url = urljoin(url, href)
                    
#                     # Check if it's a valid DailyPost article URL with date pattern
#                     if 'dailypost.ng' in full_url and re.search(r'/\d{4}/\d{2}/\d{2}/', full_url):
#                         all_links.add(full_url)
                        
#             logger.info(f"Found {len(all_links)} unique links so far")
            
#             # Add delay between requests
#             time.sleep(random.uniform(2, 4))
            
#         except Exception as e:
#             logger.error(f"Error scraping {url}: {e}")
#             continue
    
#     # Limit the number of articles to process
#     limited_links = list(all_links)[:limit]
#     logger.info(f"Selected {len(limited_links)} articles for processing")
#     return limited_links

# def scrape_dailypost_article(session, url):
#     """Scrape individual DailyPost article."""
#     try:
#         response = make_request_with_retry(session, url)
#         if not response:
#             return None
            
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Extract title
#         title_tag = soup.find('h1', class_='entry-title') or soup.find('h1') or soup.find('title')
#         title = title_tag.get_text(strip=True) if title_tag else "No title found"
        
#         # Extract meta description
#         meta_desc = soup.find('meta', {'name': 'description'})
#         description = meta_desc.get('content', '').strip() if meta_desc else "No description found"
        
#         # Extract article content
#         article_text = ""
        
#         # Try different content selectors for DailyPost
#         content_selectors = [
#             {'class': 'entry-content'},
#             {'id': 'mvp-content-main'},
#             {'class': 'post-content'},
#             {'class': 'article-content'},
#             {'class': 'content'}
#         ]
        
#         for selector in content_selectors:
#             content_div = soup.find('div', selector)
#             if content_div:
#                 paragraphs = content_div.find_all('p')
#                 article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
#                 break
        
#         # Fallback: get all paragraphs
#         if not article_text:
#             paragraphs = soup.find_all('p')
#             article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
#         # Basic content validation
#         if len(article_text) < 100:
#             logger.warning(f"Article content too short: {url}")
#             return None
        
#         return {
#             "Title": title,
#             "Description": description,
#             "Content": article_text,
#             "Link": url
#         }
        
#     except Exception as e:
#         logger.error(f"Error scraping article {url}: {e}")
#         return None

# def is_business_relevant(article):
#     """Check if article is relevant to business risks with strict filtering."""
#     if not article:
#         return False
        
#     content = (article.get("Title", "") + " " + 
#               article.get("Description", "") + " " + 
#               article.get("Content", "")).lower()
    
#     # First check if it's purely political content to exclude
#     political_exclusion_count = sum(1 for keyword in POLITICAL_KEYWORDS_TO_EXCLUDE if keyword in content)
    
#     # If it's heavily political, check if it has business impact
#     if political_exclusion_count >= 2:
#         # Only allow if it has strong business keywords too
#         business_keyword_count = sum(1 for keyword in BUSINESS_KEYWORDS if keyword in content)
#         if business_keyword_count < 3:
#             logger.info("Excluding purely political content with no business impact")
#             return False
    
#     # Check for business keywords
#     keyword_count = sum(1 for keyword in BUSINESS_KEYWORDS if keyword in content)
    
#     # Article is relevant if it contains at least 2 business keywords
#     return keyword_count >= 2

# def validate_industry_content_match(industry, content):
#     """Validate that the industry actually matches the article content."""
#     if not industry or industry not in INDUSTRY_MAPPING:
#         return False
    
#     content_lower = content.lower()
#     industry_keywords = INDUSTRY_MAPPING[industry]["keywords"]
    
#     # Check if at least 2 industry-specific keywords are present
#     keyword_matches = sum(1 for keyword in industry_keywords if keyword in content_lower)
    
#     return keyword_matches >= 2

# # ================================
# # 🔹 6. AI Analysis Functions
# # ================================

# STRICT_BUSINESS_ANALYSIS_PROMPT = """
# You are an expert business risk analyst specializing in Nigerian market conditions. 
# Analyze the following news article and extract business risk information ONLY if it has DIRECT business impact.

# CRITICAL RULES:
# 1. DO NOT classify political news as business risks unless they have DIRECT impact on business operations
# 2. Political party activities, elections, campaigns, and leadership changes are NOT business risks
# 3. Only include if the article discusses specific business impacts like:
#    - Factory closures or operational disruptions
#    - Supply chain disruptions
#    - Regulatory changes affecting business operations
#    - Economic indicators affecting business
#    - Industry-specific operational issues
#    - Infrastructure problems affecting business operations

# 4. The INDUSTRY must be directly mentioned or clearly implied in the article content
# 5. If you cannot find a clear industry connection, return "NO_BUSINESS_RISK"

# Extract the following information in JSON format ONLY if genuine business risk:

# 1. **Industry** (Must be directly related to article content):
#    - Manufacturing (only if factories, production, or manufacturing mentioned)
#    - Healthcare (only if hospitals, medical facilities, or pharmaceutical mentioned)
#    - Finance & Banking (only if banks, financial institutions, or banking operations mentioned)
#    - Oil & Gas (only if oil, gas, petroleum, refinery, or energy sector mentioned)
#    - Education (only if schools, universities, or educational institutions mentioned)
#    - Logistics & Transportation (only if transport, shipping, ports, or logistics mentioned)
#    - Travel & Hospitality (only if hotels, tourism, or hospitality sector mentioned)
#    - Agro-allied (only if agriculture, farming, or food production mentioned)
#    - Telecommunications (only if telecom, networks, or communication infrastructure mentioned)
#    - Mining (only if mining, minerals, or extraction mentioned)
#    - Real Estate & Construction (only if construction, building, or real estate mentioned)

# 2. **Industry Subtype** (Based on specific mentions in article)

# 3. **Business Risk Factor**: Economic, Political, Technology, Social, Environmental, Operational, Healthcare, Regulatory and Legal

# 4. **Risk Indicator**: GDP, Unemployment Rate, Inflation Rate, Government Stability, Corruption, Rule of Law, Digital Infrastructure, Cybersecurity, Technology Adoption, Poverty Rate, Social Unrest, Education, Air and Water Quality, Natural Disaster, Climate Change Probability, Infrastructure Quality, Supply Chain Disruption, Business Continuity, Healthcare Access, Disease Prevalence, Healthcare Infrastructure, Burden of Compliance, Legal Framework, Enforcement

# 5. **Impact Type**: Positive or Negative

# 6. **Impact Level**: Low, Medium, High, Critical

# 7. **Event Headline** (Max 20 words): Focus on business impact, not political aspects

# 8. **State**: Nigerian state mentioned in the article
# 9. **City**: Specific city or location mentioned

# IMPORTANT:
# - If the article is primarily about politics without clear business impact, return "NO_BUSINESS_RISK"
# - If you cannot find specific industry keywords in the content, return "NO_BUSINESS_RISK"
# - Only positive impacts should be Low level
# - The industry must be explicitly supported by content keywords

# Return your analysis in JSON format or "NO_BUSINESS_RISK" if not applicable.
# """

# async def analyze_business_article(article):
#     """Use AI to analyze business article and extract risk information with strict validation."""
#     try:
#         response = await client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": STRICT_BUSINESS_ANALYSIS_PROMPT},
#                 {"role": "user", "content": f"Title: {article['Title']}\n\nDescription: {article['Description']}\n\nContent: {article['Content'][:4000]}"}
#             ],
#             model="llama3-8b-8192",
#             temperature=0.1,  # Lower temperature for more consistent results
#             max_tokens=2000
#         )
        
#         extracted_text = response.choices[0].message.content.strip()
        
#         # Check if AI determined no business risk
#         if "NO_BUSINESS_RISK" in extracted_text:
#             logger.info("AI determined no genuine business risk")
#             return None
        
#         # Find JSON content
#         json_match = re.search(r'```(?:json)?(.*?)```', extracted_text, re.DOTALL)
#         if json_match:
#             extracted_text = json_match.group(1).strip()
        
#         # Try to parse JSON
#         try:
#             extracted_data = json.loads(extracted_text)
#         except json.JSONDecodeError:
#             json_start = extracted_text.find('{')
#             json_end = extracted_text.rfind('}') + 1
#             if json_start >= 0 and json_end > json_start:
#                 cleaned_json = extracted_text[json_start:json_end]
#                 try:
#                     extracted_data = json.loads(cleaned_json)
#                 except:
#                     logger.error(f"Failed to parse JSON: {extracted_text}")
#                     return None
#             else:
#                 logger.error(f"Could not find JSON object: {extracted_text}")
#                 return None
        
#         # Additional validation: Check if industry matches content
#         industry = extracted_data.get("Industry", "")
#         full_content = article['Title'] + " " + article['Description'] + " " + article['Content']
        
#         if not validate_industry_content_match(industry, full_content):
#             logger.info(f"Industry '{industry}' doesn't match article content - excluding")
#             return None
        
#         return extracted_data
    
#     except Exception as e:
#         logger.error(f"Error analyzing business article: {e}")
#         return None

# # ================================
# # 🔹 7. Data Processing Functions
# # ================================

# def extract_location_info(article):
#     """Extract state and city information from article."""
#     content = (article.get("Title", "") + " " + 
#               article.get("Description", "") + " " + 
#               article.get("Content", "")).lower()
    
#     # Extract state
#     state = "Unknown"
#     for state_name in NIGERIAN_STATES:
#         if re.search(r'\b' + re.escape(state_name.lower()) + r'\b', content):
#             if state_name.lower() in ["abuja", "fct"]:
#                 state = "Federal Capital Territory"
#             else:
#                 state = state_name
#             break
    
#     return state, state  # Use state as city for simplicity

# def validate_state(state):
#     """Validate if the extracted state is a valid Nigerian state."""
#     if state == "Unknown" or not state:
#         return False
    
#     # Normalize state name
#     if state.lower() in ["abuja", "fct"]:
#         state = "Federal Capital Territory"
    
#     return state in NIGERIAN_STATES

# def convert_impact_level_to_text(impact_level):
#     """Convert numeric impact level to descriptive text."""
#     if isinstance(impact_level, (int, float)):
#         return IMPACT_LEVEL_MAPPING.get(int(impact_level), "Low")
#     elif isinstance(impact_level, str):
#         # If it's already text, validate and return
#         if impact_level.title() in ["Low", "Medium", "High", "Critical"]:
#             return impact_level.title()
#         else:
#             # Try to convert if it's a number in string form
#             try:
#                 return IMPACT_LEVEL_MAPPING.get(int(impact_level), "Low")
#             except ValueError:
#                 return "Low"
#     else:
#         return "Low"

# def create_business_risk_record(article, extracted_data):
#     """Create a business risk record using extracted data."""
#     # Get current date
#     today = datetime.now()
    
#     # Use extracted data
#     state = extracted_data.get("State", "Unknown")
#     city = extracted_data.get("City", "Unknown")
    
#     # If AI didn't provide location, try to extract it
#     if state == "Unknown" or not state:
#         state, city = extract_location_info(article)
    
#     # Validate state - if unknown, return None to exclude this record
#     if not validate_state(state):
#         logger.warning(f"Invalid or unknown state '{state}' - excluding record")
#         return None
    
#     # Ensure positive impact is always low level
#     impact_type = extracted_data.get("Impact Type", "Negative")
#     impact_level = extracted_data.get("Impact Level", "Medium")
    
#     # Convert impact level to text format
#     impact_level_text = convert_impact_level_to_text(impact_level)
    
#     if impact_type == "Positive" and impact_level_text != "Low":
#         impact_level_text = "Low"
    
#     record = {
#         "Day": today.day,
#         "Month": today.strftime("%b"),
#         "Year": today.year,
#         "Date": today.strftime("%d/%m/%Y"),
#         "State": state,
#         "City": city,
#         "Industry": extracted_data.get("Industry", ""),
#         "Industry Subtype": extracted_data.get("Industry Subtype", ""),
#         "Business Risk Factor": extracted_data.get("Business Risk Factor", ""),
#         "Risk Indicator": extracted_data.get("Risk Indicator", ""),
#         "Impact Type": impact_type,
#         "Impact Level": impact_level_text,
#         "Event Headline": extracted_data.get("Event Headline", article.get("Title", "")[:100]),
#         "Evidence Source Link": article.get("Link", "")
#     }
    
#     return record

# def validate_business_record(record):
#     """Validate business risk record for completeness and accuracy."""
#     required_fields = ['Industry', 'Business Risk Factor', 'Risk Indicator', 'Impact Type', 'Impact Level']
    
#     for field in required_fields:
#         if not record.get(field) or record[field] == "":
#             return False, f"Missing required field: {field}"
    
#     # Validate Impact Type and Level relationship
#     if record['Impact Type'] == 'Positive' and record['Impact Level'] != 'Low':
#         return False, "Positive impact must have Low impact level"
    
#     # Validate Impact Level options
#     if record['Impact Level'] not in ['Low', 'Medium', 'High', 'Critical']:
#         return False, "Impact Level must be Low, Medium, High, or Critical"
    
#     # Validate state
#     if not validate_state(record.get('State', '')):
#         return False, "Invalid or unknown state"
    
#     # Validate industry is in our mapping
#     if record.get('Industry', '') not in INDUSTRY_MAPPING:
#         return False, f"Invalid industry: {record.get('Industry', '')}"
    
#     return True, "Valid record"

# # ================================
# # 🔹 8. Email Function
# # ================================

# def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
#     """Send email with business risk data attached."""
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         with open(attachment_path, 'rb') as attachment:
#             part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
#         part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#         msg.attach(part)

#         server = smtplib.SMTP_SSL(smtp_server, smtp_port)
#         server.login(sender_email, smtp_password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())
#         server.quit()
        
#         logger.info(f"Email sent successfully to {receiver_email}")
#     except Exception as e:
#         logger.error(f"Error sending email: {e}")

# # ================================
# # 🔹 9. Main Function
# # ================================

# async def main():
#     """Main function to run the business risk scraper."""
#     logger.info("🚀 Starting DailyPost Business Risk Scraper with Strict Industry Validation...")
    
#     # Create session
#     session = create_session()
    
#     try:
#         # Get article links from DailyPost
#         logger.info("📄 Extracting article links from DailyPost...")
#         article_links = get_dailypost_article_links(session, limit=30)
        
#         if not article_links:
#             logger.error("No article links found. Exiting.")
#             return
        
#         # Scrape articles
#         logger.info(f"📖 Scraping {len(article_links)} articles...")
#         articles = []
        
#         for i, url in enumerate(article_links):
#             logger.info(f"Scraping article {i+1}/{len(article_links)}: {url}")
            
#             article = scrape_dailypost_article(session, url)
#             if article and is_business_relevant(article):
#                 articles.append(article)
#                 logger.info(f"✅ Added relevant article: {article['Title'][:60]}...")
#             else:
#                 logger.info("❌ Article not relevant or failed to scrape")
            
#             # Rate limiting
#             time.sleep(random.uniform(1, 3))
        
#         logger.info(f"📊 Successfully scraped {len(articles)} relevant business articles")
        
#         if not articles:
#             logger.error("No relevant business articles found. Exiting.")
#             return
        
#         # Process articles with AI analysis
#         logger.info("🤖 Processing articles with strict AI analysis...")
#         business_risk_records = []
#         processing_log = []
        
#         for i, article in enumerate(articles):
#             try:
#                 logger.info(f"Processing article {i+1}/{len(articles)}: {article['Title'][:60]}...")
                
#                 # AI analysis with strict validation
#                 logger.info("  🔍 Performing strict AI analysis...")
#                 extracted_data = await analyze_business_article(article)
                
#                 if not extracted_data:
#                     logger.warning("  ❌ AI analysis failed or no business risk identified - skipping")
#                     processing_log.append({
#                         'title': article['Title'][:100],
#                         'status': 'no_business_risk_identified',
#                         'included': False
#                     })
#                     continue
                
#                 # Create record
#                 logger.info("  📝 Creating business risk record...")
#                 record = create_business_risk_record(article, extracted_data)
                
#                 if not record:
#                     logger.warning("  ❌ Record creation failed")
#                     processing_log.append({
#                         'title': article['Title'][:100],
#                         'status': 'failed_record_creation',
#                         'included': False
#                     })
#                     continue
                
#                 # Validate record
#                 is_valid, validation_message = validate_business_record(record)
#                 if not is_valid:
#                     logger.warning(f"  ❌ Validation failed: {validation_message}")
#                     processing_log.append({
#                         'title': article['Title'][:100],
#                         'status': f'validation_failed_{validation_message}',
#                         'included': False
#                     })
#                     continue
                
#                 # Add record to final list
#                 business_risk_records.append(record)
                
#                 logger.info(f"  ✅ Record INCLUDED - Industry: {record['Industry']}")
#                 processing_log.append({
#                     'title': article['Title'][:100],
#                     'status': 'included',
#                     'industry': record['Industry'],
#                     'included': True
#                 })
                
#                 # Add delay between API calls
#                 await asyncio.sleep(2)
                
#             except Exception as e:
#                 logger.error(f"  ❌ Error processing article: {e}")
#                 processing_log.append({
#                     'title': article['Title'][:100],
#                     'status': f'processing_error_{str(e)[:50]}',
#                     'included': False
#                 })
#                 continue
        
#         # Generate summary
#         logger.info(f"\n📊 Processing Summary:")
#         logger.info(f"Total articles processed: {len(articles)}")
#         logger.info(f"Records created: {len(business_risk_records)}")
#         logger.info(f"Success rate: {(len(business_risk_records) / len(articles) * 100):.1f}%")
        
#         # Save processing log
#         if processing_log:
#             processing_df = pd.DataFrame(processing_log)
#             processing_filename = f'processing_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
#             processing_df.to_csv(processing_filename, index=False)
#             logger.info(f"Processing log saved to {processing_filename}")
        
#         # Save business risk data
#         if business_risk_records:
#             df = pd.DataFrame(business_risk_records)
            
#             # Sort by impact level and industry
#             impact_order = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
#             df['Impact_Sort'] = df['Impact Level'].map(impact_order)
#             df = df.sort_values(['Impact_Sort', 'Industry'], ascending=[False, True])
#             df = df.drop('Impact_Sort', axis=1)
            
#             # Save to CSV
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f'business_risk_data_{timestamp}.csv'
#             df.to_csv(filename, index=False)
#             logger.info(f"Business risk data saved to {filename}")
            
#             # Display summary statistics
#             logger.info("\n📈 Business Risk Data Summary:")
#             logger.info(f"Total Records: {len(df)}")
#             logger.info(f"Industries Covered: {df['Industry'].nunique()}")
#             logger.info(f"States Covered: {df['State'].nunique()}")
            
#             logger.info("\n🏭 Industries with Risk Events:")
#             industry_counts = df['Industry'].value_counts()
#             for industry, count in industry_counts.items():
#                 logger.info(f"  {industry}: {count} events")
            
#             logger.info("\n🌍 States with Risk Events:")
#             state_counts = df['State'].value_counts().head(5)
#             for state, count in state_counts.items():
#                 logger.info(f"  {state}: {count} events")
            
#             logger.info("\n📊 Impact Level Distribution:")
#             impact_counts = df['Impact Level'].value_counts()
#             for level, count in impact_counts.items():
#                 logger.info(f"  {level}: {count} events")
            
#             logger.info("\n🔍 Risk Factor Distribution:")
#             risk_factor_counts = df['Business Risk Factor'].value_counts()
#             for factor, count in risk_factor_counts.items():
#                 logger.info(f"  {factor}: {count} events")
            
#             # Send email if credentials are provided
#             sender_email = os.environ.get('USER_EMAIL')
#             sender_password = os.environ.get('USER_PASSWORD')
            
#             if sender_email and sender_password:
#                 try:
#                     send_email(
#                         sender_email=sender_email,
#                         receiver_email="riskcontrolservicesnig@gmail.com",
#                         subject="Validated Business Risk Intelligence Report - DailyPost",
#                         body=f"""Validated Business Risk Intelligence Report - DailyPost

# 🔍 QUALITY ASSURANCE SUMMARY:
# - Articles Processed: {len(articles)}
# - Business Risk Records Generated: {len(df)}
# - Success Rate: {(len(business_risk_records) / len(articles) * 100):.1f}%
# - Strict Industry Validation Applied: ✅
# - Political Content Filtering: ✅

# 📊 BUSINESS INTELLIGENCE OVERVIEW:
# - Total Risk Events: {len(df)}
# - Industries Monitored: {df['Industry'].nunique()}
# - States with Business Risks: {df['State'].nunique()}
# - Critical/High Impact Events: {len(df[df['Impact Level'].isin(['Critical', 'High'])])}

# 🎯 TOP RISK INSIGHTS:
# - Primary Industry at Risk: {df['Industry'].value_counts().index[0] if len(df) > 0 else 'N/A'}
# - Primary Risk Factor: {df['Business Risk Factor'].value_counts().index[0] if len(df) > 0 else 'N/A'}
# - Most Affected State: {df['State'].value_counts().index[0] if len(df) > 0 else 'N/A'}

# 🏭 INDUSTRY DISTRIBUTION:
# {chr(10).join([f"- {industry}: {count} events" for industry, count in df['Industry'].value_counts().items()])}

# 📈 IMPACT DISTRIBUTION:
# {chr(10).join([f"- {level}: {count} events" for level, count in df['Impact Level'].value_counts().items()])}

# 🔧 QUALITY IMPROVEMENTS:
# - Removed "Verification Status" and "Confidence Score" columns
# - Strict industry-content validation implemented
# - Political content filtering (no random industry assignment)
# - Industry keywords matching validation
# - Enhanced business relevance filtering

# 📋 ATTACHED FILES:
# 1. {filename} - Validated business risk dataset
# 2. {processing_filename} - Processing log with inclusion/exclusion details

# This report ensures only genuine business risks with proper industry classification are included.

# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# """,
#                         attachment_path=filename,
#                         smtp_server="smtp.gmail.com",
#                         smtp_port=465,
#                         smtp_password=sender_password
#                     )
#                 except Exception as e:
#                     logger.error(f"Failed to send email: {e}")
#             else:
#                 logger.info("Email credentials not provided - skipping email send")
            
#             logger.info("✅ Validated business risk processing completed successfully!")
            
#             # Display sample records for verification
#             logger.info("\n🔍 Sample Business Risk Records:")
#             for i, record in enumerate(df.head(3).to_dict('records')):
#                 logger.info(f"\nRecord {i+1}:")
#                 logger.info(f"  Industry: {record['Industry']}")
#                 logger.info(f"  Event: {record['Event Headline']}")
#                 logger.info(f"  Risk Factor: {record['Business Risk Factor']}")
#                 logger.info(f"  Impact Level: {record['Impact Level']}")
#                 logger.info(f"  State: {record['State']}")
#         else:
#             logger.warning("❌ No validated business risk records were generated.")
    
#     except Exception as e:
#         logger.error(f"❌ Error in main processing: {e}")
#         raise

# # ================================
# # 🔹 10. Script Execution
# # ================================

# if __name__ == "__main__":
#     print("🚀 Starting Validated DailyPost Business Risk Scraper...")
#     print("🔧 Features: Strict industry validation, political content filtering")
#     print("📊 Target: DailyPost business articles with genuine industry impact")
#     print("🚫 Excludes: Political content without business relevance")
#     print("=" * 70)
    
#     asyncio.run(main())

# import os
# import random
# import time
# import asyncio
# import pandas as pd
# import re
# from datetime import datetime
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# import requests
# from bs4 import BeautifulSoup
# from groq import AsyncGroq
# import google.generativeai as genai
# import json
# from urllib.parse import urljoin, urlparse
# import logging

# # ================================
# # 🔹 1. Setup Logging
# # ================================

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # ================================
# # 🔹 2. Initialize APIs
# # ================================

# # Initialize Groq API Client
# client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY", "your_groq_api_key_here"))

# # Initialize Gemini API Client
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual Gemini API key
# genai.configure(api_key=GEMINI_API_KEY)
# gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# # ================================
# # 🔹 3. Constants and Configuration
# # ================================

# # User-Agent Rotation
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
# ]

# # DailyPost specific URLs
# DAILYPOST_URLS = [
#     "https://dailypost.ng/category/business/",
#     "https://dailypost.ng/category/economy/",
#     "https://dailypost.ng/"
# ]

# # Business Keywords for filtering
# BUSINESS_KEYWORDS = [
#     'gdp', 'inflation', 'unemployment', 'economic', 'economy', 'recession', 'growth', 'naira', 'dollar', 'forex',
#     'interest rate', 'monetary policy', 'fiscal policy', 'budget', 'revenue', 'tax', 'taxation',
#     'business', 'company', 'industry', 'factory', 'manufacturing', 'production', 'supply chain', 'logistics',
#     'import', 'export', 'trade', 'commerce', 'investment', 'investor', 'market', 'price', 'cost',
#     'infrastructure', 'port', 'airport', 'road', 'railway', 'power', 'electricity', 'fuel', 'energy',
#     'telecommunications', 'banking', 'finance', 'insurance', 'loan', 'credit',
#     'oil', 'gas', 'petroleum', 'pipeline', 'refinery', 'crude', 'nnpc', 'upstream', 'downstream',
#     'agriculture', 'farming', 'crop', 'livestock', 'food', 'harvest',
#     'mining', 'solid minerals', 'healthcare', 'hospital', 'medical', 'drug', 'pharmaceutical',
#     'construction', 'building', 'real estate', 'property', 'housing',
#     'strike', 'shutdown', 'closure', 'disruption', 'operations', 'productivity', 'profitability'
# ]

# # Political Keywords to EXCLUDE (unless they have direct business impact)
# POLITICAL_KEYWORDS_TO_EXCLUDE = [
#     'election', 'campaign', 'political party', 'pdp', 'apc', 'labour party', 'candidate',
#     'governor race', 'senate race', 'political crisis', 'coalition', 'political alliance',
#     'political defection', 'party leadership', 'political rally', 'political meeting'
# ]

# # Nigerian states
# NIGERIAN_STATES = [
#     'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
#     'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
#     'Federal Capital Territory', 'FCT', 'Abuja', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 
#     'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 
#     'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 
#     'Yobe', 'Zamfara'
# ]

# # Business Risk Framework
# BUSINESS_RISK_FACTORS = {
#     "Economic": ["GDP", "Unemployment Rate", "Inflation rate"],
#     "Political": ["Government stability", "Corruption", "Rule of law"],
#     "Technology": ["Digital Infrastructure", "Cybersecurity", "Technology Adoption"],
#     "Social": ["Poverty Rate", "Social unrest", "Education"],
#     "Environmental": ["Air and water quality", "Natural disaster", "Climate change probability"],
#     "Operational": ["Infrastructure Quality", "Supply chain disruption", "Business Continuity"],
#     "Healthcare": ["Healthcare Access", "Disease prevalence", "Healthcare Infrastructure"],
#     "Regulatory and Legal": ["Burden Of Compliance", "Legal Framework", "Enforcement"]
# }

# # Balanced Industry Mapping with Keywords
# INDUSTRY_MAPPING = {
#     "Manufacturing": {
#         "subtypes": ["Factory", "Processing Plant", "Industrial"],
#         "keywords": ["manufacturing", "factory", "production", "industrial", "processing", "plant"]
#     },
#     "Healthcare": {
#         "subtypes": ["Hospitals", "Pharmaceutical"],
#         "keywords": ["hospital", "medical", "healthcare", "pharmaceutical", "drug", "medicine", "clinic"]
#     },
#     "Finance & Banking": {
#         "subtypes": ["Banks", "Insurance", "Financial Services"],
#         "keywords": ["bank", "banking", "finance", "financial", "insurance", "loan", "credit", "investment"]
#     },
#     "Oil & Gas": {
#         "subtypes": ["Upstream", "Downstream"],
#         "keywords": ["oil", "gas", "petroleum", "crude", "refinery", "pipeline", "nnpc", "fuel", "energy"]
#     },
#     "Education": {
#         "subtypes": ["Primary", "Secondary", "Tertiary"],
#         "keywords": ["school", "education", "university", "college", "student", "teacher", "academic"]
#     },
#     "Logistics & Transportation": {
#         "subtypes": ["Logistics", "Transportation", "Shipping"],
#         "keywords": ["transport", "logistics", "shipping", "cargo", "freight", "port", "airport", "railway"]
#     },
#     "Travel & Hospitality": {
#         "subtypes": ["Hotel", "Restaurant", "Tourism"],
#         "keywords": ["hotel", "tourism", "restaurant", "hospitality", "travel", "tourist"]
#     },
#     "Agro-allied": {
#         "subtypes": ["Agriculture", "Food Processing"],
#         "keywords": ["agriculture", "farming", "farm", "crop", "livestock", "agricultural", "food"]
#     },
#     "Telecommunications": {
#         "subtypes": ["Telecom", "Network", "Communication"],
#         "keywords": ["telecommunications", "telecom", "network", "internet", "communication", "mobile"]
#     },
#     "Mining": {
#         "subtypes": ["Mining", "Processing"],
#         "keywords": ["mining", "mineral", "gold", "coal", "tin", "iron ore", "solid minerals"]
#     },
#     "Real Estate & Construction": {
#         "subtypes": ["Construction", "Real Estate"],
#         "keywords": ["construction", "building", "real estate", "property", "housing", "infrastructure"]
#     },
#     "Government & Public Sector": {
#         "subtypes": ["Revenue", "Public Services", "Economic Policy"],
#         "keywords": ["revenue", "government", "public", "policy", "economic", "budget", "taxation"]
#     }
# }

# # Impact Level Mapping
# IMPACT_LEVEL_MAPPING = {
#     1: "Low",
#     2: "Medium", 
#     3: "High",
#     4: "Critical",
#     "Low": 1,
#     "Medium": 2,
#     "High": 3,
#     "Critical": 4
# }

# # ================================
# # 🔹 4. Request Session Setup
# # ================================

# def create_session():
#     """Create a requests session with proper headers and configuration."""
#     session = requests.Session()
#     session.headers.update({
#         'User-Agent': random.choice(USER_AGENTS),
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Accept-Encoding': 'gzip, deflate',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1'
#     })
#     return session

# def make_request_with_retry(session, url, max_retries=3, delay=2):
#     """Make HTTP request with retry mechanism."""
#     for attempt in range(max_retries):
#         try:
#             response = session.get(url, timeout=30)
#             response.raise_for_status()
#             return response
#         except requests.exceptions.RequestException as e:
#             logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
#             if attempt < max_retries - 1:
#                 time.sleep(delay * (attempt + 1))
#             else:
#                 logger.error(f"All retry attempts failed for {url}")
#                 return None
#     return None

# # ================================
# # 🔹 5. Web Scraping Functions
# # ================================

# def get_dailypost_article_links(session, limit=50):
#     """Extract article links from DailyPost pages."""
#     all_links = set()
    
#     for url in DAILYPOST_URLS:
#         try:
#             logger.info(f"Scraping links from: {url}")
#             response = make_request_with_retry(session, url)
            
#             if not response:
#                 continue
                
#             soup = BeautifulSoup(response.content, 'html.parser')
            
#             # DailyPost specific selectors
#             article_links = soup.find_all('a', href=True)
            
#             for link in article_links:
#                 href = link.get('href')
#                 if href:
#                     # Convert relative URLs to absolute
#                     full_url = urljoin(url, href)
                    
#                     # Check if it's a valid DailyPost article URL with date pattern
#                     if 'dailypost.ng' in full_url and re.search(r'/\d{4}/\d{2}/\d{2}/', full_url):
#                         all_links.add(full_url)
                        
#             logger.info(f"Found {len(all_links)} unique links so far")
            
#             # Add delay between requests
#             time.sleep(random.uniform(2, 4))
            
#         except Exception as e:
#             logger.error(f"Error scraping {url}: {e}")
#             continue
    
#     # Limit the number of articles to process
#     limited_links = list(all_links)[:limit]
#     logger.info(f"Selected {len(limited_links)} articles for processing")
#     return limited_links

# def scrape_dailypost_article(session, url):
#     """Scrape individual DailyPost article."""
#     try:
#         response = make_request_with_retry(session, url)
#         if not response:
#             return None
            
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Extract title
#         title_tag = soup.find('h1', class_='entry-title') or soup.find('h1') or soup.find('title')
#         title = title_tag.get_text(strip=True) if title_tag else "No title found"
        
#         # Extract meta description
#         meta_desc = soup.find('meta', {'name': 'description'})
#         description = meta_desc.get('content', '').strip() if meta_desc else "No description found"
        
#         # Extract article content
#         article_text = ""
        
#         # Try different content selectors for DailyPost
#         content_selectors = [
#             {'class': 'entry-content'},
#             {'id': 'mvp-content-main'},
#             {'class': 'post-content'},
#             {'class': 'article-content'},
#             {'class': 'content'}
#         ]
        
#         for selector in content_selectors:
#             content_div = soup.find('div', selector)
#             if content_div:
#                 paragraphs = content_div.find_all('p')
#                 article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
#                 break
        
#         # Fallback: get all paragraphs
#         if not article_text:
#             paragraphs = soup.find_all('p')
#             article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
#         # Basic content validation
#         if len(article_text) < 100:
#             logger.warning(f"Article content too short: {url}")
#             return None
        
#         return {
#             "Title": title,
#             "Description": description,
#             "Content": article_text,
#             "Link": url
#         }
        
#     except Exception as e:
#         logger.error(f"Error scraping article {url}: {e}")
#         return None

# def is_business_relevant(article):
#     """Check if article is relevant to business risks with balanced filtering."""
#     if not article:
#         return False
        
#     content = (article.get("Title", "") + " " + 
#               article.get("Description", "") + " " + 
#               article.get("Content", "")).lower()
    
#     # First check if it's purely political content to exclude
#     political_exclusion_count = sum(1 for keyword in POLITICAL_KEYWORDS_TO_EXCLUDE if keyword in content)
    
#     # If it's heavily political, check if it has business impact
#     if political_exclusion_count >= 2:
#         # Only allow if it has strong business keywords too
#         business_keyword_count = sum(1 for keyword in BUSINESS_KEYWORDS if keyword in content)
#         if business_keyword_count < 3:
#             logger.info("Excluding purely political content with no business impact")
#             return False
    
#     # Check for business keywords
#     keyword_count = sum(1 for keyword in BUSINESS_KEYWORDS if keyword in content)
    
#     # Article is relevant if it contains at least 2 business keywords
#     return keyword_count >= 2

# def validate_industry_content_match(industry, content):
#     """Validate that the industry matches the article content with balanced criteria."""
#     if not industry or industry not in INDUSTRY_MAPPING:
#         return False
    
#     content_lower = content.lower()
#     industry_keywords = INDUSTRY_MAPPING[industry]["keywords"]
    
#     # Check if at least 1 industry-specific keyword is present (more balanced)
#     keyword_matches = sum(1 for keyword in industry_keywords if keyword in content_lower)
    
#     return keyword_matches >= 1

# # ================================
# # 🔹 6. AI Analysis Functions
# # ================================

# BALANCED_BUSINESS_ANALYSIS_PROMPT = """
# You are an expert business risk analyst specializing in Nigerian market conditions. 
# Analyze the following news article and extract business risk information if it has business relevance.

# GUIDELINES:
# 1. Include economic news that affects businesses (GDP, inflation, currency, markets, etc.)
# 2. Include industry-specific operational issues and disruptions
# 3. Include regulatory changes affecting business operations
# 4. Include infrastructure issues affecting business
# 5. Include revenue and taxation news from government agencies
# 6. EXCLUDE pure political party activities, elections, campaigns unless they directly impact business
# 7. If the article discusses economic policies, market conditions, or business operations, include it

# Extract the following information in JSON format:

# 1. **Industry** (Choose most relevant to article content):
#    - Manufacturing (for production, factories, industrial activities)
#    - Healthcare (for medical, pharmaceutical, health services)
#    - Finance & Banking (for financial services, banking, investments)
#    - Oil & Gas (for petroleum, energy, fuel-related content)
#    - Education (for schools, universities, educational services)
#    - Logistics & Transportation (for transport, shipping, ports, logistics)
#    - Travel & Hospitality (for hotels, tourism, restaurants)
#    - Agro-allied (for agriculture, farming, food production)
#    - Telecommunications (for telecom, networks, communications)
#    - Mining (for minerals, mining activities)
#    - Real Estate & Construction (for construction, building, property)
#    - Government & Public Sector (for revenue collection, economic policies, public services)

# 2. **Industry Subtype** (Based on specific content)

# 3. **Business Risk Factor**: Economic, Political, Technology, Social, Environmental, Operational, Healthcare, Regulatory and Legal

# 4. **Risk Indicator**: Specific indicator from the article

# 5. **Impact Type**: Positive or Negative

# 6. **Impact Level**: Low, Medium, High, Critical

# 7. **Event Headline** (Max 20 words): Focus on business/economic impact

# 8. **State**: Nigerian state mentioned (or "Federal" for national issues)
# 9. **City**: Specific city mentioned

# IMPORTANT:
# - If the article is purely about sports, entertainment, or personal matters, return "NO_BUSINESS_RISK"
# - Focus on business and economic relevance rather than strict industry keyword matching
# - If positive impact, use Low level only
# - Use "Federal" as state for national economic/business news

# Return your analysis in JSON format or "NO_BUSINESS_RISK" if not applicable.
# """

# async def analyze_business_article(article):
#     """Use AI to analyze business article with balanced validation."""
#     try:
#         response = await client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": BALANCED_BUSINESS_ANALYSIS_PROMPT},
#                 {"role": "user", "content": f"Title: {article['Title']}\n\nDescription: {article['Description']}\n\nContent: {article['Content'][:4000]}"}
#             ],
#             model="llama3-8b-8192",
#             temperature=0.2,
#             max_tokens=2000
#         )
        
#         extracted_text = response.choices[0].message.content.strip()
        
#         # Check if AI determined no business risk
#         if "NO_BUSINESS_RISK" in extracted_text:
#             logger.info("AI determined no genuine business risk")
#             return None
        
#         # Find JSON content
#         json_match = re.search(r'```(?:json)?(.*?)```', extracted_text, re.DOTALL)
#         if json_match:
#             extracted_text = json_match.group(1).strip()
        
#         # Try to parse JSON
#         try:
#             extracted_data = json.loads(extracted_text)
#         except json.JSONDecodeError:
#             json_start = extracted_text.find('{')
#             json_end = extracted_text.rfind('}') + 1
#             if json_start >= 0 and json_end > json_start:
#                 cleaned_json = extracted_text[json_start:json_end]
#                 try:
#                     extracted_data = json.loads(cleaned_json)
#                 except:
#                     logger.error(f"Failed to parse JSON: {extracted_text}")
#                     return None
#             else:
#                 logger.error(f"Could not find JSON object: {extracted_text}")
#                 return None
        
#         # Balanced validation: Check if industry somewhat matches content
#         industry = extracted_data.get("Industry", "")
#         full_content = article['Title'] + " " + article['Description'] + " " + article['Content']
        
#         # More lenient validation - allow if there's some relevance
#         if industry and industry in INDUSTRY_MAPPING:
#             if not validate_industry_content_match(industry, full_content):
#                 logger.info(f"Industry '{industry}' doesn't strongly match content, but keeping with lower confidence")
#                 # Don't exclude, but note the mismatch
        
#         return extracted_data
    
#     except Exception as e:
#         logger.error(f"Error analyzing business article: {e}")
#         return None

# # ================================
# # 🔹 7. Data Processing Functions
# # ================================

# def extract_location_info(article):
#     """Extract state and city information from article."""
#     content = (article.get("Title", "") + " " + 
#               article.get("Description", "") + " " + 
#               article.get("Content", "")).lower()
    
#     # Extract state
#     state = "Federal"  # Default for national news
#     for state_name in NIGERIAN_STATES:
#         if re.search(r'\b' + re.escape(state_name.lower()) + r'\b', content):
#             if state_name.lower() in ["abuja", "fct"]:
#                 state = "Federal Capital Territory"
#             else:
#                 state = state_name
#             break
    
#     return state, state

# def validate_state(state):
#     """Validate if the extracted state is a valid Nigerian state."""
#     if state == "Federal":  # Allow Federal for national news
#         return True
#     if state == "Unknown" or not state:
#         return False
    
#     # Normalize state name
#     if state.lower() in ["abuja", "fct"]:
#         state = "Federal Capital Territory"
    
#     return state in NIGERIAN_STATES

# def convert_impact_level_to_text(impact_level):
#     """Convert numeric impact level to descriptive text."""
#     if isinstance(impact_level, (int, float)):
#         return IMPACT_LEVEL_MAPPING.get(int(impact_level), "Low")
#     elif isinstance(impact_level, str):
#         if impact_level.title() in ["Low", "Medium", "High", "Critical"]:
#             return impact_level.title()
#         else:
#             try:
#                 return IMPACT_LEVEL_MAPPING.get(int(impact_level), "Low")
#             except ValueError:
#                 return "Low"
#     else:
#         return "Low"

# def create_business_risk_record(article, extracted_data):
#     """Create a business risk record using extracted data."""
#     today = datetime.now()
    
#     state = extracted_data.get("State", "Federal")
#     city = extracted_data.get("City", "")
    
#     # If AI didn't provide location, try to extract it
#     if state in ["Unknown", "N/A", "", None]:
#         state, city = extract_location_info(article)
    
#     # Validate state
#     if not validate_state(state):
#         logger.warning(f"Invalid state '{state}' - using Federal")
#         state = "Federal"
#         city = "Federal"
    
#     # Ensure positive impact is always low level
#     impact_type = extracted_data.get("Impact Type", "Negative")
#     impact_level = extracted_data.get("Impact Level", "Medium")
    
#     impact_level_text = convert_impact_level_to_text(impact_level)
    
#     if impact_type == "Positive" and impact_level_text != "Low":
#         impact_level_text = "Low"
    
#     record = {
#         "Day": today.day,
#         "Month": today.strftime("%b"),
#         "Year": today.year,
#         "Date": today.strftime("%d/%m/%Y"),
#         "State": state,
#         "City": city if city else state,
#         "Industry": extracted_data.get("Industry", ""),
#         "Industry Subtype": extracted_data.get("Industry Subtype", ""),
#         "Business Risk Factor": extracted_data.get("Business Risk Factor", ""),
#         "Risk Indicator": extracted_data.get("Risk Indicator", ""),
#         "Impact Type": impact_type,
#         "Impact Level": impact_level_text,
#         "Event Headline": extracted_data.get("Event Headline", article.get("Title", "")[:100]),
#         "Evidence Source Link": article.get("Link", "")
#     }
    
#     return record

# def validate_business_record(record):
#     """Validate business risk record with balanced criteria."""
#     required_fields = ['Industry', 'Business Risk Factor', 'Impact Type', 'Impact Level']
    
#     for field in required_fields:
#         if not record.get(field) or record[field] == "":
#             return False, f"Missing required field: {field}"
    
#     # Validate Impact Type and Level relationship
#     if record['Impact Type'] == 'Positive' and record['Impact Level'] != 'Low':
#         return False, "Positive impact must have Low impact level"
    
#     # Validate Impact Level options
#     if record['Impact Level'] not in ['Low', 'Medium', 'High', 'Critical']:
#         return False, "Impact Level must be Low, Medium, High, or Critical"
    
#     # More lenient state validation
#     state = record.get('State', '')
#     if not validate_state(state):
#         return False, f"Invalid state: {state}"
    
#     return True, "Valid record"

# # ================================
# # 🔹 8. Email Function
# # ================================

# def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
#     """Send email with business risk data attached."""
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         with open(attachment_path, 'rb') as attachment:
#             part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
#         part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#         msg.attach(part)

#         server = smtplib.SMTP_SSL(smtp_server, smtp_port)
#         server.login(sender_email, smtp_password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())
#         server.quit()
        
#         logger.info(f"Email sent successfully to {receiver_email}")
#     except Exception as e:
#         logger.error(f"Error sending email: {e}")

# # ================================
# # 🔹 9. Main Function
# # ================================

# async def main():
#     """Main function to run the business risk scraper."""
#     logger.info("🚀 Starting Balanced DailyPost Business Risk Scraper...")
    
#     session = create_session()
    
#     try:
#         # Get article links from DailyPost
#         logger.info("📄 Extracting article links from DailyPost...")
#         article_links = get_dailypost_article_links(session, limit=30)
        
#         if not article_links:
#             logger.error("No article links found. Exiting.")
#             return
        
#         # Scrape articles
#         logger.info(f"📖 Scraping {len(article_links)} articles...")
#         articles = []
        
#         for i, url in enumerate(article_links):
#             logger.info(f"Scraping article {i+1}/{len(article_links)}: {url}")
            
#             article = scrape_dailypost_article(session, url)
#             if article and is_business_relevant(article):
#                 articles.append(article)
#                 logger.info(f"✅ Added relevant article: {article['Title'][:60]}...")
#             else:
#                 logger.info("❌ Article not relevant or failed to scrape")
            
#             time.sleep(random.uniform(1, 3))
        
#         logger.info(f"📊 Successfully scraped {len(articles)} relevant business articles")
        
#         if not articles:
#             logger.error("No relevant business articles found. Exiting.")
#             return
        
#         # Process articles with AI analysis
#         logger.info("🤖 Processing articles with balanced AI analysis...")
#         business_risk_records = []
#         processing_log = []
        
#         for i, article in enumerate(articles):
#             try:
#                 logger.info(f"Processing article {i+1}/{len(articles)}: {article['Title'][:60]}...")
                
#                 extracted_data = await analyze_business_article(article)
                
#                 if not extracted_data:
#                     logger.warning("  ❌ No business risk identified - skipping")
#                     processing_log.append({
#                         'title': article['Title'][:100],
#                         'status': 'no_business_risk_identified',
#                         'included': False
#                     })
#                     continue
                
#                 record = create_business_risk_record(article, extracted_data)
                
#                 if not record:
#                     logger.warning("  ❌ Record creation failed")
#                     processing_log.append({
#                         'title': article['Title'][:100],
#                         'status': 'failed_record_creation',
#                         'included': False
#                     })
#                     continue
                
#                 is_valid, validation_message = validate_business_record(record)
#                 if not is_valid:
#                     logger.warning(f"  ❌ Validation failed: {validation_message}")
#                     processing_log.append({
#                         'title': article['Title'][:100],
#                         'status': f'validation_failed_{validation_message}',
#                         'included': False
#                     })
#                     continue
                
#                 business_risk_records.append(record)
                
#                 logger.info(f"  ✅ Record INCLUDED - Industry: {record['Industry']}")
#                 processing_log.append({
#                     'title': article['Title'][:100],
#                     'status': 'included',
#                     'industry': record['Industry'],
#                     'included': True
#                 })
                
#                 await asyncio.sleep(1)  # Rate limiting
                
#             except Exception as e:
#                 logger.error(f"  ❌ Error processing article: {e}")
#                 processing_log.append({
#                     'title': article['Title'][:100],
#                     'status': f'processing_error_{str(e)[:50]}',
#                     'included': False
#                 })
#                 continue
        
#         # Generate summary
#         logger.info(f"\n📊 Processing Summary:")
#         logger.info(f"Total articles processed: {len(articles)}")
#         logger.info(f"Records created: {len(business_risk_records)}")
#         logger.info(f"Success rate: {(len(business_risk_records) / len(articles) * 100):.1f}%")
        
#         # Save processing log
#         if processing_log:
#             processing_df = pd.DataFrame(processing_log)
#             processing_filename = f'processing_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
#             processing_df.to_csv(processing_filename, index=False)
#             logger.info(f"Processing log saved to {processing_filename}")
        
#         # Save business risk data
#         if business_risk_records:
#             df = pd.DataFrame(business_risk_records)
            
#             impact_order = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
#             df['Impact_Sort'] = df['Impact Level'].map(impact_order)
#             df = df.sort_values(['Impact_Sort', 'Industry'], ascending=[False, True])
#             df = df.drop('Impact_Sort', axis=1)
            
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f'business_risk_data_{timestamp}.csv'
#             df.to_csv(filename, index=False)
#             logger.info(f"Business risk data saved to {filename}")
            
#             # Display summary statistics
#             logger.info("\n📈 Business Risk Data Summary:")
#             logger.info(f"Total Records: {len(df)}")
#             logger.info(f"Industries Covered: {df['Industry'].nunique()}")
#             logger.info(f"States Covered: {df['State'].nunique()}")
            
#             logger.info("\n🏭 Industries with Risk Events:")
#             industry_counts = df['Industry'].value_counts()
#             for industry, count in industry_counts.items():
#                 logger.info(f"  {industry}: {count} events")
            
#             logger.info("\n🌍 States with Risk Events:")
#             state_counts = df['State'].value_counts().head(5)
#             for state, count in state_counts.items():
#                 logger.info(f"  {state}: {count} events")
            
#             logger.info("\n📊 Impact Level Distribution:")
#             impact_counts = df['Impact Level'].value_counts()
#             for level, count in impact_counts.items():
#                 logger.info(f"  {level}: {count} events")
            
#             logger.info("\n🔍 Risk Factor Distribution:")
#             risk_factor_counts = df['Business Risk Factor'].value_counts()
#             for factor, count in risk_factor_counts.items():
#                 logger.info(f"  {factor}: {count} events")
            
#             # Send email if credentials are provided
#             sender_email = os.environ.get('USER_EMAIL')
#             sender_password = os.environ.get('USER_PASSWORD')
            
#             if sender_email and sender_password:
#                 try:
#                     send_email(
#                         sender_email=sender_email,
#                         receiver_email="riskcontrolservicesnig@gmail.com",
#                         subject="Balanced Business Risk Intelligence Report - DailyPost",
#                         body=f"""Balanced Business Risk Intelligence Report - DailyPost

# 🔍 PROCESSING SUMMARY:
# - Articles Processed: {len(articles)}
# - Business Risk Records Generated: {len(df)}
# - Success Rate: {(len(business_risk_records) / len(articles) * 100):.1f}%
# - Balanced Validation Applied: ✅
# - Political Content Filtering: ✅

# 📊 BUSINESS INTELLIGENCE OVERVIEW:
# - Total Risk Events: {len(df)}
# - Industries Monitored: {df['Industry'].nunique()}
# - States with Business Risks: {df['State'].nunique()}
# - Critical/High Impact Events: {len(df[df['Impact Level'].isin(['Critical', 'High'])])}

# 🎯 TOP RISK INSIGHTS:
# - Primary Industry at Risk: {df['Industry'].value_counts().index[0] if len(df) > 0 else 'N/A'}
# - Primary Risk Factor: {df['Business Risk Factor'].value_counts().index[0] if len(df) > 0 else 'N/A'}
# - Most Affected State: {df['State'].value_counts().index[0] if len(df) > 0 else 'N/A'}

# 🏭 INDUSTRY DISTRIBUTION:
# {chr(10).join([f"- {industry}: {count} events" for industry, count in df['Industry'].value_counts().items()])}

# 📈 IMPACT DISTRIBUTION:
# {chr(10).join([f"- {level}: {count} events" for level, count in df['Impact Level'].value_counts().items()])}

# 🔧 IMPROVEMENTS IMPLEMENTED:
# - Removed verification and confidence columns
# - Balanced industry validation (not overly strict)
# - Added "Government & Public Sector" for revenue/policy news
# - Allow "Federal" state for national economic news
# - Focus on business relevance over strict keyword matching
# - Enhanced political content filtering

# 📋 ATTACHED FILES:
# 1. {filename} - Business risk dataset (clean format)
# 2. {processing_filename} - Processing log with inclusion/exclusion details

# This report provides business-relevant risk intelligence from Nigerian news sources.

# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# """,
#                         attachment_path=filename,
#                         smtp_server="smtp.gmail.com",
#                         smtp_port=465,
#                         smtp_password=sender_password
#                     )
#                 except Exception as e:
#                     logger.error(f"Failed to send email: {e}")
#             else:
#                 logger.info("Email credentials not provided - skipping email send")
            
#             logger.info("✅ Balanced business risk processing completed successfully!")
            
#             # Display sample records for verification
#             logger.info("\n🔍 Sample Business Risk Records:")
#             for i, record in enumerate(df.head(3).to_dict('records')):
#                 logger.info(f"\nRecord {i+1}:")
#                 logger.info(f"  Industry: {record['Industry']}")
#                 logger.info(f"  Event: {record['Event Headline']}")
#                 logger.info(f"  Risk Factor: {record['Business Risk Factor']}")
#                 logger.info(f"  Impact Level: {record['Impact Level']}")
#                 logger.info(f"  State: {record['State']}")
#                 logger.info(f"  Link: {record['Evidence Source Link']}")
#         else:
#             logger.warning("❌ No business risk records were generated.")
    
#     except Exception as e:
#         logger.error(f"❌ Error in main processing: {e}")
#         raise

# # ================================
# # 🔹 10. Script Execution
# # ================================

# if __name__ == "__main__":
#     print("🚀 Starting Balanced DailyPost Business Risk Scraper...")
#     print("🔧 Features: Balanced validation, economic focus, political filtering")
#     print("📊 Target: Business and economic news with industry relevance")
#     print("🎯 Goal: Generate actionable business risk intelligence")
#     print("=" * 70)
    
#     asyncio.run(main())

import os
import random
import time
import asyncio
import pandas as pd
import re
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import requests
from bs4 import BeautifulSoup
from groq import AsyncGroq
import google.generativeai as genai
import json
from urllib.parse import urljoin, urlparse
import logging

# ================================
# 🔹 1. Setup Logging
# ================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ================================
# 🔹 2. Initialize APIs
# ================================

# Initialize Groq API Client
client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY", "your_groq_api_key_here"))

# Initialize Gemini API Client
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# ================================
# 🔹 3. Constants and Configuration
# ================================

# User-Agent Rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
]

# DailyPost specific URLs
DAILYPOST_URLS = [
    "https://dailypost.ng/category/business/",
    "https://dailypost.ng/category/economy/",
    "https://dailypost.ng/"
]

# Strict Business Keywords for filtering
BUSINESS_KEYWORDS = [
    'gdp', 'inflation', 'unemployment', 'economic growth', 'recession', 'naira', 'dollar', 'forex',
    'interest rate', 'monetary policy', 'fiscal policy', 'budget', 'revenue', 'tax', 'taxation',
    'business', 'company', 'industry', 'factory', 'manufacturing', 'production', 'supply chain', 'logistics',
    'import', 'export', 'trade', 'commerce', 'investment', 'investor', 'market', 'price', 'cost',
    'infrastructure', 'port', 'airport', 'road', 'railway', 'power', 'electricity', 'fuel', 'energy',
    'telecommunications', 'banking', 'finance', 'insurance', 'loan', 'credit',
    'oil', 'gas', 'petroleum', 'pipeline', 'refinery', 'crude', 'nnpc', 'upstream', 'downstream',
    'agriculture', 'farming', 'crop', 'livestock', 'food', 'harvest',
    'mining', 'solid minerals', 'healthcare', 'hospital', 'medical', 'drug', 'pharmaceutical',
    'construction', 'building', 'real estate', 'property', 'housing',
    'strike affecting business', 'factory closure', 'plant shutdown', 'supply disruption',
    'regulatory compliance', 'business license', 'operations', 'productivity', 'profitability'
]

# Political Keywords to EXCLUDE (unless they have direct business impact)
POLITICAL_KEYWORDS_TO_EXCLUDE = [
    'election', 'campaign', 'political party', 'pdp', 'apc', 'labour party', 'candidate',
    'governor race', 'senate race', 'political crisis', 'coalition', 'political alliance',
    'political defection', 'party leadership', 'political rally', 'political meeting'
]

# Nigerian states
NIGERIAN_STATES = [
    'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
    'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
    'Federal Capital Territory', 'FCT', 'Abuja', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 
    'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 
    'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 
    'Yobe', 'Zamfara'
]

# Event Categories - Strict validation
EVENT_CATEGORIES = [
    "Economic", "Political", "Technology", "Social", "Environmental", 
    "Operational", "Healthcare", "Regulatory and Legal"
]

# Industry Mapping with Subtypes and Risk Types
INDUSTRY_MAPPING = {
    "Manufacturing": {
        "subtypes": ["Factory", "Warehouse", "Supermarket"],
        "risk_types": ["Supply Chain Disruption", "Forex/Import Policy", "Labour Unrest", "Insecurity", "Energy Costs"],
        "keywords": ["factory", "manufacturing", "production", "plant", "assembly", "industrial", "processing", "warehouse", "supermarket"]
    },
    "Healthcare": {
        "subtypes": ["Hospitals", "Pharmaceutical"],
        "risk_types": ["Drug Supply Shortages", "Regulatory Changes", "Security Risks (Kidnapping/Attacks)", "Workforce Shortage", "Counterfeiting"],
        "keywords": ["hospital", "medical", "healthcare", "pharmaceutical", "drug", "medicine", "clinic", "health"]
    },
    "Finance & Banking": {
        "subtypes": ["Banks", "Insurance", "Mortgage", "Microfinance"],
        "risk_types": ["Cybersecurity Threats", "Regulatory Policy Shifts", "Economic Instability", "Naira Volatility", "Fraud Trends"],
        "keywords": ["bank", "banking", "finance", "financial", "insurance", "loan", "credit", "mortgage", "microfinance"]
    },
    "Oil & Gas": {
        "subtypes": ["Upstream", "Downstream"],
        "risk_types": ["Pipeline Vandalism", "Community Unrest", "Regulatory Compliance", "Environmental Incidents", "Militant Activity"],
        "keywords": ["oil", "gas", "petroleum", "crude", "refinery", "pipeline", "nnpc", "upstream", "downstream", "fuel"]
    },
    "Education": {
        "subtypes": ["Primary", "Secondary", "Tertiary"],
        "risk_types": ["Student Protests", "Terrorism/Insecurity", "Infrastructure Vandalism", "Regulatory Shifts", "Tuition Policy Changes"],
        "keywords": ["school", "education", "university", "college", "student", "teacher", "academic", "classroom"]
    },
    "Logistics & Transportation": {
        "subtypes": ["Logistics", "Transportation (Land)", "Aviation (Air)", "Maritime (Sea)"],
        "risk_types": ["Road Infrastructure Quality", "Port Congestion", "Fuel Price Volatility", "Cargo Theft/Banditry", "Regulatory Permits", "Insecurity"],
        "keywords": ["transport", "logistics", "shipping", "cargo", "freight", "port", "airport", "railway", "aviation", "maritime"]
    },
    "Travel & Hospitality": {
        "subtypes": ["Hotel", "Nightclub", "Bar", "Restaurant"],
        "risk_types": ["Insecurity (Kidnapping/Terrorism)", "Health Epidemics", "Currency Volatility", "Regulatory Shifts (Tourism Policies)", "Labour Strikes"],
        "keywords": ["hotel", "tourism", "restaurant", "hospitality", "travel", "tourist", "accommodation", "nightclub", "bar"]
    },
    "Agro-allied": {
        "subtypes": ["Farm", "Storage", "Livestock"],
        "risk_types": ["Climate Risks", "Banditry & Herdsmen Attacks", "Market Price Volatility", "Supply Chain Blockages", "Land Use Policy", "Input Costs"],
        "keywords": ["agriculture", "farming", "farm", "crop", "livestock", "agricultural", "harvest", "food production", "storage"]
    },
    "Telecommunications": {
        "subtypes": ["Telcomm", "Cloud", "Network"],
        "risk_types": ["Vandalism of Infrastructure", "Regulatory Compliance (NCC)", "Cybersecurity Threats", "Power Supply Disruption", "Taxation Changes"],
        "keywords": ["telecommunications", "telecom", "network", "internet", "communication", "mobile", "broadband", "cloud"]
    },
    "Mining": {
        "subtypes": ["Mining", "Processing"],
        "risk_types": ["Community Unrest", "Illegal Mining Activities", "Environmental Regulations", "Insecurity (Banditry/Terrorism)", "Licensing Delays"],
        "keywords": ["mining", "mineral", "gold", "coal", "tin", "iron ore", "solid minerals", "extraction", "processing"]
    },
    "Real Estate & Construction": {
        "subtypes": ["Construction", "Real estate"],
        "risk_types": ["Policy Shifts (Land Use Act)", "Material Cost Volatility", "Regulatory Approvals Delays", "Insecurity (Site Theft/Kidnap)", "Infrastructure Quality"],
        "keywords": ["construction", "building", "real estate", "property", "housing", "infrastructure", "contractor"]
    }
}

# Impact Level Mapping
IMPACT_LEVEL_MAPPING = {
    1: "Low",
    2: "Medium", 
    3: "High",
    4: "Critical",
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4
}

# ================================
# 🔹 4. Request Session Setup
# ================================

def create_session():
    """Create a requests session with proper headers and configuration."""
    session = requests.Session()
    session.headers.update({
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    return session

def make_request_with_retry(session, url, max_retries=3, delay=2):
    """Make HTTP request with retry mechanism."""
    for attempt in range(max_retries):
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                logger.error(f"All retry attempts failed for {url}")
                return None
    return None

# ================================
# 🔹 5. Web Scraping Functions
# ================================

def get_dailypost_article_links(session, limit=50):
    """Extract article links from DailyPost pages."""
    all_links = set()
    
    for url in DAILYPOST_URLS:
        try:
            logger.info(f"Scraping links from: {url}")
            response = make_request_with_retry(session, url)
            
            if not response:
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # DailyPost specific selectors
            article_links = soup.find_all('a', href=True)
            
            for link in article_links:
                href = link.get('href')
                if href:
                    # Convert relative URLs to absolute
                    full_url = urljoin(url, href)
                    
                    # Check if it's a valid DailyPost article URL with date pattern
                    if 'dailypost.ng' in full_url and re.search(r'/\d{4}/\d{2}/\d{2}/', full_url):
                        all_links.add(full_url)
                        
            logger.info(f"Found {len(all_links)} unique links so far")
            
            # Add delay between requests
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            continue
    
    # Limit the number of articles to process
    limited_links = list(all_links)[:limit]
    logger.info(f"Selected {len(limited_links)} articles for processing")
    return limited_links

def scrape_dailypost_article(session, url):
    """Scrape individual DailyPost article."""
    try:
        response = make_request_with_retry(session, url)
        if not response:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('h1', class_='entry-title') or soup.find('h1') or soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        
        # Extract meta description
        meta_desc = soup.find('meta', {'name': 'description'})
        description = meta_desc.get('content', '').strip() if meta_desc else "No description found"
        
        # Extract article content
        article_text = ""
        
        # Try different content selectors for DailyPost
        content_selectors = [
            {'class': 'entry-content'},
            {'id': 'mvp-content-main'},
            {'class': 'post-content'},
            {'class': 'article-content'},
            {'class': 'content'}
        ]
        
        for selector in content_selectors:
            content_div = soup.find('div', selector)
            if content_div:
                paragraphs = content_div.find_all('p')
                article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                break
        
        # Fallback: get all paragraphs
        if not article_text:
            paragraphs = soup.find_all('p')
            article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
        # Basic content validation
        if len(article_text) < 100:
            logger.warning(f"Article content too short: {url}")
            return None
        
        return {
            "Title": title,
            "Description": description,
            "Content": article_text,
            "Link": url
        }
        
    except Exception as e:
        logger.error(f"Error scraping article {url}: {e}")
        return None

def is_business_relevant(article):
    """Check if article is relevant to business risks with strict filtering."""
    if not article:
        return False
        
    content = (article.get("Title", "") + " " + 
              article.get("Description", "") + " " + 
              article.get("Content", "")).lower()
    
    # First check if it's purely political content to exclude
    political_exclusion_count = sum(1 for keyword in POLITICAL_KEYWORDS_TO_EXCLUDE if keyword in content)
    
    # If it's heavily political, check if it has business impact
    if political_exclusion_count >= 2:
        # Only allow if it has strong business keywords too
        business_keyword_count = sum(1 for keyword in BUSINESS_KEYWORDS if keyword in content)
        if business_keyword_count < 3:
            logger.info("Excluding purely political content with no business impact")
            return False
    
    # Check for business keywords
    keyword_count = sum(1 for keyword in BUSINESS_KEYWORDS if keyword in content)
    
    # Article is relevant if it contains at least 2 business keywords
    return keyword_count >= 2

def validate_industry_content_match(industry, content):
    """Validate that the industry actually matches the article content."""
    if not industry or industry not in INDUSTRY_MAPPING:
        return False
    
    content_lower = content.lower()
    industry_keywords = INDUSTRY_MAPPING[industry]["keywords"]
    
    # Check if at least 2 industry-specific keywords are present
    keyword_matches = sum(1 for keyword in industry_keywords if keyword in content_lower)
    
    return keyword_matches >= 2

def determine_industry_subtype(industry, content):
    """Determine appropriate industry subtype based on content."""
    if not industry or industry not in INDUSTRY_MAPPING:
        return ""
    
    content_lower = content.lower()
    subtypes = INDUSTRY_MAPPING[industry]["subtypes"]
    
    # Simple keyword matching for subtypes
    for subtype in subtypes:
        if subtype.lower() in content_lower:
            return subtype
    
    # Return first subtype as default
    return subtypes[0] if subtypes else ""

def determine_industry_risk_type(industry, content):
    """Determine appropriate industry risk type based on content."""
    if not industry or industry not in INDUSTRY_MAPPING:
        return ""
    
    content_lower = content.lower()
    risk_types = INDUSTRY_MAPPING[industry]["risk_types"]
    
    # Keyword matching for risk types
    risk_keywords = {
        "Supply Chain Disruption": ["supply chain", "disruption", "shortage", "delay"],
        "Forex/Import Policy": ["forex", "import", "policy", "exchange rate"],
        "Labour Unrest": ["strike", "protest", "worker", "union", "labour"],
        "Insecurity": ["security", "kidnap", "attack", "violence", "theft"],
        "Energy Costs": ["power", "electricity", "fuel", "energy", "cost"],
        "Drug Supply Shortages": ["drug", "shortage", "medicine", "pharmaceutical"],
        "Regulatory Changes": ["regulation", "policy", "law", "compliance"],
        "Cybersecurity Threats": ["cyber", "hack", "digital", "security"],
        "Pipeline Vandalism": ["pipeline", "vandalism", "damage", "sabotage"],
        "Community Unrest": ["community", "protest", "unrest", "violence"],
        "Student Protests": ["student", "protest", "university", "school"],
        "Infrastructure Vandalism": ["infrastructure", "vandalism", "damage"],
        "Road Infrastructure Quality": ["road", "infrastructure", "transport"],
        "Port Congestion": ["port", "congestion", "delay", "shipping"],
        "Climate Risks": ["climate", "weather", "rain", "drought", "flood"],
        "Banditry & Herdsmen Attacks": ["bandit", "herdsmen", "attack", "farmer"],
        "Vandalism of Infrastructure": ["vandalism", "infrastructure", "damage"],
        "Illegal Mining Activities": ["illegal", "mining", "unauthorized"],
        "Policy Shifts": ["policy", "law", "regulation", "government"]
    }
    
    # Score each risk type based on keyword matches
    risk_scores = {}
    for risk_type in risk_types:
        if risk_type in risk_keywords:
            score = sum(1 for keyword in risk_keywords[risk_type] if keyword in content_lower)
            risk_scores[risk_type] = score
    
    # Return the risk type with highest score
    if risk_scores:
        return max(risk_scores, key=risk_scores.get)
    
    # Return first risk type as default
    return risk_types[0] if risk_types else ""

# ================================
# 🔹 6. AI Analysis Functions
# ================================

STRICT_BUSINESS_ANALYSIS_PROMPT = """
You are an expert business risk analyst specializing in Nigerian market conditions. 
Analyze the following news article and extract business risk information ONLY if it has DIRECT business impact.

CRITICAL RULES:
1. DO NOT classify political news as business risks unless they have DIRECT impact on business operations
2. Political party activities, elections, campaigns, and leadership changes are NOT business risks
3. Only include if the article discusses specific business impacts like:
   - Factory closures or operational disruptions
   - Supply chain disruptions
   - Regulatory changes affecting business operations
   - Economic indicators affecting business
   - Industry-specific operational issues
   - Infrastructure problems affecting business operations

4. The INDUSTRY must be directly mentioned or clearly implied in the article content
5. If you cannot find a clear industry connection, return "NO_BUSINESS_RISK"

Extract the following information in JSON format ONLY if genuine business risk:

1. **Industry** (Must be directly related to article content - choose ONLY ONE):
   - Manufacturing
   - Healthcare
   - Finance & Banking
   - Oil & Gas
   - Education
   - Logistics & Transportation
   - Travel & Hospitality
   - Agro-allied
   - Telecommunications
   - Mining
   - Real Estate & Construction

2. **Event Category** (choose ONLY ONE):
   - Economic
   - Political
   - Technology
   - Social
   - Environmental
   - Operational
   - Healthcare
   - Regulatory and Legal

3. **Impact Type**: Positive or Negative

4. **Impact Level**: 
   - If Impact Type is "Positive": ALWAYS use "Low"
   - If Impact Type is "Negative": Choose from Low, Medium, High, Critical based on:
     * Low: No known threat, unverified report, non-violent protest, minor regulatory update
     * Medium: Notification of strike, major delay, policy change, localized violent threat
     * High: Confirmed major disruption, security incident, policy changes, health/environmental disasters
     * Critical: Shutdowns, attacks, policy crisis with national impact

5. **Event Headline** (Max 20 words): Focus on business impact, not political aspects

6. **State**: Nigerian state mentioned in the article
7. **City**: Specific city or location mentioned

8. **Analyst Comments**: Optional insights, predictions, or related alerts about the news (max 100 words)

IMPORTANT:
- If the article is primarily about politics without clear business impact, return "NO_BUSINESS_RISK"
- If you cannot find specific industry keywords in the content, return "NO_BUSINESS_RISK"
- The industry must be explicitly supported by content keywords
- Event Category must be one of the 8 specified categories
- Impact Type must be either "Positive" or "Negative"
- Positive impacts are ALWAYS Low level

Return your analysis in JSON format or "NO_BUSINESS_RISK" if not applicable.
"""

async def analyze_business_article(article):
    """Use AI to analyze business article and extract risk information with strict validation."""
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": STRICT_BUSINESS_ANALYSIS_PROMPT},
                {"role": "user", "content": f"Title: {article['Title']}\n\nDescription: {article['Description']}\n\nContent: {article['Content'][:4000]}"}
            ],
            model="llama3-8b-8192",
            temperature=0.1,  # Lower temperature for more consistent results
            max_tokens=2000
        )
        
        extracted_text = response.choices[0].message.content.strip()
        
        # Check if AI determined no business risk
        if "NO_BUSINESS_RISK" in extracted_text:
            logger.info("AI determined no genuine business risk")
            return None
        
        # Find JSON content
        json_match = re.search(r'```(?:json)?(.*?)```', extracted_text, re.DOTALL)
        if json_match:
            extracted_text = json_match.group(1).strip()
        
        # Try to parse JSON
        try:
            extracted_data = json.loads(extracted_text)
        except json.JSONDecodeError:
            json_start = extracted_text.find('{')
            json_end = extracted_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                cleaned_json = extracted_text[json_start:json_end]
                try:
                    extracted_data = json.loads(cleaned_json)
                except:
                    logger.error(f"Failed to parse JSON: {extracted_text}")
                    return None
            else:
                logger.error(f"Could not find JSON object: {extracted_text}")
                return None
        
        # Additional validation: Check if industry matches content
        industry = extracted_data.get("Industry", "")
        full_content = article['Title'] + " " + article['Description'] + " " + article['Content']
        
        if not validate_industry_content_match(industry, full_content):
            logger.info(f"Industry '{industry}' doesn't match article content - excluding")
            return None
        
        # Validate Event Category
        event_category = extracted_data.get("Event Category", "")
        if event_category not in EVENT_CATEGORIES:
            logger.info(f"Invalid Event Category '{event_category}' - excluding")
            return None
        
        return extracted_data
    
    except Exception as e:
        logger.error(f"Error analyzing business article: {e}")
        return None

# ================================
# 🔹 7. Data Processing Functions
# ================================

def extract_location_info(article):
    """Extract state and city information from article."""
    content = (article.get("Title", "") + " " + 
              article.get("Description", "") + " " + 
              article.get("Content", "")).lower()
    
    # Extract state
    state = "Unknown"
    for state_name in NIGERIAN_STATES:
        if re.search(r'\b' + re.escape(state_name.lower()) + r'\b', content):
            if state_name.lower() in ["abuja", "fct"]:
                state = "Federal Capital Territory"
            else:
                state = state_name
            break
    
    return state, state  # Use state as city for simplicity

def validate_state(state):
    """Validate if the extracted state is a valid Nigerian state."""
    if state == "Unknown" or not state:
        return False
    
    # Normalize state name
    if state.lower() in ["abuja", "fct"]:
        state = "Federal Capital Territory"
    
    return state in NIGERIAN_STATES

def convert_impact_level_to_text(impact_level):
    """Convert numeric impact level to descriptive text."""
    if isinstance(impact_level, (int, float)):
        return IMPACT_LEVEL_MAPPING.get(int(impact_level), "Low")
    elif isinstance(impact_level, str):
        # If it's already text, validate and return
        if impact_level.title() in ["Low", "Medium", "High", "Critical"]:
            return impact_level.title()
        else:
            # Try to convert if it's a number in string form
            try:
                return IMPACT_LEVEL_MAPPING.get(int(impact_level), "Low")
            except ValueError:
                return "Low"
    else:
        return "Low"

def create_business_risk_record(article, extracted_data):
    """Create a business risk record using extracted data."""
    # Get current date
    today = datetime.now()
    
    # Use extracted data
    state = extracted_data.get("State", "Unknown")
    city = extracted_data.get("City", "Unknown")
    
    # If AI didn't provide location, try to extract it
    if state == "Unknown" or not state:
        state, city = extract_location_info(article)
    
    # Validate state - if unknown, return None to exclude this record
    if not validate_state(state):
        logger.warning(f"Invalid or unknown state '{state}' - excluding record")
        return None
    
    # Get industry information
    industry = extracted_data.get("Industry", "")
    full_content = article['Title'] + " " + article['Description'] + " " + article['Content']
    
    # Determine industry subtype and risk type
    industry_subtype = determine_industry_subtype(industry, full_content)
    industry_risk_type = determine_industry_risk_type(industry, full_content)
    
    # Ensure positive impact is always low level
    impact_type = extracted_data.get("Impact Type", "Negative")
    impact_level = extracted_data.get("Impact Level", "Medium")
    
    # Convert impact level to text format
    impact_level_text = convert_impact_level_to_text(impact_level)
    
    # Force positive impact to be low level
    if impact_type == "Positive":
        impact_level_text = "Low"
    
    # Create record with new column arrangement
    record = {
        "Day": today.day,
        "Month": today.strftime("%b"),
        "Year": today.year,
        "Date": today.strftime("%d/%m/%Y"),
        "State": state,
        "City": city,
        "Industry": industry,
        "Industry Subtype": industry_subtype,
        "Industry Risk Type": industry_risk_type,
        "Event Category": extracted_data.get("Event Category", ""),
        "Impact Type": impact_type,
        "Impact Level": impact_level_text,
        "Event Headline": extracted_data.get("Event Headline", article.get("Title", "")[:100]),
        "Evidence Source Link": article.get("Link", ""),
        "Analyst Comments": extracted_data.get("Analyst Comments", "")
    }
    
    return record

def validate_business_record(record):
    """Validate business risk record for completeness and accuracy."""
    required_fields = ['Industry', 'Event Category', 'Impact Type', 'Impact Level']
    
    for field in required_fields:
        if not record.get(field) or record[field] == "":
            return False, f"Missing required field: {field}"
    
    # Validate Event Category
    if record.get('Event Category', '') not in EVENT_CATEGORIES:
        return False, f"Invalid Event Category: {record.get('Event Category', '')}"
    
    # Validate Impact Type and Level relationship
    if record['Impact Type'] == 'Positive' and record['Impact Level'] != 'Low':
        return False, "Positive impact must have Low impact level"
    
    # Validate Impact Level options
    if record['Impact Level'] not in ['Low', 'Medium', 'High', 'Critical']:
        return False, "Impact Level must be Low, Medium, High, or Critical"
    
    # Validate state
    if not validate_state(record.get('State', '')):
        return False, "Invalid or unknown state"
    
    # Validate industry is in our mapping
    if record.get('Industry', '') not in INDUSTRY_MAPPING:
        return False, f"Invalid industry: {record.get('Industry', '')}"
    
    return True, "Valid record"

# ================================
# 🔹 8. Email Function
# ================================

def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
    """Send email with business risk data attached."""
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        
        logger.info(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")

# ================================
# 🔹 9. Main Function
# ================================

async def main():
    """Main function to run the business risk scraper."""
    logger.info("🚀 Starting DailyPost Business Risk Scraper with Updated Structure...")
    
    # Create session
    session = create_session()
    
    try:
        # Get article links from DailyPost
        logger.info("📄 Extracting article links from DailyPost...")
        article_links = get_dailypost_article_links(session, limit=30)
        
        if not article_links:
            logger.error("No article links found. Exiting.")
            return
        
        # Scrape articles
        logger.info(f"📖 Scraping {len(article_links)} articles...")
        articles = []
        
        for i, url in enumerate(article_links):
            logger.info(f"Scraping article {i+1}/{len(article_links)}: {url}")
            
            article = scrape_dailypost_article(session, url)
            if article and is_business_relevant(article):
                articles.append(article)
                logger.info(f"✅ Added relevant article: {article['Title'][:60]}...")
            else:
                logger.info("❌ Article not relevant or failed to scrape")
            
            # Rate limiting
            time.sleep(random.uniform(1, 3))
        
        logger.info(f"📊 Successfully scraped {len(articles)} relevant business articles")
        
        if not articles:
            logger.error("No relevant business articles found. Exiting.")
            return
        
        # Process articles with AI analysis
        logger.info("🤖 Processing articles with updated AI analysis...")
        business_risk_records = []
        processing_log = []
        
        for i, article in enumerate(articles):
            try:
                logger.info(f"Processing article {i+1}/{len(articles)}: {article['Title'][:60]}...")
                
                # AI analysis with strict validation
                logger.info("  🔍 Performing updated AI analysis...")
                extracted_data = await analyze_business_article(article)
                
                if not extracted_data:
                    logger.warning("  ❌ AI analysis failed or no business risk identified - skipping")
                    processing_log.append({
                        'title': article['Title'][:100],
                        'status': 'no_business_risk_identified',
                        'included': False
                    })
                    continue
                
                # Create record
                logger.info("  📝 Creating business risk record...")
                record = create_business_risk_record(article, extracted_data)
                
                if not record:
                    logger.warning("  ❌ Record creation failed")
                    processing_log.append({
                        'title': article['Title'][:100],
                        'status': 'failed_record_creation',
                        'included': False
                    })
                    continue
                
                # Validate record
                is_valid, validation_message = validate_business_record(record)
                if not is_valid:
                    logger.warning(f"  ❌ Validation failed: {validation_message}")
                    processing_log.append({
                        'title': article['Title'][:100],
                        'status': f'validation_failed_{validation_message}',
                        'included': False
                    })
                    continue
                
                # Add record to final list
                business_risk_records.append(record)
                
                logger.info(f"  ✅ Record INCLUDED - Industry: {record['Industry']}, Category: {record['Event Category']}")
                processing_log.append({
                    'title': article['Title'][:100],
                    'status': 'included',
                    'industry': record['Industry'],
                    'event_category': record['Event Category'],
                    'included': True
                })
                
                # Add delay between API calls
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"  ❌ Error processing article: {e}")
                processing_log.append({
                    'title': article['Title'][:100],
                    'status': f'processing_error_{str(e)[:50]}',
                    'included': False
                })
                continue
        
        # Generate summary
        logger.info(f"\n📊 Processing Summary:")
        logger.info(f"Total articles processed: {len(articles)}")
        logger.info(f"Records created: {len(business_risk_records)}")
        logger.info(f"Success rate: {(len(business_risk_records) / len(articles) * 100):.1f}%")
        
        # Save processing log
        if processing_log:
            processing_df = pd.DataFrame(processing_log)
            processing_filename = f'processing_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            processing_df.to_csv(processing_filename, index=False)
            logger.info(f"Processing log saved to {processing_filename}")
        
        # Save business risk data
        if business_risk_records:
            df = pd.DataFrame(business_risk_records)
            
            # Sort by impact level and industry
            impact_order = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
            df['Impact_Sort'] = df['Impact Level'].map(impact_order)
            df = df.sort_values(['Impact_Sort', 'Industry'], ascending=[False, True])
            df = df.drop('Impact_Sort', axis=1)
            
            # Save to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'business_risk_data_{timestamp}.csv'
            df.to_csv(filename, index=False)
            logger.info(f"Business risk data saved to {filename}")
            
            # Display summary statistics
            logger.info("\n📈 Business Risk Data Summary:")
            logger.info(f"Total Records: {len(df)}")
            logger.info(f"Industries Covered: {df['Industry'].nunique()}")
            logger.info(f"States Covered: {df['State'].nunique()}")
            logger.info(f"Event Categories: {df['Event Category'].nunique()}")
            
            logger.info("\n🏭 Industries with Risk Events:")
            industry_counts = df['Industry'].value_counts()
            for industry, count in industry_counts.items():
                logger.info(f"  {industry}: {count} events")
            
            logger.info("\n🌍 States with Risk Events:")
            state_counts = df['State'].value_counts().head(5)
            for state, count in state_counts.items():
                logger.info(f"  {state}: {count} events")
            
            logger.info("\n📊 Impact Level Distribution:")
            impact_counts = df['Impact Level'].value_counts()
            for level, count in impact_counts.items():
                logger.info(f"  {level}: {count} events")
            
            logger.info("\n🔍 Event Category Distribution:")
            event_category_counts = df['Event Category'].value_counts()
            for category, count in event_category_counts.items():
                logger.info(f"  {category}: {count} events")
            
            # Send email if credentials are provided
            sender_email = os.environ.get('USER_EMAIL')
            sender_password = os.environ.get('USER_PASSWORD')
            
            if sender_email and sender_password:
                try:
                    send_email(
                        sender_email=sender_email,
                        receiver_email="riskcontrolservicesnig@gmail.com",
                        subject="Updated Business Risk Intelligence Report - DailyPost",
                        body=f"""Updated Business Risk Intelligence Report - DailyPost

🔍 UPDATED QUALITY ASSURANCE SUMMARY:
- Articles Processed: {len(articles)}
- Business Risk Records Generated: {len(df)}
- Success Rate: {(len(business_risk_records) / len(articles) * 100):.1f}%
- Updated Column Structure Applied: ✅
- Event Category Validation: ✅
- Industry Risk Type Mapping: ✅

📊 BUSINESS INTELLIGENCE OVERVIEW:
- Total Risk Events: {len(df)}
- Industries Monitored: {df['Industry'].nunique()}
- States with Business Risks: {df['State'].nunique()}
- Event Categories: {df['Event Category'].nunique()}
- Critical/High Impact Events: {len(df[df['Impact Level'].isin(['Critical', 'High'])])}

🎯 TOP RISK INSIGHTS:
- Primary Industry at Risk: {df['Industry'].value_counts().index[0] if len(df) > 0 else 'N/A'}
- Primary Event Category: {df['Event Category'].value_counts().index[0] if len(df) > 0 else 'N/A'}
- Most Affected State: {df['State'].value_counts().index[0] if len(df) > 0 else 'N/A'}

🏭 INDUSTRY DISTRIBUTION:
{chr(10).join([f"- {industry}: {count} events" for industry, count in df['Industry'].value_counts().items()])}

📈 IMPACT DISTRIBUTION:
{chr(10).join([f"- {level}: {count} events" for level, count in df['Impact Level'].value_counts().items()])}

🔖 EVENT CATEGORY DISTRIBUTION:
{chr(10).join([f"- {category}: {count} events" for category, count in df['Event Category'].value_counts().items()])}

🔧 CRITICAL UPDATES IMPLEMENTED:
- Removed "Risk Indicator" column completely
- Renamed "Business Risk Factor" to "Event Category"
- Added strict Event Category validation (8 categories)
- Implemented Industry Subtype logic
- Implemented Industry Risk Type logic
- Added "Analyst Comments" column
- Updated Impact Level logic (Positive always Low)
- Reordered columns as requested
- Enhanced industry-content validation

📋 COLUMN STRUCTURE:
Day | Month | Year | Date | State | City | Industry | Industry Subtype | Industry Risk Type | Event Category | Impact Type | Impact Level | Event Headline | Evidence Source Link | Analyst Comments

📋 ATTACHED FILES:
1. {filename} - Updated business risk dataset
2. {processing_filename} - Processing log with inclusion/exclusion details

This report implements all requested critical changes and ensures strict categorical validation.

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""",
                        attachment_path=filename,
                        smtp_server="smtp.gmail.com",
                        smtp_port=465,
                        smtp_password=sender_password
                    )
                except Exception as e:
                    logger.error(f"Failed to send email: {e}")
            else:
                logger.info("Email credentials not provided - skipping email send")
            
            logger.info("✅ Updated business risk processing completed successfully!")
            
            # Display sample records for verification
            logger.info("\n🔍 Sample Business Risk Records:")
            for i, record in enumerate(df.head(3).to_dict('records')):
                logger.info(f"\nRecord {i+1}:")
                logger.info(f"  Industry: {record['Industry']}")
                logger.info(f"  Industry Subtype: {record['Industry Subtype']}")
                logger.info(f"  Industry Risk Type: {record['Industry Risk Type']}")
                logger.info(f"  Event Category: {record['Event Category']}")
                logger.info(f"  Event: {record['Event Headline']}")
                logger.info(f"  Impact Level: {record['Impact Level']}")
                logger.info(f"  State: {record['State']}")
                logger.info(f"  Analyst Comments: {record['Analyst Comments']}")
        else:
            logger.warning("❌ No validated business risk records were generated.")
    
    except Exception as e:
        logger.error(f"❌ Error in main processing: {e}")
        raise

# ================================
# 🔹 10. Script Execution
# ================================

if __name__ == "__main__":
    print("🚀 Starting Updated DailyPost Business Risk Scraper...")
    print("🔧 Features: Updated column structure, Event Category validation, Industry Risk Type mapping")
    print("📊 Target: DailyPost business articles with strict categorical validation")
    print("🚫 Excludes: Risk Indicator column, political content without business relevance")
    print("=" * 70)
    
    asyncio.run(main())
