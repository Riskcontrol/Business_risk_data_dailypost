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
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from groq import AsyncGroq
import google.generativeai as genai
import json

# ================================
# 🔹 1. Initialize APIs & Web Scraper
# ================================

# Initialize Groq API Client
client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])

# Initialize Gemini API Client
#GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual Gemini API key
#genai.configure(api_key=GEMINI_API_KEY)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# User-Agent Rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
]

# News Sources for Business Data
BUSINESS_NEWS_URLS = [
    "https://www.dailypost.ng",
    "https://dailypost.ng/category/business/",
    "https://dailypost.ng/category/economy/",
    "https://punchng.com/topics/business/",
    "https://www.vanguardngr.com/category/business/",
    "https://www.premiumtimesng.com/business/"
]

# ================================
# 🔹 2. Business Risk Framework
# ================================

# Risk Factors and their indicators based on your SOP
BUSINESS_RISK_FACTORS = {
    "Economic": ["GDP", "Unemployment Rate", "Inflation rate"],
    "Political": ["Government stability", "Corruption", "Rule of law"],
    "Technology": ["Digital Infrastructure", "Cybersecurity", "Technology Adoption"],
    "Social": ["Poverty Rate", "Social unrest", "Education"],
    "Environmental": ["Air and water quality", "Natural disaster", "Climate change probability"],
    "Operational": ["Infrastructure Quality", "Supply chain disruption", "Business Continuity"],
    "Healthcare": ["Healthcare Access", "Disease prevalence", "Healthcare Infrastructure"],
    "Regulatory and Legal": ["Burden Of Compliance", "Legal Framework", "Enforcement"]
}

# Industry Types and Subtypes
INDUSTRY_MAPPING = {
    "Manufacturing": ["Factory", "Warehouse", "Supermarket"],
    "Healthcare": ["Hospitals", "Pharmaceutical"],
    "Finance & Banking": ["Banks", "Insurance", "Mortgage", "Microfinance"],
    "Oil & Gas": ["Upstream", "Downstream"],
    "Education": ["Primary", "Secondary", "Tertiary"],
    "Logistics & Transportation": ["Logistics", "Transportation (Land)", "Aviation (Air)", "Maritime (Sea)"],
    "Travel & Hospitality": ["Hotel", "Nightclub", "Bar", "Restaurant"],
    "Agro-allied": ["Farm", "Storage", "Livestock"],
    "Telecommunications": ["Telcomm", "Cloud", "Network"],
    "Mining": ["Mining", "Processing"],
    "Real Estate & Construction": ["Construction", "Real estate"]
}

# Industry Risk Types
INDUSTRY_RISK_TYPES = {
    "Manufacturing": ["Supply Chain Disruption", "Forex/Import Policy", "Labour Unrest", "Insecurity", "Energy Costs"],
    "Healthcare": ["Drug Supply Shortages", "Regulatory Changes", "Security Risks (Kidnapping/Attacks)", "Workforce Shortage", "Counterfeiting"],
    "Finance & Banking": ["Cybersecurity Threats", "Regulatory Policy Shifts", "Economic Instability", "Naira Volatility", "Fraud Trends"],
    "Oil & Gas": ["Pipeline Vandalism", "Community Unrest", "Regulatory Compliance", "Environmental Incidents", "Militant Activity"],
    "Education": ["Student Protests", "Terrorism/Insecurity", "Infrastructure Vandalism", "Regulatory Shifts", "Tuition Policy Changes"],
    "Logistics & Transportation": ["Road Infrastructure Quality", "Port Congestion", "Fuel Price Volatility", "Cargo Theft/Banditry", "Regulatory Permits", "Insecurity"],
    "Travel & Hospitality": ["Insecurity (Kidnapping/Terrorism)", "Health Epidemics", "Currency Volatility", "Regulatory Shifts (Tourism Policies)", "Labour Strikes"],
    "Agro-allied": ["Climate Risks", "Banditry & Herdsmen Attacks", "Market Price Volatility", "Supply Chain Blockages", "Land Use Policy", "Input Costs"],
    "Telecommunications": ["Vandalism of Infrastructure", "Regulatory Compliance (NCC)", "Cybersecurity Threats", "Power Supply Disruption", "Taxation Changes"],
    "Mining": ["Community Unrest", "Illegal Mining Activities", "Environmental Regulations", "Insecurity (Banditry/Terrorism)", "Licensing Delays"],
    "Real Estate & Construction": ["Policy Shifts (Land Use Act)", "Material Cost Volatility", "Regulatory Approvals Delays", "Insecurity (Site Theft/Kidnap)", "Infrastructure Quality"]
}

# Business Keywords for filtering
BUSINESS_KEYWORDS = [
    # Economic indicators
    'gdp', 'inflation', 'unemployment', 'economic', 'economy', 'recession', 'growth', 'naira', 'dollar', 'forex',
    'interest rate', 'monetary policy', 'fiscal policy', 'budget', 'revenue', 'tax', 'taxation',
    
    # Business operations
    'business', 'company', 'industry', 'factory', 'manufacturing', 'production', 'supply chain', 'logistics',
    'import', 'export', 'trade', 'commerce', 'investment', 'investor', 'market', 'price', 'cost',
    
    # Infrastructure and operations
    'infrastructure', 'port', 'airport', 'road', 'railway', 'power', 'electricity', 'fuel', 'energy',
    'telecommunications', 'banking', 'finance', 'insurance', 'loan', 'credit',
    
    # Risk-related terms
    'strike', 'protest', 'unrest', 'violence', 'attack', 'kidnap', 'terrorism', 'bandit', 'herdsmen',
    'vandalism', 'theft', 'fraud', 'corruption', 'policy', 'regulation', 'compliance', 'enforcement',
    'shutdown', 'closure', 'disruption', 'delay', 'shortage', 'scarcity',
    
    # Industry-specific
    'oil', 'gas', 'petroleum', 'pipeline', 'refinery', 'crude', 'nnpc', 'upstream', 'downstream',
    'agriculture', 'farming', 'crop', 'livestock', 'food', 'harvest',
    'mining', 'solid minerals', 'gold', 'coal', 'tin', 'iron ore',
    'healthcare', 'hospital', 'medical', 'drug', 'pharmaceutical', 'medicine',
    'education', 'school', 'university', 'student', 'teacher', 'academic',
    'construction', 'building', 'real estate', 'property', 'housing', 'land'
]

# Nigerian states for validation
NIGERIAN_STATES = [
    'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
    'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
    'Federal Capital Territory', 'FCT', 'Abuja', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 
    'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 
    'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 
    'Yobe', 'Zamfara'
]

# ================================
# 🔹 3. Load Neighbourhood Data
# ================================

def load_neighborhoods_data(filepath="state_neighbourhoods.csv"):
    """Load neighborhood data for location mapping."""
    NIGERIAN_STATES_COORDS = {
        'Abia': {'lat': 5.4301, 'lon': 7.5248},
        'Adamawa': {'lat': 9.3328, 'lon': 12.3954},
        'Akwa Ibom': {'lat': 5.0072, 'lon': 7.9306},
        'Anambra': {'lat': 6.2209, 'lon': 7.0388},
        'Bauchi': {'lat': 10.3158, 'lon': 9.8474},
        'Bayelsa': {'lat': 4.7719, 'lon': 6.0699},
        'Benue': {'lat': 7.3369, 'lon': 8.7404},
        'Borno': {'lat': 11.8846, 'lon': 13.1520},
        'Cross River': {'lat': 5.8702, 'lon': 8.6089},
        'Delta': {'lat': 5.5322, 'lon': 5.8983},
        'Ebonyi': {'lat': 6.2649, 'lon': 8.0137},
        'Edo': {'lat': 6.3350, 'lon': 5.6038},
        'Ekiti': {'lat': 7.7190, 'lon': 5.3110},
        'Enugu': {'lat': 6.4584, 'lon': 7.5463},
        'Federal Capital Territory': {'lat': 9.0764, 'lon': 7.3986},
        'FCT': {'lat': 9.0764, 'lon': 7.3986},
        'Abuja': {'lat': 9.0764, 'lon': 7.3986},
        'Gombe': {'lat': 10.2896, 'lon': 11.1698},
        'Imo': {'lat': 5.4833, 'lon': 7.0333},
        'Jigawa': {'lat': 12.2280, 'lon': 9.5615},
        'Kaduna': {'lat': 10.5166, 'lon': 7.4166},
        'Kano': {'lat': 11.9964, 'lon': 8.5167},
        'Katsina': {'lat': 12.9855, 'lon': 7.6184},
        'Kebbi': {'lat': 12.4539, 'lon': 4.1975},
        'Kogi': {'lat': 7.8012, 'lon': 6.7374},
        'Kwara': {'lat': 9.5917, 'lon': 4.5481},
        'Lagos': {'lat': 6.5244, 'lon': 3.3792},
        'Nasarawa': {'lat': 8.5399, 'lon': 8.2980},
        'Niger': {'lat': 9.9309, 'lon': 5.5982},
        'Ogun': {'lat': 7.1600, 'lon': 3.3500},
        'Ondo': {'lat': 7.2500, 'lon': 5.2000},
        'Osun': {'lat': 7.7583, 'lon': 4.5641},
        'Oyo': {'lat': 7.8500, 'lon': 3.9300},
        'Plateau': {'lat': 9.2182, 'lon': 9.5179},
        'Rivers': {'lat': 4.7500, 'lon': 7.0000},
        'Sokoto': {'lat': 13.0654, 'lon': 5.2379},
        'Taraba': {'lat': 7.9994, 'lon': 10.7744},
        'Yobe': {'lat': 12.2939, 'lon': 11.4390},
        'Zamfara': {'lat': 12.1222, 'lon': 6.2236}
    }
    
    try:
        if not os.path.exists(filepath):
            print(f"Neighborhood file {filepath} not found. Using default coordinates.")
            return {
                "by_state": {state: [{"name": state, "latitude": coords["lat"], "longitude": coords["lon"]}] 
                           for state, coords in NIGERIAN_STATES_COORDS.items()},
                "all_neighborhoods": [],
                "neighborhood_names": set()
            }
        
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} neighborhoods from {filepath}")
        
        neighborhoods_by_state = {}
        all_neighborhoods = []
        neighborhood_names = set()
        
        for _, row in df.iterrows():
            state = row['state']
            neighborhood = row['neighbourhood_name']
            
            try:
                lat = float(row['latitude'])
                lon = float(row['longitude'])
                
                if state not in neighborhoods_by_state:
                    neighborhoods_by_state[state] = []
                
                neighborhoods_by_state[state].append({
                    "name": neighborhood,
                    "latitude": lat,
                    "longitude": lon
                })
                
                all_neighborhoods.append({
                    "name": neighborhood,
                    "state": state,
                    "latitude": lat,
                    "longitude": lon
                })
                
                neighborhood_names.add(neighborhood.lower())
                
            except (ValueError, TypeError):
                continue
        
        for state, coords in NIGERIAN_STATES_COORDS.items():
            if state not in neighborhoods_by_state:
                neighborhoods_by_state[state] = [{
                    "name": state,
                    "latitude": coords["lat"],
                    "longitude": coords["lon"]
                }]
        
        return {
            "by_state": neighborhoods_by_state,
            "all_neighborhoods": all_neighborhoods,
            "neighborhood_names": neighborhood_names
        }
        
    except Exception as e:
        print(f"Error loading neighborhood data: {e}")
        return {
            "by_state": {state: [{"name": state, "latitude": coords["lat"], "longitude": coords["lon"]}] 
                       for state, coords in NIGERIAN_STATES_COORDS.items()},
            "all_neighborhoods": [],
            "neighborhood_names": set()
        }

# ================================
# 🔹 4. WebDriver Setup
# ================================

def init_driver():
    """Initialize and return a WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# ================================
# 🔹 5. Web Scraping Functions
# ================================

def get_business_article_links(driver):
    """Extract business-related article links from various news sources."""
    all_links = []
    
    for url in BUSINESS_NEWS_URLS:
        try:
            print(f"Getting business links from {url}")
            driver.get(url)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Get all links from the page with date patterns
            pattern = re.compile(r"/\d{4}/\d{2}/\d{2}/")
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if pattern.search(href):
                    # Convert relative URLs to absolute
                    if not href.startswith("http"):
                        base_domain = re.match(r'https?://[^/]+', url).group(0)
                        href = base_domain + href
                    if href not in all_links:
                        all_links.append(href)
            
            print(f"Found {len(all_links)} links so far")
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"Error getting links from {url}: {e}")
    
    print(f"Total unique business links found: {len(all_links)}")
    return all_links

def scrape_business_article(driver, url):
    """Scrape business article content."""
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract title and description
        title = soup.find("title").text.strip() if soup.find("title") else "No title found"
        meta_desc = soup.find("meta", {"name": "description"})
        description = meta_desc["content"].strip() if meta_desc and meta_desc.has_attr("content") else "No description found"
        
        # Extract article content based on site
        article_text = ""
        
        # DailyPost
        if "dailypost.ng" in url:
            content_container = soup.find("div", id="mvp-content-main")
            if content_container:
                paragraphs = content_container.find_all("p")
                article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
        # Punch
        elif "punchng.com" in url:
            content_container = soup.find("div", class_="post-content")
            if content_container:
                paragraphs = content_container.find_all("p")
                article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
        # Vanguard
        elif "vanguardngr.com" in url:
            content_container = soup.find("div", class_="entry-content")
            if content_container:
                paragraphs = content_container.find_all("p")
                article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
        # Premium Times
        elif "premiumtimesng.com" in url:
            content_container = soup.find("div", class_="content")
            if content_container:
                paragraphs = content_container.find_all("p")
                article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
        # Generic extraction
        if not article_text:
            paragraphs = soup.find_all("p")
            article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
        return {
            "Title": title,
            "Description": description,
            "Content": article_text,
            "Link": url
        }
        
    except Exception as e:
        print(f"Error scraping business article {url}: {e}")
        return None

def is_business_relevant(article):
    """Check if article is relevant to business risks."""
    content = (article["Title"] + " " + article["Description"] + " " + article["Content"]).lower()
    
    # Check for business keywords
    keyword_count = sum(1 for keyword in BUSINESS_KEYWORDS if keyword in content)
    
    # Article is relevant if it contains at least 2 business keywords
    return keyword_count >= 2

# ================================
# 🔹 6. AI Analysis Functions
# ================================

BUSINESS_ANALYSIS_PROMPT = """
You are an expert business risk analyst specializing in Nigerian market conditions. 
Analyze the following news article and extract business risk information with high precision.

Extract the following information in JSON format:

1. **Industry** (Choose the most relevant):
   - Manufacturing, Healthcare, Finance & Banking, Oil & Gas, Education, 
   - Logistics & Transportation, Travel & Hospitality, Agro-allied, 
   - Telecommunications, Mining, Real Estate & Construction

2. **Industry Subtype** (Based on industry selected):
   Manufacturing: Factory, Warehouse, Supermarket
   Healthcare: Hospitals, Pharmaceutical
   Finance & Banking: Banks, Insurance, Mortgage, Microfinance
   Oil & Gas: Upstream, Downstream
   Education: Primary, Secondary, Tertiary
   Logistics & Transportation: Logistics, Transportation (Land), Aviation (Air), Maritime (Sea)
   Travel & Hospitality: Hotel, Nightclub, Bar, Restaurant
   Agro-allied: Farm, Storage, Livestock
   Telecommunications: Telcomm, Cloud, Network
   Mining: Mining, Processing
   Real Estate & Construction: Construction, Real estate

3. **Business Risk Factor** (Choose most relevant):
   - Economic, Political, Technology, Social, Environmental, 
   - Operational, Healthcare, Regulatory and Legal

4. **Risk Indicator** (Based on Risk Factor):
   Economic: GDP, Unemployment Rate, Inflation rate
   Political: Government stability, Corruption, Rule of law
   Technology: Digital Infrastructure, Cybersecurity, Technology Adoption
   Social: Poverty Rate, Social unrest, Education
   Environmental: Air and water quality, Natural disaster, Climate change probability
   Operational: Infrastructure Quality, Supply chain disruption, Business Continuity
   Healthcare: Healthcare Access, Disease prevalence, Healthcare Infrastructure
   Regulatory and Legal: Burden Of Compliance, Legal Framework, Enforcement

5. **Impact Type**: Positive or Negative

6. **Impact Level** (1-4):
   1 = Low: No known threat, unverified report, non-violent protest, minor regulatory update
   2 = Medium: Notification of strike, major delay, policy change, localized violent threat
   3 = High: Confirmed major disruption, security incident, policy changes, health/environmental disasters
   4 = Critical: Shutdowns, attacks, policy crisis with national impact

7. **Event Headline** (Max 20 words): Brief, clear headline describing the business risk

8. **Industry Risktype** (Choose most relevant for the identified industry):
   Manufacturing: Supply Chain Disruption, Forex/Import Policy, Labour Unrest, Insecurity, Energy Costs
   Healthcare: Drug Supply Shortages, Regulatory Changes, Security Risks, Workforce Shortage, Counterfeiting
   Finance & Banking: Cybersecurity Threats, Regulatory Policy Shifts, Economic Instability, Naira Volatility, Fraud Trends
   Oil & Gas: Pipeline Vandalism, Community Unrest, Regulatory Compliance, Environmental Incidents, Militant Activity
   Education: Student Protests, Terrorism/Insecurity, Infrastructure Vandalism, Regulatory Shifts, Tuition Policy Changes
   Logistics & Transportation: Road Infrastructure Quality, Port Congestion, Fuel Price Volatility, Cargo Theft/Banditry, Regulatory Permits, Insecurity
   Travel & Hospitality: Insecurity, Health Epidemics, Currency Volatility, Regulatory Shifts, Labour Strikes
   Agro-allied: Climate Risks, Banditry & Herdsmen Attacks, Market Price Volatility, Supply Chain Blockages, Land Use Policy, Input Costs
   Telecommunications: Vandalism of Infrastructure, Regulatory Compliance, Cybersecurity Threats, Power Supply Disruption, Taxation Changes
   Mining: Community Unrest, Illegal Mining Activities, Environmental Regulations, Insecurity, Licensing Delays
   Real Estate & Construction: Policy Shifts, Material Cost Volatility, Regulatory Approvals Delays, Insecurity, Infrastructure Quality

9. **State**: Nigerian state mentioned in the article
10. **City**: Specific city or location mentioned

IMPORTANT RULES:
- If Impact Type is Positive, Impact Level must be 1 (Low)
- Only extract information explicitly mentioned in the article
- Use null for fields where information is not available
- Return response in clean JSON format only

Return your analysis in JSON format without explanations.
"""

async def analyze_business_article(article):
    """Use AI to analyze business article and extract risk information."""
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": BUSINESS_ANALYSIS_PROMPT},
                {"role": "user", "content": f"Title: {article['Title']}\n\nDescription: {article['Description']}\n\nContent: {article['Content']}"}
            ],
            model="llama3-8b-8192",
            temperature=0.2,
            max_tokens=2000
        )
        
        extracted_text = response.choices[0].message.content
        
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
                    print(f"Failed to parse JSON: {extracted_text}")
                    extracted_data = {}
            else:
                print(f"Could not find JSON object: {extracted_text}")
                extracted_data = {}
        
        return extracted_data
    
    except Exception as e:
        print(f"Error analyzing business article: {e}")
        return {}

# ================================
# 🔹 7. Gemini Verification Functions
# ================================

GEMINI_VERIFICATION_PROMPT = """
You are a senior quality assurance analyst tasked with verifying the accuracy of business risk data extraction.

Review the following:

1. **Original News Article:**
Title: {title}
Content: {content}

2. **Extracted Business Risk Data:**
{extracted_data}

**Verification Tasks:**

1. **Content Intent Verification**: Does the extracted data accurately reflect the main business risk discussed in the article? (Yes/No)

2. **State/Location Accuracy**: Is the state mentioned in the extracted data actually referenced in the article? (Yes/No)

3. **Industry Classification**: Is the industry classification appropriate based on the article content? (Yes/No)

4. **Risk Factor Mapping**: Does the risk factor correctly categorize the type of business risk described? (Yes/No)

5. **Impact Assessment**: Is the impact level (1-4) and type (Positive/Negative) appropriate for the event described? (Yes/No)

6. **Overall Accuracy Score**: Rate the overall accuracy from 1-10 (where 10 is perfect accuracy)

7. **Recommendations**: If accuracy score is below 7, provide specific corrections needed.

8. **Final Decision**: Should this record be INCLUDED or EXCLUDED from the final dataset?

Respond in the following JSON format:
{
  "content_intent_accurate": true/false,
  "location_accurate": true/false,
  "industry_classification_accurate": true/false,
  "risk_factor_accurate": true/false,
  "impact_assessment_accurate": true/false,
  "accuracy_score": 1-10,
  "recommendations": "specific corrections needed",
  "final_decision": "INCLUDE/EXCLUDE",
  "verification_summary": "brief explanation of decision"
}
"""

async def verify_with_gemini(article, extracted_data):
    """Use Gemini to verify the accuracy of extracted business risk data."""
    try:
        # Prepare the verification prompt
        prompt = GEMINI_VERIFICATION_PROMPT.format(
            title=article["Title"],
            content=article["Content"][:3000],  # Limit content length for API
            extracted_data=json.dumps(extracted_data, indent=2)
        )
        
        # Call Gemini API
        response = gemini_model.generate_content(prompt)
        verification_text = response.text
        
        # Extract JSON from response
        json_match = re.search(r'```(?:json)?(.*?)```', verification_text, re.DOTALL)
        if json_match:
            verification_text = json_match.group(1).strip()
        
        # Parse verification JSON
        try:
            verification_data = json.loads(verification_text)
        except json.JSONDecodeError:
            json_start = verification_text.find('{')
            json_end = verification_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                cleaned_json = verification_text[json_start:json_end]
                try:
                    verification_data = json.loads(cleaned_json)
                except:
                    print(f"Failed to parse Gemini verification JSON: {verification_text}")
                    verification_data = {"final_decision": "EXCLUDE", "accuracy_score": 0}
            else:
                print(f"Could not find JSON in Gemini response: {verification_text}")
                verification_data = {"final_decision": "EXCLUDE", "accuracy_score": 0}
        
        return verification_data
    
    except Exception as e:
        print(f"Error with Gemini verification: {e}")
        return {"final_decision": "EXCLUDE", "accuracy_score": 0, "verification_summary": f"Verification failed: {e}"}

# ================================
# 🔹 8. Location and Data Processing
# ================================

def extract_location_info(article, neighborhoods_data):
    """Extract state and city information from article."""
    content = article["Title"] + " " + article["Description"] + " " + article["Content"]
    
    # Extract state
    state = "Unknown"
    for state_name in NIGERIAN_STATES:
        if re.search(r'\b' + re.escape(state_name) + r'\b', content, re.IGNORECASE):
            if state_name.lower() in ["abuja", "fct"]:
                state = "Federal Capital Territory"
            else:
                state = state_name
            break
    
    # Extract city
    city = "Unknown"
    if state != "Unknown" and state in neighborhoods_data["by_state"]:
        for neighborhood in neighborhoods_data["by_state"][state]:
            if re.search(r'\b' + re.escape(neighborhood["name"]) + r'\b', content, re.IGNORECASE):
                city = neighborhood
                break
        
        # If no specific city found, use state as city
        if city == "Unknown":
            city = state
    
    return state, city

def validate_state(state):
    """Validate if the extracted state is a valid Nigerian state."""
    if state == "Unknown":
        return False
    
    # Normalize state name
    if state.lower() in ["abuja", "fct"]:
        state = "Federal Capital Territory"
    
    return state in NIGERIAN_STATES

def create_business_risk_record(article, analysis, neighborhoods_data):
    """Create a business risk record in the required format."""
    # Get current date
    today = datetime.now()
    
    # Extract location
    state, city = extract_location_info(article, neighborhoods_data)
    
    # Override with AI analysis if available
    if analysis.get("State"):
        state = analysis["State"]
    if analysis.get("City"):
        city = analysis["City"]
    
    # Validate state - if unknown, return None to exclude this record
    if not validate_state(state):
        print(f"Invalid or unknown state '{state}' - excluding record")
        return None
    
    # Ensure positive impact is always low level
    impact_type = analysis.get("Impact Type", "Negative")
    impact_level = analysis.get("Impact Level", 2)
    
    if impact_type == "Positive" and impact_level != 1:
        impact_level = 1
    
    record = {
        "Day": today.day,
        "Month": today.strftime("%b"),
        "Year": today.year,
        "Date": today.strftime("%d/%m/%Y"),
        "State": state,
        "City": city,
        "Industry": analysis.get("Industry", ""),
        "Industry Subtype": analysis.get("Industry Subtype", ""),
        "Business Risk Factor": analysis.get("Business Risk Factor", ""),
        "Risk Indicator": analysis.get("Risk Indicator", ""),
        "Impact Type": impact_type,
        "Impact Level": impact_level,
        "Event Headline": analysis.get("Event Headline", article["Title"][:100]),
        "Evidence Source Link": article["Link"],
        "Analyst Comments": "",
        "Industry Risktype": analysis.get("Industry Risktype", "")
    }
    
    return record

# ================================
# 🔹 9. Enhanced Validation Functions
# ================================

def validate_business_record(record):
    """Validate business risk record for completeness and accuracy."""
    required_fields = ['Industry', 'Business Risk Factor', 'Risk Indicator', 'Impact Type', 'Impact Level']
    
    for field in required_fields:
        if not record.get(field) or record[field] == "":
            return False, f"Missing required field: {field}"
    
    # Validate Impact Type and Level relationship
    if record['Impact Type'] == 'Positive' and record['Impact Level'] != 1:
        return False, "Positive impact must have Low (1) impact level"
    
    # Validate Impact Level range
    if record['Impact Level'] not in [1, 2, 3, 4]:
        return False, "Impact Level must be between 1-4"
    
    # Validate Industry and Industry Subtype relationship
    industry = record.get('Industry', '')
    subtype = record.get('Industry Subtype', '')
    
    if industry in INDUSTRY_MAPPING and subtype:
        if subtype not in INDUSTRY_MAPPING[industry]:
            return False, f"Invalid subtype {subtype} for industry {industry}"
    
    # Validate state
    if not validate_state(record.get('State', '')):
        return False, "Invalid or unknown state"
    
    return True, "Valid record"

def cross_validate_with_content(record, article):
    """Cross-validate extracted data with original article content."""
    content = (article["Title"] + " " + article["Description"] + " " + article["Content"]).lower()
    
    validation_score = 0
    max_score = 5
    
    # Check if industry is mentioned in content
    industry = record.get('Industry', '').lower()
    if industry and industry in content:
        validation_score += 1
    
    # Check if state is mentioned in content
    state = record.get('State', '').lower()
    if state and (state in content or state.replace(' ', '') in content):
        validation_score += 1
    
    # Check if risk factor keywords are present
    risk_factor = record.get('Business Risk Factor', '').lower()
    risk_keywords_map = {
        'economic': ['economic', 'economy', 'inflation', 'gdp', 'unemployment', 'naira', 'dollar'],
        'political': ['political', 'government', 'policy', 'corruption', 'stability'],
        'operational': ['supply chain', 'infrastructure', 'disruption', 'operations'],
        'social': ['social', 'unrest', 'protest', 'education', 'poverty'],
        'regulatory and legal': ['regulation', 'compliance', 'legal', 'enforcement', 'law']
    }
    
    if risk_factor in risk_keywords_map:
        if any(keyword in content for keyword in risk_keywords_map[risk_factor]):
            validation_score += 1
    
    # Check impact type alignment
    impact_type = record.get('Impact Type', '').lower()
    if impact_type == 'negative':
        negative_words = ['crisis', 'attack', 'disruption', 'shortage', 'loss', 'damage', 'threat']
        if any(word in content for word in negative_words):
            validation_score += 1
    elif impact_type == 'positive':
        positive_words = ['growth', 'improvement', 'increase', 'boost', 'recovery', 'success']
        if any(word in content for word in positive_words):
            validation_score += 1
    
    # Check headline relevance
    headline = record.get('Event Headline', '').lower()
    title = article["Title"].lower()
    if headline and any(word in title for word in headline.split() if len(word) > 3):
        validation_score += 1
    
    return validation_score / max_score

# ================================
# 🔹 10. Email Function
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
        
        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# ================================
# 🔹 11. Main Function with Enhanced Verification
# ================================

async def main():
    """Main function to run the business risk scraper with enhanced verification."""
    print("Starting Enhanced Business Risk Data Scraper with Gemini Verification...")
    
    # Load neighborhood data
    neighborhoods_data = load_neighborhoods_data()
    print(f"Loaded neighborhood data with {len(neighborhoods_data['all_neighborhoods'])} locations")
    
    # Initialize WebDriver
    driver = init_driver()
    
    try:
        # Get business article links
        article_links = get_business_article_links(driver)
        print(f"Found {len(article_links)} business article links")
        
        # Scrape articles
        articles = []
        for url in article_links:
            article = scrape_business_article(driver, url)
            if article and is_business_relevant(article):
                articles.append(article)
                print(f"Found relevant business article: {article['Title'][:80]}...")
            
            time.sleep(random.uniform(2, 4))  # Random delay between requests
        
        print(f"Successfully scraped {len(articles)} relevant business articles")
        
        if not articles:
            print("No relevant business articles found. Exiting.")
            return
        
        # Analyze articles and create business risk records with enhanced verification
        business_risk_records = []
        verification_results = []
        
        for i, article in enumerate(articles):
            try:
                print(f"Processing article {i+1}/{len(articles)}: {article['Title'][:60]}...")
                
                # Step 1: Initial AI analysis
                analysis = await analyze_business_article(article)
                
                if not analysis:
                    print("  ❌ Initial analysis failed - skipping")
                    continue
                
                # Step 2: Create preliminary record
                preliminary_record = create_business_risk_record(article, analysis, neighborhoods_data)
                
                if not preliminary_record:
                    print("  ❌ Record creation failed (likely unknown state) - skipping")
                    continue
                
                # Step 3: Basic validation
                is_valid, validation_message = validate_business_record(preliminary_record)
                if not is_valid:
                    print(f"  ❌ Basic validation failed: {validation_message} - skipping")
                    continue
                
                # Step 4: Cross-validation with content
                content_score = cross_validate_with_content(preliminary_record, article)
                print(f"  📊 Content validation score: {content_score:.2f}")
                
                # Step 5: Gemini verification (second-level verification)
                print("  🔍 Performing Gemini verification...")
                gemini_verification = await verify_with_gemini(article, analysis)
                
                # Step 6: Decision based on verifications
                accuracy_score = gemini_verification.get('accuracy_score', 0)
                final_decision = gemini_verification.get('final_decision', 'EXCLUDE')
                
                print(f"  🎯 Gemini accuracy score: {accuracy_score}/10")
                print(f"  🎯 Gemini decision: {final_decision}")
                
                # Store verification results for reporting
                verification_results.append({
                    'title': article['Title'][:100],
                    'content_score': content_score,
                    'gemini_score': accuracy_score,
                    'gemini_decision': final_decision,
                    'verification_summary': gemini_verification.get('verification_summary', ''),
                    'included': False
                })
                
                # Include record only if it passes all verifications
                if final_decision == 'INCLUDE' and accuracy_score >= 7 and content_score >= 0.6:
                    business_risk_records.append(preliminary_record)
                    verification_results[-1]['included'] = True
                    print("  ✅ Record INCLUDED after verification")
                else:
                    print(f"  ❌ Record EXCLUDED - Decision: {final_decision}, Score: {accuracy_score}, Content: {content_score:.2f}")
                
                # Add small delay between Gemini API calls
                time.sleep(2)
                
            except Exception as e:
                print(f"  ❌ Error processing article: {e}")
                continue
        
        print(f"\n📊 Verification Summary:")
        print(f"Total articles processed: {len(articles)}")
        print(f"Records created after verification: {len(business_risk_records)}")
        print(f"Exclusion rate: {((len(articles) - len(business_risk_records)) / len(articles) * 100):.1f}%")
        
        # Save verification report
        if verification_results:
            verification_df = pd.DataFrame(verification_results)
            verification_filename = f'verification_report_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
            verification_df.to_csv(verification_filename, index=False)
            print(f"Verification report saved to {verification_filename}")
        
        # Save business risk data
        if business_risk_records:
            df = pd.DataFrame(business_risk_records)
            
            # Sort by date and impact level (most recent and critical first)
            df = df.sort_values(['Year', 'Month', 'Day', 'Impact Level'], 
                              ascending=[False, False, False, False])
            
            # Save to CSV
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f'business_risk_data_verified_{timestamp}.csv'
            df.to_csv(filename, index=False)
            print(f"Verified business risk data saved to {filename}")
            
            # Display summary statistics
            print("\n📊 Business Risk Data Summary:")
            print(f"Total Verified Records: {len(df)}")
            print(f"Industries Covered: {df['Industry'].nunique()}")
            print(f"States Covered: {df['State'].nunique()}")
            print(f"Risk Factors: {df['Business Risk Factor'].nunique()}")
            
            print("\n🏭 Top Industries by Risk Events:")
            industry_counts = df['Industry'].value_counts().head(5)
            for industry, count in industry_counts.items():
                print(f"  {industry}: {count} events")
            
            print("\n🌍 Top States by Risk Events:")
            state_counts = df['State'].value_counts().head(5)
            for state, count in state_counts.items():
                print(f"  {state}: {count} events")
            
            print("\n⚠️ Risk Factor Distribution:")
            risk_factor_counts = df['Business Risk Factor'].value_counts()
            for factor, count in risk_factor_counts.items():
                print(f"  {factor}: {count} events")
            
            print("\n📈 Impact Level Distribution:")
            impact_counts = df['Impact Level'].value_counts().sort_index()
            impact_labels = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}
            for level, count in impact_counts.items():
                print(f"  Level {level} ({impact_labels.get(level, 'Unknown')}): {count} events")
            
            # Generate insights based on verification results
            included_count = sum(1 for vr in verification_results if vr['included'])
            avg_gemini_score = sum(vr['gemini_score'] for vr in verification_results) / len(verification_results)
            avg_content_score = sum(vr['content_score'] for vr in verification_results) / len(verification_results)
            
            # Send email with the verified business risk data
            send_email(
                sender_email=os.environ.get('USER_EMAIL'),
                receiver_email="riskcontrolservicesnig@gmail.com",
                subject="Verified Daily Business Risk Data Update",
                body=f"""Enhanced Business Risk Intelligence Report with Gemini Verification

🔍 VERIFICATION METRICS:
- Articles Processed: {len(articles)}
- Records After Verification: {len(df)}
- Quality Acceptance Rate: {(included_count / len(verification_results) * 100):.1f}%
- Average Gemini Accuracy Score: {avg_gemini_score:.1f}/10
- Average Content Validation Score: {avg_content_score:.2f}

📊 BUSINESS INTELLIGENCE SUMMARY:
- Total Verified Risk Events: {len(df)}
- Industries Monitored: {df['Industry'].nunique()}
- States with Business Risks: {df['State'].nunique()}
- High/Critical Events: {len(df[df['Impact Level'] >= 3])}

🔍 TOP RISK AREAS:
- Primary Industry at Risk: {df['Industry'].value_counts().index[0] if len(df) > 0 else 'N/A'}
- Primary Risk Factor: {df['Business Risk Factor'].value_counts().index[0] if len(df) > 0 else 'N/A'}
- Most Affected State: {df['State'].value_counts().index[0] if len(df) > 0 else 'N/A'}

🎯 QUALITY ASSURANCE:
- All records have been verified using Gemini AI for accuracy
- Only records with 70%+ accuracy scores are included
- Unknown states and invalid data have been filtered out
- Cross-validation performed against original news content

📋 ATTACHED FILES:
1. {filename} - Verified business risk data
2. {verification_filename} - Detailed verification report

This enhanced report ensures maximum data quality and reliability for strategic business risk analysis.

Generated automatically with AI-powered verification from Nigerian business news sources.
""",
                attachment_path=filename,
                smtp_server="smtp.gmail.com",
                smtp_port=465,
                smtp_password=os.environ.get('USER_PASSWORD')
            )
            
            print("✅ Enhanced business risk data processing with verification completed successfully")
        else:
            print("❌ No business risk records passed verification.")
    
    except Exception as e:
        print(f"❌ Error in main processing: {e}")
    
    finally:
        # Clean up
        driver.quit()

# ================================
# 🔹 12. Script Execution
# ================================

if __name__ == "__main__":
    print("🚀 Starting Enhanced Business Risk Scraper with Gemini Verification...")
    print("⚠️  Remember to replace 'YOUR_GEMINI_API_KEY_HERE' with your actual Gemini API key!")
    asyncio.run(main())

