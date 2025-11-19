from flask import Flask, render_template, url_for, redirect
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
import re 
from flask import render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Global DataFrame to hold scraped data
scraped_data = pd.DataFrame()



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')


@app.route('/data_science')
def data_science():
    return render_template('data_science.html')

@app.route('/aboutcodroidhub')
def aboutcodroidhub():
    return render_template('aboutcodroidhub.html')



@app.route('/aiml')
def aiml():
    return render_template('aiml.html')






@app.route('/powerbiDashboards')
def powerbiDashboards():
    return render_template('powerbiDashboards.html')


@app.route("/covid19_dashboard")
def covid19_dashboard():
    return render_template("covid19_dashboard.html")

@app.route("/banking_churn")
def banking_churn():
    return render_template("banking_churn.html")

@app.route("/titanic_dashboard")
def titanic_dashboard():
    return render_template("titanic_dashboard.html")

@app.route("/iris_dashboard")
def iris_dashboard():
    return render_template("iris_dashboard.html")

@app.route("/hr_analytics_dashboard")
def hr_analytics_dashboard():
    return render_template("hr_analytics_dashboard.html")

@app.route("/super_store_dashboard")
def super_store_dashboard():
    return render_template("super_store_dashboard.html")






# @app.route('/scraping-flipkart')
# def scraping_flipkart():
#     return render_template('scraping-flipkart.html')




# @app.route('/scraping-amazon')
# def scraping_amazon():
#     return render_template('scraping-amazon.html')


# @app.route('/amazon')
# def amazon():
#     return render_template('amazon.html')

#flipkart
@app.route('/flipkart')
def flipkart():
    global scraped_data

    url="https://www.flipkart.com/search?q=mouse&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    mouse_data=[]
    data=soup.find_all("div" ,class_='slAVV4')



    for i in data:
        name = i.find("a",class_="wjcEIp")
        discount_price = i.find("div", class_="Nx9bqj")
        ratings = i.find("div", class_="XQDdHH")
        discount_off=i.find("div",class_="UkUFwK")
        original_price=i.find("div",class_="yRaY8j")

    

        mouse_data.append({
        "Name":name,
        "Discount Price":discount_price,
        "Ratings":ratings,
        "Discount off%":discount_off,
        "Original Price":original_price
    })
    scraped_data = pd.DataFrame(mouse_data)
    return render_template("flipkart.html", data=scraped_data.to_html(index=False, classes="styled-table"))












#amazon-watche
@app.route('/amazon')
def amazon():
    global scraped_data

    url="https://www.amazon.in/s?k=watches&crid=2XEWE9M2261T7&sprefix=watches%2Caps%2C1539&ref=nb_sb_noss_2"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    watche_data=[]
    watches=soup.find_all("div" ,class_='a-section a-spacing-small puis-padding-left-micro puis-padding-right-micro')


    for i in watches:
        name= i.find("span", class_="a-size-base-plus a-color-base")
        price=i.find("span",class_="a-price-whole")
        rating=i.find("span",class_="a-size-small a-color-base")
        free_dilvary_date=i.find("span",class_="a-text-bold")

        watche_data.append ( {
        "Watch Name":name,
        "Price":price,
        "Ratings":rating,
        "Free Dilvary Date":free_dilvary_date
    
    
    }) 
    scraped_data = pd.DataFrame(watche_data)
    return render_template("amazon.html", data=scraped_data.to_html(index=False, classes="styled-table"))












@app.route('/scraping')
def scraping():
    return render_template('scraping.html')


#Goodreads Website
@app.route('/goodreads')
def goodreads():
    global scraped_data

    url = "https://www.goodreads.com/quotes"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes_data = []
    quotes = soup.find_all("div", class_='quote')

    for i in quotes:
        Quote = i.find("div", class_="quoteText").get_text(strip=True)
        Author = i.find("span", class_="authorOrTitle").get_text(strip=True)
    
    # Find the likes <a> tag correctly
        likes_tag = i.find("a", class_="smallText")  # adjust class if needed
        if likes_tag:
            likes_text = likes_tag.get_text(strip=True)
            likes_number = re.sub(r'\D', '', likes_text)  # remove all non-digit chars
            Total_likes = int(likes_number) if likes_number else 0
        else:
            Total_likes = 0

    

        quotes_data.append({
        "Quote": Quote,
        "Author": Author,
        "Likes": Total_likes
    })

    scraped_data = pd.DataFrame(quotes_data)
    return render_template("goodreads.html", data=scraped_data.to_html(index=False, classes="styled-table"))




#Book To Scrape  Website
@app.route('/BookScrape')
def BookScrape():
    global scraped_data
    
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    book_data = []
    books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
 
    for i in books:
        # Book name
        Book_name = i.find("h3").find("a")
        Book_name = Book_name.get("title") if Book_name else "N/A"

        # Book price
        Book_price = i.find("p", class_="price_color")
        if Book_price:
            price_text = Book_price.get_text(strip=True).replace("Â", "").replace("£", "")
            try:
                price_value = float(price_text)
                Book_price = f"₹{price_value * 100:.2f}"
            except:
                Book_price = "N/A"
        else:
            Book_price = "N/A"

        Book_rating = i.find("p", class_="star-rating")
        if Book_rating:
            classes = Book_rating.get("class")
            rating_word = classes[1] if len(classes) > 1 else "N/A"
            ratings = ["Zero","One","Two","Three","Four","Five"]
            Book_rating = ratings.index(rating_word) if rating_word in ratings else "N/A"
        else:
            Book_rating = "N/A"

        book_data.append([Book_name, Book_price, Book_rating])

    scraped_data = pd.DataFrame(book_data, columns=["Name", "Price", "Rating"])
    
    return render_template("BookScrape.html", data=scraped_data.to_html(index=False, classes="styled-table"))

# @app.route('/bookto scrape_BarChart')
# def booktoscrape_BarChart():
#     if scraped_data.empty:
#         return redirect('/BookScrape')

#     plt.figure(figsize=(10, 6))
#     plt.bar(scraped_data["Name"], scraped_data["Price"],scraped_data["Rating"])
#     plt.xticks(rotation=90)
#     plt.ylabel("Price (£)")
#     plt.title("Book Prices - Bar Chart")
#     chart_path = os.path.join(app.config['UPLOAD_FOLDER'], 'chart.png')
#     plt.tight_layout()
#     plt.savefig(chart_path)
#     plt.close()
#     return render_template('bookto scrape_BarChart.html', chart_url=url_for('static', filename='chart.png'))



# @app.route('/book to scrape_PieChart')
# def booktoscrape_PieChart():
#     if scraped_data.empty:
#         return redirect('/templates/book to scrape_PieChart')

#     top_books = scraped_data.sort_values(by="Price", ascending=False).head(5)
#     plt.figure(figsize=(8, 8))
#     plt.pie(top_books["Price"], labels=top_books["Name"], autopct="%1.1f%%", startangle=140)
#     plt.title("Books")
#     chart_path = os.path.join(app.config['UPLOAD_FOLDER'], 'chart.png')
#     plt.savefig(chart_path)
#     plt.close()
#     return render_template('book to scrape_PieChart.html', chart_url=url_for('static', filename='chart.png'))




#quotes to scrape website
@app.route('/QuotesScrape')
def QuotesScrape():
    global scraped_data

    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes_data = []
    quotes=soup.find_all("div" ,class_='quote')


    for i in quotes:
        title = i.find("span", class_="text").get_text(strip=True)
        Author = i.find("small", class_="author").get_text(strip=True)
    
    # Get all tag <a> elements under div with class 'tags'
        tag_elements = i.find("div", class_="tags").find_all("a", class_="tag")
        tags = [tag.get_text(strip=True) for tag in tag_elements]
    
        quotes_data.append({
        "Quote": title,
        "Author": Author,
        "Tags": tags
    })
    scraped_data = pd.DataFrame(quotes_data)
    return render_template("QuotesScrape.html", data=scraped_data.to_html(index=False, classes="styled-table"))


#Gilson website
@app.route('/gilson')
def gilson():
    global scraped_data

    url = "https://www.gilson.com/default/shop-products/pipettes.html?srsltid=AfmBOoqOV3Sdidb7prT6f91fn9c_JRv_uo8cpJNV_r-EaKW_5kikp4hx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pipette_data=[]

    pipette = soup.find_all('div', class_="product details product-item-details")



    for p in pipette:
    
        product_element = p.find('div', class_="sku-box")
        product = product_element.get_text(strip=True) if product_element else "N/A"

        title_element = p.find('a', class_="product-item-link")
        title = title_element.get_text(strip=True) if title_element else "N/A"

        price_element = p.find('span', class_="price")
        price = price_element.get_text(strip=True) if price_element else "N/A"

        pipette_data.append({
      "Product ID": product,
      "Product Name": title,
      "Price": price,
    })

    scraped_data = pd.DataFrame(pipette_data)
    return render_template("gilson.html", data=scraped_data.to_html(index=False, classes="styled-table"))



#IMDb website
@app.route('/IMDb')
def IMDb():
    global scraped_data

    url = "https://www.imdb.com/chart/top/"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
 }

    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_data=[]

    movies=soup.find_all("div" ,class_='ipc-metadata-list-summary-item__c')
    for i in movies:
        name = i.find("h3", class_="ipc-title__text ipc-title__text--reduced").get_text(strip=True)
        rating = i.find("span", class_="ipc-rating-star--rating")
        rating = rating.get_text(strip=True) if rating else "N/A"
        released_year = i.find("span",class_="sc-caa65599-7 eeMIpC cli-title-metadata-item").get_text(strip=True) 
        timing = i.find_all("span", class_="sc-caa65599-7 eeMIpC cli-title-metadata-item")
        total_timimg = timing[1].get_text(strip=True) if len(timing) > 1 else "N/A"

        movie_data.append({
        "Movie Name": name,
        "Released Year": released_year,
        "Total_Timimg": total_timimg,
        "Rating": rating,
    })

    scraped_data = pd.DataFrame(movie_data)
    return render_template("IMDb.html", data=scraped_data.to_html(index=False, classes="styled-table"))




#pubmed website
@app.route('/pubmed')
def pubmed():
    global scraped_data

    url = "https://pubmed.ncbi.nlm.nih.gov/?term=asprin&filter=datesearch.y_1"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    medicine = []

    data = soup.find_all("article", class_='full-docsum')

    for i in data:
        
        medicine_name_tag = i.find("a", class_="docsum-title")
        PMID_tag = i.find("span", class_="docsum-pmid")
        description_tag = i.find("div", class_="full-view-snippet")
        type_tag = i.find("span", class_="publication-type spaced-citation-item citation-part")

        
        medicine_name = medicine_name_tag.get_text(strip=True) if medicine_name_tag else None
        PMID = PMID_tag.get_text(strip=True) if PMID_tag else None
        description = description_tag.get_text(strip=True) if description_tag else None
        type_ = type_tag.get_text(strip=True) if type_tag else None

        medicine.append({
            "Name": medicine_name,
            "PMID": PMID,
            "Description": description,
            "Type": type_
        })

    
    scraped_data = pd.DataFrame(medicine)

    return render_template(
        "pubmed.html",
        data=scraped_data.to_html(index=False, classes="styled-table")
    )





@app.route('/apnaapp')
def apnaapp():
    global scraped_data

    url = "https://apna.co/jobs?location_id=0&location_identifier=64e4ad63c35bd44248ca7741&location_type=NBCity&location_name=Gurgaon/Gurugram&search=true&text=Data%20Analyst&entity_id=10039789&entity_type=JobTitle&min_experience=0&raw_text_correction=true&session_id=d47dd086-1bdd-48b2-9e4d-150e5c255b0b"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_deatils = []

    jobs = soup.find_all("div", class_='min-h-full cursor-pointer rounded-lg border border-solid border-[#E8E7EA] bg-white p-[12px] shadow-100 md:m-0')

    for i in jobs:
        job = i.find("h2", class_="m-0 w-full text-[16px] font-semibold leading-[24px]").get_text(strip=True)

        Company_Name = i.find("div", class_="JobListCardstyles__JobCompany-ffng7u-8 gguURM").get_text(strip=True)

        Job_Location = i.find("p", class_="m-0 text-sm leading-[20px] text-[#8C8594]").get_text(strip=True)

        Salary_Range = [s.get_text(strip=True) for s in i.find_all("p", class_="m-0 truncate text-sm leading-[20px] text-[#8C8594]")]

        Job_Type = [j.get_text(strip=True) for j in i.find_all("p", class_="m-0 whitespace-nowrap text-xs text-[#8C8594]")]

        job_deatils.append({
            "Job": job,
            "Company Name": Company_Name,
            "Job Location": Job_Location,
            "Salary Range": Salary_Range,
            "Job Type": Job_Type
        })

    # ⬇️ RETURN LOOP KE BAAHAR
    scraped_data = pd.DataFrame(job_deatils)
    return render_template("apnaapp.html", data=scraped_data.to_html(index=False, classes="styled-table"))




if __name__ == '__main__':
    app.run(debug=True, port=3000, host="0.0.0.0")